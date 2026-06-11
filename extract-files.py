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
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

blob_fixups: blob_fixups_user_type = {
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
    check_elf=False,
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
