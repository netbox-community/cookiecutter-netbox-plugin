from netbox.plugins import PluginMenuButton, PluginMenuItem


plugin_buttons = [
    PluginMenuButton(
        link="plugins:{{ cookiecutter.underscored }}:{{ cookiecutter.__model_url_name }}_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
    )
]

menu_items = (
    PluginMenuItem(
        link="plugins:{{ cookiecutter.underscored }}:{{ cookiecutter.__model_url_name }}_list",
        link_text="{{ cookiecutter.plugin_name }}",
        buttons=plugin_buttons,
    ),
)
