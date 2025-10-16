# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import sys

from odoo import SUPERUSER_ID, registry
from odoo.api import Environment
from odoo.cli import Command
from odoo.tools import config
from ..tools.filestore import cleanup_filestore


class CleanupFilestore(Command):
    """
    Remove all files in filestore that does not referenced in ir.attachment model.

    The option "--addons-path" with all addons path split with comma must be defined in first argument even if
    "addons_path" parameter is already defined in config file.

    Example:
        odoo --addons-path=odoo/odoo/addons,odoo/addons,user/pyper cleanup_filestore -c odoo.conf --stop-after-init -d database_name
    """

    name = 'cleanup_filestore'

    def __init__(self):
        super().__init__()
        self.env = None

    def run(self, args):
        config.parse_config(args)

        try:
            dbname = config['db_name']

            if not dbname:
                raise Exception('Cleanup filestore command needs a database name. Use "-d" argument')

            with registry(dbname).cursor() as cr:
                self.env = Environment(cr, SUPERUSER_ID, {})
                self.cleanup()
        except Exception as e:
            sys.exit("ERROR: %s" % e)

    def cleanup(self):
        deleted_file_count = cleanup_filestore(self.env)

        print(f"Number of deleted files in filestore: {deleted_file_count}")
