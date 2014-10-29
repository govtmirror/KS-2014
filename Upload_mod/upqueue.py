#
# Copyright 2014 National MEdiation Board.
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

from datetime import *
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

import pdf_miner_app_engine as pdf_miner

_INDEX_NAME = nmbcfg.med_prog_index
BUCKET_NAME = nmbcfg.med_prog_bucket

def to_unicode_or_bust(
	obj, encoding='utf-8'):
	if isinstance(obj, basestring):
		if not isinstance(obj, unicode):
			obj = unicode(obj, encoding)
	return obj

class UpQueueHandler(webapp2.RequestHandler):
	"""returns a JSON string"""


	def post(self):

		keys = self.request.arguments()

		myFields = []

		for arg in keys:

			if arg != "doctext" and arg!= "_csrf_token":
				value = self.request.get(arg)
				logging.info("upqueuehandler arg=%s" % arg)
				logging.info("value=%s" % value)
				newField = search.TextField(name=arg, value=value)
				myFields.append(newField)

		try:
			docdate = self.request.get('docdate')
			dtSplt = docdate.split('-')
			docyear = int(dtSplt[0])
			docmonth = int(dtSplt[1])
			docday = int(dtSplt[2])
			myDocDate = search.DateField(name='datedate', value=date(docyear, docmonth, docday))
			myFields.append(myDocDate)
		except:
			b = "why am I here?"

		myStamp = search.DateField(name='stamp', value=datetime.now().date())
		myFields.append(myStamp)


		doctext = self.request.get('doctext')
		filename1 = self.request.get('link')

		gcs_file = gcs.open(filename1)

		try:
			pdf = gcs_file.read()
			text = pdf_miner.pdf_to_text(pdf)
			text_uni = to_unicode_or_bust(text)
			text3 = text_uni.encode('utf-8')
			doctext_uni = to_unicode_or_bust(doctext)
			doctext3 = doctext_uni.encode('utf-8')
			doctext = doctext3 + text3
		except:
			a = "do something good"

		gcs_file.close()

		if len(doctext) > 983040:
			doctext = doctext[:983040]

		mydoctext = search.TextField(name='doctext', value=doctext)
		myFields.append(mydoctext)

		""" make a seach document"""
		award = search.Document(fields= myFields)

		""" put that search document in to the index """
		search.Index(name=_INDEX_NAME).put(award)