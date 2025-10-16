# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import logging
import odoo

from odoo.fields import resolve_mro
from xmlrpc.client import MAXINT


_logger = logging.getLogger(__name__)


class IntegerFalsable(odoo.fields.Field):
    """ Encapsulates an :class:`int`. """
    type = 'integer'
    column_type = ('int4', 'int4')

    group_operator = 'sum'

    def _get_attrs(self, model_class, name):
        res = super()._get_attrs(model_class, name)
        # The default group_operator is None for sequence fields
        if 'group_operator' not in res and name == 'sequence':
            res['group_operator'] = None
        return res

    def convert_to_column(self, value, record, values=None, validate=True):
        return None if value is False else int(value or 0)

    def convert_to_cache(self, value, record, validate=True):
        if isinstance(value, dict):
            # special case, when an integer field is used as inverse for a one2many
            return value.get('id', None)

        return False if value is False else int(value or 0)

    def convert_to_record(self, value, record):
        return False if value is None else value

    def convert_to_read(self, value, record, use_display_name=True):
        # Integer values greater than 2^31-1 are not supported in pure XMLRPC,
        # so we have to pass them as floats :-(
        if value and value > MAXINT:
            return float(value)
        return value

    def _update(self, records, value):
        # special case, when an integer field is used as inverse for a one2many
        cache = records.env.cache
        for record in records:
            cache.set(record, self, value.id or 0)

    def convert_to_export(self, value, record):
        if value or value == 0:
            return value
        return ''


odoo.fields.IntegerFalsable = IntegerFalsable

# Extend Selection field
_original_field_selection_get_attrs = odoo.fields.Selection._get_attrs
def _field_selection_get_attrs(self, model_class, name):
    attrs = _original_field_selection_get_attrs(self, model_class, name)
    attrs.pop('selection_replace', None)

    return attrs


_original_field_selection_setup_attrs = odoo.fields.Selection._setup_attrs
def _field_selection_setup_attrs(self, model_class, name):
    _original_field_selection_setup_attrs(self, model_class, name)

    for field in self._base_fields:
        if 'selection_replace' in field.args:
            if self.related:
                _logger.warning("%s: selection_replace attribute will be ignored as the field is related", self)

            editable_selection = {t[0]: t[1] for t in self.selection}
            selection_replace = field.args['selection_replace']

            assert isinstance(selection_replace, list), \
                "%s: selection_replace=%r must be a list" % (self, selection_replace)

            for selection in selection_replace:
                assert selection[0] in editable_selection, \
                    "%s: selection_replace=%r must existing" % (self, selection_replace)

                editable_selection[selection[0]] = selection[1]

            new_selection = list(editable_selection.items())
            self.selection = new_selection


_original_field_selection_selection_modules = odoo.fields.Selection._selection_modules
def _field_selection_selection_modules(self, model):
    value_modules = _original_field_selection_selection_modules(self, model)

    if not isinstance(self.selection, list):
        return value_modules

    for field in reversed(resolve_mro(model, self.name, type(self).__instancecheck__)):
        module = field._module

        if not module:
            continue

        if 'selection_replace' in field.args:
            for value_label in field.args['selection_replace']:
                if len(value_label) > 1:
                    value_modules[value_label[0]].add(module)

    return value_modules


odoo.fields.Selection._get_attrs = _field_selection_get_attrs
odoo.fields.Selection._setup_attrs = _field_selection_setup_attrs
odoo.fields.Selection._selection_modules = _field_selection_selection_modules
