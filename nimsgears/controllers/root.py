# -*- coding: utf-8 -*-
"""Main Controller"""

import json
from tg import expose, flash, require, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_

from nimsgears.lib.base import BaseController
from nimsgears.controllers.error import ErrorController
from nimsgears.controllers.data import DataController, AuthDataController
from nimsgears.controllers.access import AccessController
from nimsgears.controllers.browse import BrowseController
from nimsgears.controllers.groups import GroupsController

__all__ = ['RootController']


class RootController(BaseController):

    """Root controller for the nimsgears application."""

    groups = GroupsController()
    browse = BrowseController()
    access = AccessController()
    pub = DataController()
    auth = AuthDataController()
    error = ErrorController()

    @expose()
    def download(self, **kwargs):
        user = request.identity['user']
        id_dict = None
        result = {}
        if 'id_dict' in kwargs:
            id_dict = json.loads(kwargs['id_dict'])
            if 'sess' in id_dict:
                try:
                    sess_id = int(id_dict['sess'])
                    result['success'] = True
                except:
                    result['success'] = False
                else:
                    pass
                    #TODO Download stuff goes here
        return result

    @expose('nimsgears.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('nimsgears.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('nimsgears.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(environment=request.environ)

    @expose('nimsgears.templates.login')
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials.'), 'warning')
        return dict(page='login', login_counter=str(login_counter), came_from=came_from)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.
        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect('/login', params=dict(came_from=came_from, __logins=login_counter))
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """Redirect the user to the home page on logout."""
        redirect('/')
