#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from pathlib import Path
import runpy

from extract_utils.fixups_blob import (
    BlobFixupCtx,
    File,
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
from extract_utils.tools import (
    llvm_objdump_path,
)
from extract_utils.utils import (
    run_cmd,
)

namespace_imports = [
    'device/xiaomi/merlinx',
    'hardware/mediatek',
    'vendor/xiaomi/mt6768-common',
]

def blob_fixup_leica_camera(ctx, file, file_path, *args, **kwargs):
    patcher = Path(__file__).resolve().parents[1] / 'mt6768-common/camera/patch_vendor.py'
    runpy.run_path(str(patcher))['patch_file'](file_path, 'merlin')

def blob_fixup_graphic_buffer_size(
    ctx: BlobFixupCtx,
    file: File,
    file_path: str,
    *args,
    **kwargs,
):
    for line in run_cmd(
        [
            llvm_objdump_path,
            '--disassemble-all',
            file_path,
        ]
    ).splitlines():
        line = line.split(maxsplit=5)
        if len(line) != 6:
            continue
        # The size of GraphicBuffer changed from 0x100 to 0xd30
        offset, _, instruction, register, value, _ = line
        if instruction == 'mov' and register[:-1] == 'w0' and value == '#0x100':
            with open(file_path, 'rb+') as f:
                f.seek(int(offset[:-1], 16))
                f.write(b'\x00\xa6\x81\x52')  # AArch64 mov w0, #0xd30

blob_fixups: blob_fixups_user_type = {
    (
        'vendor/lib64/libmibokeh_mt6768.so',
        'vendor/lib64/libarcsoft_supernight.so',
    ): blob_fixup()
        .call(blob_fixup_leica_camera),
    'vendor/bin/hw/mtkfusionrild' : blob_fixup()
        .add_needed('libutils-v32.so'),
    'vendor/lib/hw/audio.primary.mt6768.so': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libalsautils.so', 'libalsautils-v31.so')
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    'vendor/lib/librt_extamp_intf.so' : blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    'vendor/lib64/libcam.utils.sensorprovider.so': blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so'),
    'vendor/lib64/libmi_watermark.so': blob_fixup()
        .add_needed('libpiex_shim.so'),
    (
        'vendor/lib64/libmtkcam_stdutils.so',
        'vendor/lib64/hw/android.hardware.camera.provider@2.6-impl-mediatek.so',
    ): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    ('vendor/lib64/lib3a.flash.so', 'vendor/lib64/libSQLiteModule_VER_ALL.so'): blob_fixup()
         .add_needed('liblog.so'),
    'vendor/lib64/libsysenv.so' : blob_fixup()
        .add_needed('libbase_shim.so'),
    'vendor/lib64/libvidhance.so': blob_fixup()
        .add_needed('libcomparetf2_shim.so')
        .add_needed('libdemangle.so'),
    'vendor/lib64/libutinterface_custom_md.so': blob_fixup()
        .add_needed('libutinterface_md.so'),
    (
        'vendor/lib64/libcam.hal3a.v3.so',
        'vendor/lib64/libmtkcam_3rdparty.vidhance.so',
    ): blob_fixup()
        .call(blob_fixup_graphic_buffer_size),
}  # fmt: skip

module = ExtractUtilsModule(
    'merlinx',
    'xiaomi',
    blob_fixups=blob_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'mt6768-common', module.vendor
    )
    utils.run()
