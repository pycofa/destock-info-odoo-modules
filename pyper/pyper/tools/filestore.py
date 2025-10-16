# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import os

from odoo.api import Environment
from odoo.http import db_list
from odoo.tools import config


def cleanup_filestore(env: Environment):
    deleted_file_count = 0
    dbname = config['db_name']

    if not dbname:
        dbs = db_list(True)
        dbname = dbs[0] if dbs else False

    filestore_path = config.filestore(dbname)
    attachments = env['ir.attachment'].with_context({
        'skip_res_field_check': True,
    }).search_read([('store_fname', '!=', False)], ['store_fname'])
    valid_files = {attachment['store_fname'] for attachment in attachments}

    for root, _, files in os.walk(filestore_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, filestore_path)

            if relative_file_path not in valid_files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                deleted_file_count += 1

    return deleted_file_count
