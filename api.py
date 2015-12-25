import json

from agora import Agora
from agora import DBSession

from pyramid.view import view_config
from pyramid.response import Response

from logging import getLogger
logger = getLogger(__name__)


def process_request_items(items):
    """takes a list of 2-tuples
       returns dict of list items
           uses first value of tuple as key, and
           uses second value of tuple as value
       """
    request_dict = {}
    for item in items:
        request_dict[item[0]] = item[1]
    return request_dict


class AgoraAPI(object):

    def __init__(self, request):
        self.request = request
        self.agora = Agora(DBSession)

    @view_config(route_name='list_ideas', request_method='GET')
    def get_ideas(self):

        """retrieve list of ideas"""

        get_items = self.request.GET.items()
        request_dict = process_request_items(get_items)
        logger.info(request_dict)
        if 'limit' in request_dict:
            limit = request_dict['limit']
            ideas = self.agora.get_ideas(limit)
        else:
            ideas = self.agora.get_ideas()

        items = []
        for idea in ideas:
            # add a custom HTTP header here for total count (X-Total-Count)
            items.append(idea.to_dict())
            logger.info("get_ideas: idea: %s" % str(idea))
            # dict = {'title': idea.title, 'idea': idea.idea}
            # items.append(dict)
        return items

    @view_config(route_name='view_idea', request_method='GET')
    def get_idea(self):

        """retrieve an idea"""

        if 'idea' in self.request.matchdict:
            id = int(self.request.matchdict['idea'])
            idea = self.agora.get_idea(id)
            if idea:
                return Response(
                    body=json.dumps({'title': idea.title, 'idea': idea.idea}),
                    status='200',
                    content_type='application/json'
                )

            else:
                return Response(
                    body=json.dumps({'message': 'Idea not found'}),
                    status='404 Not Found',
                    content_type='application/json')
        else:
            return Response(
                body=json.dumps({'message': 'No idea provided.'}),
                status='400 Bad Request',
                content_type='application/json')

    @view_config(route_name='add_idea', request_method='POST')
    def add_idea(self):

        """create a new idea"""

        post_items = self.request.POST.items()
        request_dict = process_request_items(post_items)
        title = request_dict['title'] if 'title' in request_dict else None
        idea = request_dict['idea'] if 'idea' in request_dict else None

        logger.info("title: %s" % title)

        new_idea_id = self.agora.add_idea(title, idea)

        if new_idea_id:
            return Response(
                body=json.dumps({'new_idea_id': new_idea_id}),
                status='201 Created',
                content_type='application/json')
        else:
            return Response(
                body=json.dumps({'message':
                                 'There was a problem adding your idea.'}),
                status='400 Bad Request',
                content_type='application/json')

    @view_config(route_name='edit_idea', request_method='PUT')
    def edit_idea(self):

        """edit an idea"""

        if 'idea' in self.request.matchdict:
            idea = int(self.request.matchdict['idea'])
        params = self.request.params

        self.agora.edit_idea(idea, **params)

    @view_config(route_name='delete_idea', request_method='DELETE')
    def delete_idea(self):

        """delete an idea"""

        idea = self.request.matchdict['idea']
        self.agora.delete_idea(idea)

        return Response(status='202 Accepted',
                        content_type='application/json; charset=UTF-8')
