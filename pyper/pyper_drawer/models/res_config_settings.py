# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    drawer_show_root_app = fields.Boolean(
        'Show only root menu items in Drawer?',
        config_parameter='pyper_drawer.drawer_props.showRootApp',
    )

    drawer_nav = fields.Boolean(
        'Use nav style?',
        config_parameter='pyper_drawer.drawer_props.nav',
    )

    drawer_fixed_top = fields.Boolean(
        'Position fixed on top?',
        config_parameter='pyper_drawer.drawer_props.fixedTop',
    )

    drawer_always_header = fields.Boolean(
        'Always display header?',
        config_parameter='pyper_drawer.drawer_props.alwaysHeader',
    )

    drawer_always_footer = fields.Boolean(
        'Always display footer?',
        config_parameter='pyper_drawer.drawer_props.alwaysFooter',
    )

    drawer_always_mini = fields.Boolean(
        'Always mini drawer?',
        config_parameter='pyper_drawer.drawer_props.alwaysMini',
    )

    drawer_minifiable = fields.Boolean(
        'Minifiable?',
        config_parameter='pyper_drawer.drawer_props.minifiable',
    )

    drawer_init_minified = fields.Boolean(
        'Minified on initialisation?',
        config_parameter='pyper_drawer.drawer_props.initMinified',
    )

    drawer_popover_minified = fields.Boolean(
        'Popover title for mini drawer?',
        config_parameter='pyper_drawer.drawer_props.popoverMinified',
    )

    drawer_close_action = fields.Boolean(
        'Display close button on drawer?',
        config_parameter='pyper_drawer.drawer_props.closeAction',
    )

    drawer_close_on_click = fields.Boolean(
        'Close drawer on click?',
        config_parameter='pyper_drawer.drawer_props.closeOnClick',
    )

    drawer_close_all_unactivated_items_on_select = fields.Boolean(
        'Close all unactivated items on select?',
        config_parameter='pyper_drawer.drawer_props.closeAllUnactivatedItemsOnClick',
    )

    drawer_sub_items_depth = fields.Integer(
        'Sub item depth',
        config_parameter='pyper_drawer.drawer_props.subItemsDepth',
    )

    drawer_next_items_sub_panel = fields.Boolean(
        'Next items in sub panel',
        config_parameter='pyper_drawer.drawer_props.nextItemsSubPanel',
    )

    drawer_drag_end_ratio = fields.Float(
        'Custom width ratio of drag end',
        config_parameter='pyper_drawer.drawer_props.dragEndRatio',
    )

    drawer_hide_empty_category = fields.Boolean(
        'Hide empty categories?',
        config_parameter='pyper_drawer.drawer_props.hideEmptyCategory',
    )

    drawer_hide_category_label_full = fields.Boolean(
        'Hide category label in full?',
        config_parameter='pyper_drawer.drawer_props.hideCategoryLabelFull',
    )

    drawer_hide_category_label_minified = fields.Boolean(
        'Hide category label in mini?',
        config_parameter='pyper_drawer.drawer_props.hideCategoryLabelMinified',
    )

    drawer_show_category_section_minified = fields.Boolean(
        'Show category section in mini?',
        config_parameter='pyper_drawer.drawer_props.showCategorySectionMinified',
    )

    drawer_disabled_on_small_screen = fields.Boolean(
        'Disable drawer on small screen?',
        config_parameter='pyper_drawer.drawer_props.disabledOnSmallScreen',
    )

    drawer_hide_navbar_apps_menu = fields.Boolean(
        'Hide apps menu in navbar?',
        config_parameter='pyper_drawer.drawer_props.hideNavbarAppsMenu',
    )

    drawer_toggler_auto_hide = fields.Boolean(
        'Auto hide the toggler?',
        config_parameter='pyper_drawer.drawer_toggler_props.autoHide',
    )

    drawer_toggler_use_caret_icon = fields.Boolean(
        'Use caret icon in toggler?',
        config_parameter='pyper_drawer.drawer_toggler_props.useCaretIcon',
    )
