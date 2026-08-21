#
# Copyright (C) 2022 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from mt6768-common
$(call inherit-product, device/xiaomi/mt6768-common/mt6768.mk)

# AAPT
PRODUCT_AAPT_CONFIG := normal
PRODUCT_AAPT_PREF_CONFIG := xxhdpi

# Boot animation
TARGET_SCREEN_WIDTH := 1080
TARGET_SCREEN_HEIGHT := 2340

# Firmware
RECOVERY_TS_FW_PATH := vendor/xiaomi/merlinx/proprietary/vendor/firmware

PRODUCT_COPY_FILES += \
    $(RECOVERY_TS_FW_PATH)/novatek_ts_g6_fw.bin:recovery/root/vendor/firmware/novatek_ts_g6_fw.bin \
    $(RECOVERY_TS_FW_PATH)/novatek_ts_g6_mp.bin:recovery/root/vendor/firmware/novatek_ts_g6_mp.bin \
    $(RECOVERY_TS_FW_PATH)/novatek_ts_g6_mp.bin:recovery/root/vendor/firmware/novatek_ts_g6_mp.bin \
    $(RECOVERY_TS_FW_PATH)/novatek_ts_72d_fw.bin:recovery/root/vendor/firmware/novatek_ts_72d_fw.bin \
    $(RECOVERY_TS_FW_PATH)/novatek_ts_72d_mp.bin:recovery/root/vendor/firmware/novatek_ts_72d_mp.bin

# NFC
PRODUCT_PACKAGES += \
    android.hardware.nfc@1.2-service \
    com.android.nfc_extras \
    NfcNci \
    Tag

PRODUCT_COPY_FILES += \
    frameworks/native/data/etc/android.hardware.nfc.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/sku_merlinnfc/android.hardware.nfc.xml \
    frameworks/native/data/etc/android.hardware.nfc.ese.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/sku_merlinnfc/android.hardware.nfc.ese.xml \
    frameworks/native/data/etc/android.hardware.nfc.hce.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/sku_merlinnfc/android.hardware.nfc.hce.xml \
    frameworks/native/data/etc/android.hardware.nfc.hcef.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/sku_merlinnfc/android.hardware.nfc.hcef.xml \
    frameworks/native/data/etc/android.hardware.nfc.uicc.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/sku_merlinnfc/android.hardware.nfc.uicc.xml \
    frameworks/native/data/etc/com.android.nfc_extras.xml:$(TARGET_COPY_OUT_ODM)/etc/permissions/sku_merlinnfc/com.android.nfc_extras.xml

# Overlays
PRODUCT_PACKAGES += \
    ApertureOverlayMerlinx \
    FrameworksResOverlayMerlinx \
    SettingsOverlayMerlinx \
    SettingsProviderOverlayMerlinx \
    SystemUIOverlayMerlinx

# Rootdir
PRODUCT_PACKAGES += \
    init.project.rc

# Soong
PRODUCT_SOONG_NAMESPACES += \
    $(LOCAL_PATH)

# Shipping API Level
PRODUCT_SHIPPING_API_LEVEL := 29

# Thermal
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/configs/thermal_info_config.json:$(TARGET_COPY_OUT_VENDOR)/etc/thermal_info_config.json

# Inherit the proprietary files
$(call inherit-product, vendor/xiaomi/merlinx/merlinx-vendor.mk)
