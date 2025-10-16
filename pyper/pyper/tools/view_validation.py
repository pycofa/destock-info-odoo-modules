# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import logging
import os

from lxml import etree

from odoo import tools


_logger = logging.getLogger(__name__)
_original_relaxng = tools.view_validation.relaxng
_extend_relaxng = {}


def extend_relaxng(original_relaxng_file, extend_relaxng_file):
    if original_relaxng_file not in _extend_relaxng:
        _extend_relaxng[original_relaxng_file] = {
            'extended': False,
            'files': [],
        }

    _extend_relaxng[original_relaxng_file]['files'].append(extend_relaxng_file)


def _extend_relaxng_tree(inherit_element: etree._ElementTree, extend_element: etree._ElementTree):
    nsmap = {'rng': 'http://relaxng.org/ns/structure/1.0'}

    for xpath_element in extend_element.xpath('//xpath', namespaces=nsmap):
        expr = xpath_element.attrib['expr']
        position = xpath_element.attrib.get('position', 'inside')
        modifications = xpath_element[:]

        targets = inherit_element.xpath(expr, namespaces=nsmap)

        for target in targets:
            if position == 'inside':
                for mod in modifications:
                    target.append(mod)
            elif position == 'before':
                for mod in modifications:
                    target.addprevious(mod)
            elif position == 'after':
                for mod in modifications:
                    target.addnext(mod)
            elif position == 'replace':
                parent = target.getparent()

                if parent is not None:
                    for mod in modifications:
                        parent.insert(parent.index(target), mod)

                    parent.remove(target)


def relaxng(view_type):
    res = _original_relaxng(view_type)
    relaxng_cache = tools.view_validation._relaxng_cache
    rng_file = os.path.join('base', 'rng', '%s_view.rng' % view_type)

    if relaxng_cache[view_type] and _extend_relaxng.get(rng_file) and not _extend_relaxng.get(rng_file).get('extended'):
        try:
            with tools.file_open(rng_file) as frng:
                relaxng_doc = etree.parse(frng)
                extended_rng_files = _extend_relaxng.get(rng_file).get('files')

                for extended_rng_file in extended_rng_files:
                    with tools.file_open(extended_rng_file) as efrng:
                        relaxng_ext_doc = etree.parse(efrng)
                        _extend_relaxng_tree(relaxng_doc, relaxng_ext_doc)

                relaxng_cache[view_type] = etree.RelaxNG(relaxng_doc)
                _extend_relaxng.get(rng_file).update({'extended': True})
        except Exception:
            _logger.exception('Failed to load RelaxNG XML schema for views validation')

    return res

tools.view_validation.relaxng = relaxng
