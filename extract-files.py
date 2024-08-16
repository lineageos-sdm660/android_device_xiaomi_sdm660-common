#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import extract_utils.tools

extract_utils.tools.DEFAULT_PATCHELF_VERSION = '0_17_2'

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/sdm660-common',
    'hardware/qcom-caf/sdm660',
    'hardware/qcom-caf/wlan',
    'hardware/xiaomi',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/display',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
    ): lib_fixup_vendor_suffix,
    (
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    ('system_ext/lib64/lib-imscamera.so', 'system_ext/lib64/lib-imsvideocodec.so'): blob_fixup()
        .add_needed('libgui_shim.so'),
    'vendor/bin/mlipayd@1.1': blob_fixup()
        .remove_needed('vendor.xiaomi.hardware.mtdservice@1.0.so'),
    'vendor/bin/pm-service': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v33.so'),
    ('vendor/lib64/libmlipay.so', "vendor/lib64/libmlipay@1.1.so"): blob_fixup()
        .binary_regex_replace(b'/system/etc/firmware', b'/vendor/firmware\x00\x00\x00\x00')
        .remove_needed('vendor.xiaomi.hardware.mtdservice@1.0.so'),
    'vendor/lib64/libwvhidl.so': blob_fixup()
        .add_needed('libcrypto_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sdm660-common',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

module.add_proprietary_file('proprietary-files-fm.txt').add_copy_files_guard(
    'BOARD_HAVE_QCOM_FM', 'true'
)
module.add_proprietary_file('proprietary-files-ir.txt').add_copy_files_guard(
    'BOARD_HAVE_IR', 'true'
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
