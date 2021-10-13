import ckan.plugins as plugins
from ckan.plugins import implements, toolkit
from ckanext.datasetform import blueprint


class DatasetformPlugin(plugins.SingletonPlugin):
    # implements(plugins.IRoutes, inherit=True)
    implements(plugins.IConfigurer, inherit=True)
    implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')

    # IBlueprint

    def get_blueprint(self):
        return blueprint.datavic_datasetform