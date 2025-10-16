# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import logging

from odoo.models import Model
from ..tools.filestore import cleanup_filestore

_logger = logging.getLogger(__name__)


class IrAttachment(Model):
    _inherit = 'ir.attachment'

    def _run_cleanup_filestore(self):
        deleted_file_count = cleanup_filestore(self.env)
        _logger.info(f"Number of deleted files in filestore: {deleted_file_count}")
