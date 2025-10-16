/** @odoo-module */

import {Component, onMounted, useState} from '@odoo/owl';
import {_t} from '@web/core/l10n/translation';
import {x2ManyCommands} from '@web/core/orm_service';
import {useService} from '@web/core/utils/hooks';
import {Dropdown} from '@web/core/dropdown/dropdown';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import {useOpenMany2XRecord, useSelectCreate} from '@web/views/fields/relational_utils';
import {ConfirmationDialog} from '@web/core/confirmation_dialog/confirmation_dialog';

export const TRUE_VALUES = [
    'True',
    'true',
    '1',
];

export const FALSE_VALUES = [
    'False',
    'false',
    '0',
];

export class ViewsSwitcher extends Component {
    static template = 'pyper_web_view.ViewsSwitcher';

    static props = {
        defaultTitle: {
            type: String,
            optional: true,
        },
        placeholder: {
            type: String,
            optional: true,
        },
    };

    static components = {
        Dropdown,
        DropdownItem,
    };

    setup() {
        this.actionService = useService('action');
        this.dialogService = useService('dialog');
        this.orm = useService('orm');

        this.state = useState({
            mounted: false,
            views: [],
            selectedView: null,
        });

        const resModel = 'ir.views';

        this.openMany2X = useOpenMany2XRecord({
            resModel,
            activeActions: {
                create: true,
                write: true,
            },
            isToMany: false,
            fieldString: _t('Saved views'),
            onRecordSaved: (record) => {
                const view = {...record.data, id: record.resId};
                const vIdx = this.state.views.findIndex(v => v.id === view.id);

                if (vIdx !== -1) {
                    this.state.views.splice(vIdx, 1, view);
                }

                this.env.bus.trigger('CLEAR-CACHES');

                if (view['ir_action_id'] && view['ir_action_id'][0] && view['ir_action_id'][0] === this.env?.config?.actionId) {
                    this.selectView(view);
                }
            },
            onRecordDiscarded: () => {},
            onClose: () => {},
        });

        this.selectCreate = useSelectCreate({
            resModel,
            activeActions: {
                write: true,
            },
            onCreateEdit: async ({context}) => {
                await this.openMany2X({context});
            },
            onUnselect: () => {},
            onSelected: (resId) => {
                const resIds = Array.isArray(resId) ? resId : [resId];

                if (resIds.length > 0) {
                    const vIdx = this.state.views.findIndex(v => v.id === resIds[0]);

                    if (vIdx !== -1) {
                        this.selectView(this.state.views[vIdx]);
                    }
                }
            },
        });

        onMounted(async () => {
            if (!this.currentActionId) {
                return;
            }

            this.state.mounted = true;

            if (this.displaySwitcher) {
                const views = await this.orm.searchRead(
                    'ir.views',
                    [...this.domain, ['ir_action_id', '=', this.currentActionId]],
                    this.viewsFields,
                    {limit: 1}
                );

                if (views.length > 0) {
                    this.state.selectedView = views[0];
                }
            }
        });
    }

    get isMounted() {
        return this.state.mounted;
    }

    get currentActionId() {
        return this.env.config?.actionId || null;
    }

    get currentViewType() {
        return this.env.config?.viewType || null;
    }

    get currentModelName() {
        return this.env.model?.config?.resModel || this.env.searchModel?.resModel || null;
    }

    get currentLimit() {
        return this.env.model?.config?.initialLimit || this.actionService?.currentController?.action?.limit || 80;
    }

    get currentDomain() {
        return this.env.model?.config?.domain || this.env.searchModel?.domain || [];
    }

    get currentOrderBy() {
        return this.env.model?.config?.orderBy || this.env.searchModel?.orderBy || [];
    }

    get currentGroupBy() {
        return this.env.model?.config?.groupBy || this.env.searchModel?.groupBy || [];
    }

    get displaySwitcher() {
        return this.isMounted && !this.excludedViewTypes.includes(this.currentViewType)
            && ![undefined, 'ir.views', 'ir.ui.menu'].includes(this.currentModelName);
    }

    get excludedViewTypes() {
        return ['form'];
    }

    get viewsFields() {
        return ['id', 'name', 'category', 'shared', 'view_mode', 'ir_action_id', 'main_ir_action_id'];
    }

    get domain() {
        const categories = this.availableCategories.map(item => item[0]);

        return [['res_model_id.model', '=', this.currentModelName], ['category', 'in', categories]];
    }

    get limit() {
        return 300;
    }

    get viewModeIcons() {
        return {
            'tree': 'oi oi-view-list',
            'kanban': 'oi oi-view-kanban',
            undefined: 'fa fa-folder-o',
        }
    }

    get togglerIcon() {
        return this.getViewIcon(this.state.selectedView?.view_mode);
    }

    get togglerLabel() {
        return this.state.selectedView?.name || this.props.defaultTitle || this.placeholder;
    }

    get placeholder() {
        return this.props.placeholder || _t('Select a view');
    }

    get createLabel() {
        return _t('Create a new view');
    }

    get availableCategories() {
        return [
            ['system', null],
            ['personal', _t('My views')],
            ['shared', _t('Shared views')],
        ];
    }

    get availableViewTypes() {
        return {
            'tree': 'tree',
            'list': 'tree',
            'kanban': 'kanban',
            undefined: 'tree',
        }
    }

    get categorizedViews() {
        const categoryViews = [];
        const categ = {};
        this.availableCategories.forEach((cat) => categ[cat[0]] = []);

        this.state.views.forEach((view) => {
            categ[view.category].push(view);
        });

        this.availableCategories.forEach((cat) => {
            categoryViews.push({
                value: cat[0],
                name: cat[1],
                views: categ[cat[0]] ? [...categ[cat[0]]] : [],
            });
        });

        return categoryViews;
    }

    getViewIcon(viewMode) {
        return this.viewModeIcons[viewMode] || this.viewModeIcons[undefined];
    }

    getValidViewType(viewMode) {
        return this.availableViewTypes[viewMode] || this.availableViewTypes[undefined];
    }

    async onDropdownOpen() {
        if (this.state.views.length > 0) {
            this.state.views.splice(0, this.state.views.length);
        }

        await this.loadViews();
    }

    selectView(view) {
        this.state.selectedView = view || null;

        if (view && view['ir_action_id'] && view['ir_action_id'][0]) {
            this.actionService.doAction(view['ir_action_id'][0]).then();
        }
    }

    configureViews(categoryName) {
        this.selectCreate({
            domain: [['category', '=', categoryName], ...this.domain],
            context: this.getContext(),
            title: _t('Configure views'),
        });
    }

    async createView() {
        await this.openMany2X({context: this.getContext()});
    }

    async editView(viewId) {
        await this.openMany2X({resId: viewId});
    }

    openConfirmationDialog(viewId) {
        const view = this.state.views.find((view) => view.id === viewId);
        const dialogProps = {
            title: _t('Warning'),
            body: view.shared
                ? _t('This view is shared and will be removed for everyone.')
                : _t('Are you sure that you want to remove this view?'),
            confirmLabel: _t('Delete view'),
            confirm: async () => {
                await this.orm.unlink('ir.views', [viewId]);

                if (this.state.selectedView?.id === viewId) {
                    this.selectView(null);
                }

                await this._onViewDeleted(view);

                const vIdx = this.state.views.findIndex(v => v.id === viewId);

                if (vIdx !== -1) {
                    this.state.views.splice(vIdx, 1);
                }

                this.env.bus.trigger('CLEAR-CACHES');
            },
            cancel: () => {},
        };
        this.dialogService.add(ConfirmationDialog, dialogProps);
    }

    async loadViews() {
        this.state.views = await this.orm.searchRead(
            'ir.views',
            this.domain,
            this.viewsFields,
            {
                limit: this.limit,
            }
        );
    }

    getContext() {
        const context = {};
        context['default_res_model_name'] = this.currentModelName;
        context['default_view_mode'] = this.getValidViewType(this.currentViewType);
        context['default_limit'] = this.currentLimit;
        context['default_domain'] = this.currentDomain;
        context['default_res_field_ids'] = [];
        context['default_res_group_by_ids'] = [];
        context['default_res_order_by_ids'] = [];
        context['default_main_ir_action_id'] = this.state.selectedView?.['main_ir_action_id']?.[0] || this.currentActionId || false;

        if (this.currentGroupBy.length > 0) {
            this.currentGroupBy.forEach((groupName) => {
                context['default_res_group_by_ids'].push(x2ManyCommands.create(undefined, {
                    'field_name': groupName,
                }));
            });
        }

        if (this.currentOrderBy.length > 0) {
            const item = this.currentOrderBy[0];
            context['default_res_order_by_ids'].push(x2ManyCommands.create(undefined, {
                'field_name': item.name,
                'sort': item.asc ? 'asc': 'desc',
            }));
        }

        const arch = this.env.config.viewArch;

        if (FALSE_VALUES.includes(arch.getAttribute('create'))) {
            context['default_no_create'] = true;
        }

        if (FALSE_VALUES.includes(arch.getAttribute('edit'))) {
            context['default_no_edit'] = true;
        }

        if (FALSE_VALUES.includes(arch.getAttribute('delete'))) {
            context['default_no_delete'] = true;
        }

        if (FALSE_VALUES.includes(arch.getAttribute('import'))) {
            context['default_no_import'] = true;
        }

        if (TRUE_VALUES.includes(arch.getAttribute('sample'))) {
            context['sample'] = true;
        }

        if (arch.hasAttribute('class')) {
            context['default_classes'] = arch.getAttribute('class');
        }

        if (arch.hasAttribute('js_class')) {
            context['default_js_class'] = arch.getAttribute('js_class');
        }

        if (['tree', 'list'].includes(this.currentViewType)) {
            this._buildTreeContext(context);
        }

        if ('kanban' === this.currentViewType) {
            this._buildKanbanContext(context);
        }

        return context;
    }

    _buildTreeContext(context) {
        const arch = this.env.config.viewArch;

        if (TRUE_VALUES.includes(arch.getAttribute('editable'))) {
            context['default_editable'] = true;
        }

        if (FALSE_VALUES.includes(arch.getAttribute('duplicate'))) {
            context['default_no_duplicate'] = true;
        }

        if (FALSE_VALUES.includes(arch.getAttribute('export_xlsx'))) {
            context['default_no_export'] = true;
        }

        if (FALSE_VALUES.includes(arch.getAttribute('open_form_view'))) {
            context['default_no_open_form_view'] = true;
        }

        if (TRUE_VALUES.includes(arch.getAttribute('multi_edit'))) {
            context['default_multi_edit'] = true;
        }

        if (TRUE_VALUES.includes(arch.getAttribute('expand'))) {
            context['default_expand'] = true;
        }

        const fields = this.env.config.viewArch.querySelectorAll('field');

        fields.forEach(field => {
            const vals = {
                'field_name': field.getAttribute('name'),
            };
            const string = field.getAttribute('string');
            const invisible = field.getAttribute('column_invisible');
            const optional = field.getAttribute('optional');
            const widget = field.getAttribute('widget');
            const options = field.getAttribute('options');
            const width = field.getAttribute('width');

            if (string) {
                vals['label'] = string;
            }

            if (invisible) {
                vals['optional'] = 'invisible';
            } else if (optional) {
                vals['optional'] = optional;
            }

            if (widget) {
                vals['widget'] = widget;
            }

            if (options) {
                vals['options'] = options;
            }

            if (width) {
                vals['width'] = width;
            }

            context['default_res_field_ids'].push(x2ManyCommands.create(undefined, vals));
        });
    }

    _buildKanbanContext(context) {
        const arch = this.env.config.viewArch;

        if (FALSE_VALUES.includes(arch.getAttribute('group_create'))) {
            context['default_no_group_create'] = true;
        }

        if (FALSE_VALUES.includes(arch.getAttribute('quick_create'))) {
            context['default_no_quick_create'] = true;
        }

        if (FALSE_VALUES.includes(arch.getAttribute('records_draggable'))) {
            context['default_no_records_draggable'] = true;
        }
    }

    async _onViewDeleted(view) {}
}
