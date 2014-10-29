#
# Copyright 2013 National MEdiation Board.
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

from datetime import datetime
import webapp2
from webapp2_extras import json
from google.appengine.api import search

from google.appengine.api import taskqueue

from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
import nmbcfg
import cloudstorage as gcs
import time
import logging

from bp_includes.lib.decorators import user_permission_required
from bp_includes.lib.basehandler import BaseHandler


_INDEX_NAME = nmbcfg.med_prog_index
BUCKET_NAME = nmbcfg.med_prog_bucket

class PostAwardHandler(BaseHandler):
  """returns a JSON string"""

  @user_permission_required("can_upload")  
  def post(self):

    fileitem = self.request.POST['file']
    load = fileitem.value
    mimetype = str(fileitem.type)

    ts = int(time.time())
    filename1 = "/" + BUCKET_NAME + '/' + str(ts) + str(fileitem.filename)
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)

    try:
      gcs_file = gcs.open(filename1,
                'w',
                content_type=mimetype,
                # options={'x-goog-acl': 'public-read'},
                retry_params=write_retry_params)
      gcs_file.write(load)
      gcs_file.close()
    except:
      self.redirect('/upload_failure.html')

    keys = self.request.arguments()

    myFields = {}

    for arg in keys:
      if arg != "file":
        logging.info("found and arg = " + arg)
        value = self.request.get(arg)
        myFields[arg] = value

    myFields['link'] = filename1
    myFields['odoc'] = fileitem.filename

    taskqueue.add(
      url='/upqueue', 
      params=myFields
      )

    self.redirect('/')


# class PostPebHandler(webapp2.RequestHandler):
#   """returns a JSON string"""

#   def post(self):

#     fileitem = self.request.POST['file']
#     load = fileitem.value
#     mimetype = str(fileitem.type)

#     ts = int(time.time())
#     filename1 = "/" + BUCKET_NAME + '/' + str(ts) + str(fileitem.filename)
#     write_retry_params = gcs.RetryParams(backoff_factor=1.1)

#     try:
#       gcs_file = gcs.open(filename1,
#                 'w',
#                 content_type=mimetype,
#                 # options={'x-goog-acl': 'public-read'},
#                 retry_params=write_retry_params)
#       gcs_file.write(load)
#       gcs_file.close()
#     except:
#       self.redirect('/upload_failure.html')

#     """ angularjs sends data as a json string in the body of the post
#     this turns that string in to a dict"""
#     request_body_dict = json.decode(self.request.body)

#     """ load up the variables, missing a key will cause an error"""
#     pebnumber = request_body_dict.get('pebnumber')
#     carriers = request_body_dict.get('carriers')
#     unions = request_body_dict.get('unions')
#     parties = request_body_dict.get('parties')
#     crafts = request_body_dict.get('crafts')
#     docdate = request_body_dict.get('docdate')
#     link = request_body_dict.get('link')
#     doctext = request_body_dict.get('doctext')

#     """ make a seach document"""
#     peb = search.Document(
#       fields=[search.AtomField(name='doctype', value="peb"),
#               search.TextField(name='pebnumber', value=pebnumber),
#               search.TextField(name='carriers', value=carriers),
#               search.TextField(name='unions', value=unions),
#               search.TextField(name='parties', value=parties),
#               search.TextField(name='crafts', value=crafts),
#               search.TextField(name='docdate', value=docdate),
#               search.TextField(name='link', value=link),
#               search.DateField(name='stamp', value=datetime.now().date()),
#               search.TextField(name='doctext', value=doctext)])

#     """ put that search document in to the index """

#     search.Index(name=_INDEX_NAME).put(peb)



#     """ assemble and send the response """
#     self.response.content_type = 'application/json'
#     self.response.write(json.encode({'rsp': 'OK', 'msg': 'saved a PEB'} ))


# class PostContractHandler(webapp2.RequestHandler):
#   """returns a JSON string"""

#   def post(self):

#     fileitem = self.request.POST['file']
#     load = fileitem.value
#     mimetype = str(fileitem.type)

#     ts = int(time.time())
#     filename1 = "/" + BUCKET_NAME + '/' + str(ts) + str(fileitem.filename)
#     write_retry_params = gcs.RetryParams(backoff_factor=1.1)

#     try:
#       gcs_file = gcs.open(filename1,
#                 'w',
#                 content_type=mimetype,
#                 # options={'x-goog-acl': 'public-read'},
#                 retry_params=write_retry_params)
#       gcs_file.write(load)
#       gcs_file.close()
#     except:
#       self.redirect('/upload_failure.html')

#     """ angularjs sends data as a json string in the body of the post
#     this turns that string in to a dict"""
#     request_body_dict = json.decode(self.request.body)

#     """ load up the variables, missing a key will cause an error"""
#     carriers = request_body_dict.get('carriers')
#     unions = request_body_dict.get('unions')
#     parties = request_body_dict.get('parties')
#     crafts = request_body_dict.get('crafts')
#     docdate = request_body_dict.get('docdate')
#     enddate = request_body_dict.get('enddate')
#     link = request_body_dict.get('link')
#     doctext = request_body_dict.get('doctext')

#     """ make a seach document"""
#     contract = search.Document(
#       fields=[search.AtomField(name='doctype', value="contract"),
#               search.TextField(name='carriers', value=carriers),
#               search.TextField(name='unions', value=unions),
#               search.TextField(name='parties', value=parties),
#               search.TextField(name='crafts', value=crafts),
#               search.TextField(name='docdate', value=docdate),
#               search.TextField(name='enddate', value=enddate),
#               search.TextField(name='link', value=link),
#               search.DateField(name='stamp', value=datetime.now().date()),
#               search.TextField(name='doctext', value=doctext)])

#     """ put that search document in to the index """
#     search.Index(name=_INDEX_NAME).put(contract)

#     """ assemble and send the response """
#     self.response.content_type = 'application/json'
#     self.response.write(json.encode({'rsp': 'OK', 'msg': 'saved a Contract'} ))


# class PostDecisionHandler(webapp2.RequestHandler):
#   """returns a JSON string"""

#   def post(self):

#     fileitem = self.request.POST['file']
#     load = fileitem.value
#     mimetype = str(fileitem.type)

#     ts = int(time.time())
#     filename1 = "/" + BUCKET_NAME + '/' + str(ts) + str(fileitem.filename)
#     write_retry_params = gcs.RetryParams(backoff_factor=1.1)

#     try:
#       gcs_file = gcs.open(filename1,
#                 'w',
#                 content_type=mimetype,
#                 # options={'x-goog-acl': 'public-read'},
#                 retry_params=write_retry_params)
#       gcs_file.write(load)
#       gcs_file.close()
#     except:
#       self.redirect('/upload_failure.html')

#     """ angularjs sends data as a json string in the body of the post
#     this turns that string in to a dict"""
#     request_body_dict = json.decode(self.request.body)

#     """ load up the variables, missing a key will cause an error"""
#     volnumber = request_body_dict.get('volnumber')
#     decisionnumber = request_body_dict.get('decisionnumber')
#     citepage = request_body_dict.get('citepage')
#     carriers = request_body_dict.get('carriers')
#     unions = request_body_dict.get('unions')
#     parties = request_body_dict.get('parties')
#     crafts = request_body_dict.get('crafts')
#     docdate = request_body_dict.get('docdate')
#     link = request_body_dict.get('link')
#     doctext = request_body_dict.get('doctext')

#     """ make a seach document"""
#     decision = search.Document(
#       fields=[search.AtomField(name='doctype', value="decision"),
#               search.TextField(name='volnumber', value=volnumber),
#               search.TextField(name='decisionnumber', value=decisionnumber),
#               search.TextField(name='citepage', value=citepage),
#               search.TextField(name='carriers', value=carriers),
#               search.TextField(name='unions', value=unions),
#               search.TextField(name='parties', value=parties),
#               search.TextField(name='crafts', value=crafts),
#               search.TextField(name='docdate', value=docdate),
#               search.TextField(name='link', value=link),
#               search.DateField(name='stamp', value=datetime.now().date()),
#               search.TextField(name='doctext', value=doctext)])

#     """ put that search document in to the index """
#     search.Index(name=_INDEX_NAME).put(decision)

#     """ assemble and send the response """
#     self.response.content_type = 'application/json'
#     self.response.write(json.encode({'rsp': 'OK', 'msg': 'saved a Decision'} ))


# class PostAnnualreportHandler(webapp2.RequestHandler):
#   """returns a JSON string"""

#   def post(self):

#     fileitem = self.request.POST['file']
#     load = fileitem.value
#     mimetype = str(fileitem.type)

#     ts = int(time.time())
#     filename1 = "/" + BUCKET_NAME + '/' + str(ts) + str(fileitem.filename)
#     write_retry_params = gcs.RetryParams(backoff_factor=1.1)

#     try:
#       gcs_file = gcs.open(filename1,
#                 'w',
#                 content_type=mimetype,
#                 # options={'x-goog-acl': 'public-read'},
#                 retry_params=write_retry_params)
#       gcs_file.write(load)
#       gcs_file.close()
#     except:
#       self.redirect('/upload_failure.html')

#     """ angularjs sends data as a json string in the body of the post
#     this turns that string in to a dict"""
#     request_body_dict = json.decode(self.request.body)

#     """ load up the variables, missing a key will cause an error"""
#     year = request_body_dict.get('year')
#     link = request_body_dict.get('link')
#     doctext = request_body_dict.get('doctext')

#     """ make a seach document"""
#     annualreport = search.Document(
#       fields=[search.AtomField(name='doctype', value="annualreport"),
#               search.TextField(name='year', value=year),
#               search.TextField(name='link', value=link),
#               search.DateField(name='stamp', value=datetime.now().date()),
#               search.TextField(name='doctext', value=doctext)])

#     """ put that search document in to the index """
#     search.Index(name=_INDEX_NAME).put(annualreport)

#     """ assemble and send the response """
#     self.response.content_type = 'application/json'
#     self.response.write(json.encode({'rsp': 'OK', 'msg': 'saved an Annual Report'} ))


# class PostOtherHandler(webapp2.RequestHandler):
#   """returns a JSON string"""

#   def post(self):

#     fileitem = self.request.POST['file']
#     load = fileitem.value
#     mimetype = str(fileitem.type)

#     ts = int(time.time())
#     filename1 = "/" + BUCKET_NAME + '/' + str(ts) + str(fileitem.filename)
#     write_retry_params = gcs.RetryParams(backoff_factor=1.1)

#     try:
#       gcs_file = gcs.open(filename1,
#                 'w',
#                 content_type=mimetype,
#                 # options={'x-goog-acl': 'public-read'},
#                 retry_params=write_retry_params)
#       gcs_file.write(load)
#       gcs_file.close()
#     except:
#       self.redirect('/upload_failure.html')

#     """ angularjs sends data as a json string in the body of the post
#     this turns that string in to a dict"""
#     request_body_dict = json.decode(self.request.body)

#     """ load up the variables, missing a key will cause an error"""
#     docdate = request_body_dict.get('docdate')
#     link = request_body_dict.get('link')
#     doctext = request_body_dict.get('doctext')

#     """ make a seach document"""
#     annualreport = search.Document(
#       fields=[search.AtomField(name='doctype', value="other"),
#               search.TextField(name='docdate', value=docdate),
#               search.TextField(name='link', value=link),
#               search.DateField(name='stamp', value=datetime.now().date()),
#               search.TextField(name='doctext', value=doctext)])

#     """ put that search document in to the index """
#     search.Index(name=_INDEX_NAME).put(annualreport)

#     """ assemble and send the response """
#     self.response.content_type = 'application/json'
#     self.response.write(json.encode({'rsp': 'OK', 'msg': 'saved an Other'} ))