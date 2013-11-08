from logging import getLogger

from ckan.common import json
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

log = getLogger(__name__)
ignore_empty = p.toolkit.get_validator('ignore_empty')
natural_number_validator = p.toolkit.get_validator('natural_number_validator')


class ReclineView(p.SingletonPlugin):
    '''
    This base class for the Recline view extensions.
    '''
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IResourceView, inherit=True)

    # schema fields that apply to all Recline views
    schema = {'offset': [ignore_empty, natural_number_validator],
              'limit': [ignore_empty, natural_number_validator]}

    def update_config(self, config):
        '''
        Set up the resource library, public directory and
        template directory for the preview
        '''
        toolkit.add_public_directory(config, 'theme/public')
        toolkit.add_template_directory(config, 'theme/templates')
        toolkit.add_resource('theme/public', 'ckanext-reclinepreview')

    def can_view(self, data_dict):
        if data_dict['resource'].get('datastore_active'):
            return True
        return False

    def setup_template_variables(self, context, data_dict):
        return {'resource_json': json.dumps(data_dict['resource']),
                'resource_view_json': json.dumps(data_dict['data'])}

    def view_template(self, context, data_dict):
        return 'recline_view.html'


class ReclineGrid(ReclineView):
    '''
    This extension views resources using a Recline grid.
    '''

    def info(self):
        return {'name': 'recline_grid',
                'title': 'Grid',
                'schema': self.schema}

    def form_template(self, context, data_dict):
        return 'recline_grid_form.html'


class ReclineGraph(ReclineView):
    '''
    This extension views resources using a Recline graph.
    '''

    graph_types = [{'value': 'lines-and-points',
                    'text': 'Lines and points'},
                   {'value': 'lines', 'text': 'Lines'},
                   {'value': 'points', 'text': 'Points'},
                   {'value': 'bars', 'text': 'Bars'},
                   {'value': 'columns', 'text': 'Columns'}]

    def info(self):
        # TODO: add validators
        self.schema.update({
            'graph_type': [ignore_empty],
            'group_column': [ignore_empty],
            'series_a': [ignore_empty]
        })
        return {'name': 'recline_graph',
                'title': 'Graph',
                'schema': self.schema}

    def setup_template_variables(self, context, data_dict):
        vars = ReclineView.setup_template_variables(self, context, data_dict)
        vars.update({'graph_types': self.graph_types})
        return vars

    def form_template(self, context, data_dict):
        return 'recline_graph_form.html'


class ReclineMap(ReclineView):
    '''
    This extension views resources using a Recline map.
    '''

    def info(self):
        return {'name': 'recline_map',
                'title': 'Map',
                'schema': self.schema}

    def form_template(self, context, data_dict):
        return 'recline_map_form.html'
