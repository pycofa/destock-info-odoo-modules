Pyper SaaS
----------

# Usage

1. Create a `__pyper_saas__.py` file in your addons directory:
2. Add content with (default values):
```python
{
    # Check if restrict addons is enabled
    'enable': None,
    # Check if all addons defined in the self directory of __pyper_saas__.py file must be added
    'include_self_addons': False,
    # Check if minimal odoo addons must be added automatically
    'include_minimal_addons': True,
    # Define the addon paths in self directory to add all addons in each path
    'available_addon_paths': [],
    # Define excluded addons when it is found in the 'available_addon_paths'
    'excluded_available_addons': [],
    # Define manually the available addons
    'available_addons': [],
    # Define manually the uninstallable addons (used when addon is required by invalid dependency,
    # ex. ref xml defined in other addon)
    'uninstallable_addons': [],
}
```
3. Enable `pyper_saas` by defining `enable` property with `True` value 
4. Edit the config and mainly the `available_addons` property or `available_addon_paths`
