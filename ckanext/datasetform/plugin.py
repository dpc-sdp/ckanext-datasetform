import ckan.plugins as plugins
from ckan.plugins import implements, toolkit

from ckanext.datasetform import blueprint
from ckanext.datasetform.logic.action import datasetform_actions


class DatasetformPlugin(plugins.SingletonPlugin):
    # implements(plugins.IRoutes, inherit=True)
    implements(plugins.IConfigurer, inherit=True)
    implements(plugins.IBlueprint)
    implements(plugins.IActions)

    # IConfigurer

    def update_config(self, config):
        toolkit.add_template_directory(config, "templates")

    # IBlueprint

    def get_blueprint(self):
        return blueprint.datavic_datasetform

    # IActions

    def get_actions(self):
        return datasetform_actions()
