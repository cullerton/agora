from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.renderers import get_renderer
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql import select
from unicodedata import normalize

from logging import getLogger
logger = getLogger(__name__)

from .models import DBSession, Idea
from .agora import agora_utils

def site_layout():
    renderer = get_renderer("templates/main_template.pt")
    layout = renderer.implementation().macros['layout']
    return layout

# def get_footer():
#     renderer = get_renderer("templates/footer.pt")
#     layout = renderer.implementation().macros['layout']
#     return layout


@view_config(route_name='agora', renderer='templates/agora.pt')
class agora_view(object, agora_utils):

    def __init__(self, request):
        logger.info("agora_view: __init__: ")
        self.request = request
        site_location = request.registry.settings['site_location']
        self.view_params = {'site_name': request.registry.settings['site_name'],
                            'description': request.registry.settings['site_description'],
                            'home_url': request.route_url('agora'),
                            'add_idea_url': request.route_url('add_idea')}

    def __call__(self):
        """'Home Page' for Agora
            retrieves the most recent ideas and 
            returns them in the response
        """
        logger.info("agora_view: __call__: ")
        view_params = self.view_params
        ideas = self.getIdeasByDate()
        # logger.info("agora_view: __call__: ideas: %s" % str(ideas))
        view_params['ideas'] = ideas
        view_params['layout'] = site_layout()
        # view_params['footer'] = get_footer()
        return view_params

@view_config(route_name='add_idea', renderer='templates/add_idea.pt')
class add_idea(object, agora_utils):

    def __init__(self, request):
        logger.info("add_idea: __init__: ")
        self.request = request
        self.view_params = {'site_name': request.registry.settings['site_name'],
                            'description': request.registry.settings['site_description'],
                            'home_url': request.route_url('agora')}

    def __call__(self):
        """view to add an idea"""
        logger.info("add_idea: __call__: ")
        view_params = self.view_params
        if 'form.submitted' in self.request.params:
            title = self.request.params['title']
            intro = self.request.params['intro']
            body = self.request.params['body']
            id = self.slugify(title)
            category_id = 1
            idea = Idea(id, title, intro, body, category_id, None, None)
            try:
                DBSession.add(idea)
            except Exception, e:
                logger.info("add_idea: __call__: Exception: %s" % str(e))
                pass
            else:
                redirect_url = self.request.route_url('idea_view', self.request, idea=id)
                logger.info("add_idea: __call__: redirect_url: %s" % str(redirect_url))
                return HTTPFound(location = redirect_url)

        save_url = self.request.route_url('add_idea')
        idea = Idea('','', '', '',0,None,None)
        view_params['save_url'] = save_url
        view_params['idea'] = idea
        return view_params

@view_config(route_name='idea_view', renderer='templates/idea_view.pt')
class idea_view(object, agora_utils):

    def __init__(self, request):
        logger.info("idea_view: __init__: ")
        self.request = request
        site_location = request.registry.settings['site_location']
        logger.info("idea_view: __init__: site_location: %s" % str(site_location))
        self.view_params = {'site_name': request.registry.settings['site_name'],
                            'description': request.registry.settings['site_description'],
                            'home_url': request.route_url('agora')}

    def __call__(self):
        """"""
        logger.info("idea_view: __call__: ")
        view_params = self.view_params
        id = self.request.matchdict['idea']
        idea = self.getIdeaById(id)
        view_params['idea'] = idea
        return view_params

