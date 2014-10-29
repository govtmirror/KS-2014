# -*- coding: utf-8 -*-
import webapp2
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb
from collections import OrderedDict, Counter
from wtforms import fields
from bp_includes import forms
from bp_includes.lib.basehandler import BaseHandler

from bp_includes.models import Group
import logging


class AdminGroupListHandler(BaseHandler):
    def get(self):
        p = self.request.get('p')
        q = self.request.get('q')
        c = self.request.get('c')
        forward = True if p not in ['prev'] else False
        cursor = Cursor(urlsafe=c)

        if q:
            qry = Group.query(ndb.OR(Group.name == q.lower()))
        else:
            qry = Group.query()

        PAGE_SIZE = 50
        if forward:
            groups, next_cursor, more = qry.order(self.user_model.key).fetch_page(PAGE_SIZE, start_cursor=cursor)
            if next_cursor and more:
                self.view.next_cursor = next_cursor
            if c:
                self.view.prev_cursor = cursor.reversed()
        else:
            groups, next_cursor, more = qry.order(-self.user_model.key).fetch_page(PAGE_SIZE, start_cursor=cursor)
            groups = list(reversed(groups))
            if next_cursor and more:
                self.view.prev_cursor = next_cursor
            self.view.next_cursor = cursor.reversed()

        def pager_url(p, cursor):
            params = OrderedDict()
            if q:
                params['q'] = q
            if p in ['prev']:
                params['p'] = p
            if cursor:
                params['c'] = cursor.urlsafe()
            return self.uri_for('admin-groups-list', **params)

        self.view.pager_url = pager_url
        self.view.q = q

        params = {
            "list_columns": [('name', 'Name'),
                             ('can_view', 'Can View'),
                             ('can_edit', 'Can Edit'),
                             ('can_administer', 'Can Adminster'),
                             ('can_upload', 'Can Upload'),
                             ],
            "groups": groups,
            "count": qry.count()
        }
        return self.render_template('admin_groups_list.html', **params)
    
    
class AdminGroupEditHandler(BaseHandler):
    def get_or_404(self, group_id):
        try:
            group = Group.get_by_id(long(group_id))
            if group:
                return group
        except ValueError:
            pass
        self.abort(404)
        
    def edit(self, group_id=None):
        if group_id:
            group = self.get_or_404(group_id)
        else:
            group = Group()     

        if self.request.POST:
            if self.form.validate():
                self.form.populate_obj(group)
                group.put()
                self.add_message("Changes saved!", 'success')
                import time
                time.sleep(1)
                #return self.redirect_to("admin-groups-list", group_id=group_id)
                return self.redirect('/admin/groups/')
            else:
                self.add_message("Could not save changes!", 'danger')
        else:
            self.form.process(obj=group)
            pass
                  
        for field in self.form:
            logging.info(field)
            

        params = {
            'group': group
        }     
        return self.render_template('admin_group_edit.html', **params)

    @webapp2.cached_property
    def form(self):
        f = forms.EditGroupForm(self)
        return f