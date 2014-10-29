import os
import webapp2
import logging
from google.appengine.ext.webapp import template

from bp_includes.lib.decorators import user_permission_required
from bp_includes.lib.basehandler import BaseHandler
            
"""handlers for client redirects"""
class UploadHandler(BaseHandler):
  
  @user_permission_required("can_view") #this decorator also forces a call to the login page if no user is registered
  def get(self):

    params = {}
    return self.render_template('build.html', **params)

    
class polymerTest(BaseHandler):
  
  def get(self):

      self.redirect("static/polymerTest.html")

