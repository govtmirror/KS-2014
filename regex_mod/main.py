#
# Copyright 2016 National MEdiation Board.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import webapp2
from webapp2_extras import json
from google.appengine.api import taskqueue
import logging
from regexfilter import *

"""handlers for client redirects"""
class RegexHandler(webapp2.RequestHandler):
  def get(self):
  	# self.redirect("ks/search.html")
    self.redirect("ks/index.html")

class RegexSearch(webapp2.RequestHandler):
  def post(self):
    qStr = self.request.get('querystr')
    rStr = self.request.get('regexstr')
    filename = self.request.get('filename')

    yoparams = {
      'query': qStr,
      'regex': rStr,
      'filename':filename
    }
    taskurl = "/regexfilter"
    stat = "Bad"
    try:
      taskqueue.add(url=taskurl, params=yoparams)
      stat = "OK"
    except Exception:
      logging.error(e)


    rspObj = {
      'query': qStr,
      'regex': rStr,
      'filename':filename,
      'stat': stat
    }

    # assemble and send the response 
    self.response.content_type = 'application/json'
    self.response.write(json.encode(rspObj))





app = webapp2.WSGIApplication(
    [('/', RegexHandler),
    ('/regex', RegexSearch),
    ('/regexfilter', RegexFilter)
    ],
    debug=True)