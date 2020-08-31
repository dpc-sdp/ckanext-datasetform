import ckan.plugins as plugins
from ckan.plugins import implements, toolkit
from ckanext.datasetform import blueprint


class DatasetformPlugin(plugins.SingletonPlugin):
    # implements(plugins.IRoutes, inherit=True)
    implements(plugins.IConfigurer, inherit=True)
    implements(plugins.IPackageController, inherit=True)
    implements(plugins.IBlueprint)


    # IRoutes

    # def before_map(self, map):
    #     """
    #         /dataset/NAME/contact
    #     """
    #     controller = 'ckanext.datasetform.controller:ContactController'
    #     map.connect('/dataset/{dataset_id}/contact', controller=controller, action='send')
    #     return map

    # IConfigurer

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        # toolkit.add_resource('fanstatic', 'datasetform')

    # IPackageController

    def before_view(self, pkg_dict):
        return pkg_dict

    # IBlueprint

    def get_blueprint(self):
        return blueprint.datavic_datasetform