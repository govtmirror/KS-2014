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
import nmbcfg

_INDEX_NAME = nmbcfg.med_prog_index
_BUCKET_NAME = nmbcfg.med_prog_bucket

class KSSearch(webapp2.RequestHandler):
	"""returns a JSON string"""

	def post(self):

		""" angularjs sends data as a json string in the body of the post
		this turns that string in to a dict"""
		request_body_dict = json.decode(self.request.body)

		""" load up the variables, missing a key will cause an error"""
		queryString = request_body_dict.get('queryString')

		
		offset = request_body_dict.get('offset')
		

		limit = request_body_dict.get('limit')
		

		# offset = 0


		options=search.QueryOptions(
	        limit=limit,
	        offset=offset,
	        returned_fields=[
	        	'doctype',
	        	'boardtype',
	        	'boardnumber',
	        	'awardnumber', 
	        	'arbitrator',
	        	'carriers', 
	        	'unions', 
	        	'parties',
	        	'crafts',
	        	'link', 
	        	'docdate'
	        	],
	        snippeted_fields=['doctext'])

		query = search.Query(queryString, options)

		ksresults = search.Index(name=_INDEX_NAME).search(query)
		# ksresults = search.Index(name=_INDEX_NAME).search(queryString)

		result_set = []

		for doc in ksresults.results:
			temp_dict = {}
			for stuff in doc.fields:
				temp_dict[stuff.name] = stuff.value
			for morestuff in doc.expressions:
				temp_dict[morestuff.name] = morestuff.value
			result_set.append(temp_dict)

		num_of_matches = ksresults.number_found

		# alpha = ksresults.results.pop().doc_id
		# alpha = ksresults.results.pop().fields.pop().name
		# alpha = ksresults.results.pop().fields
		# alpha = str(ksresults.results)

		rspObj = {
			'rsp' : 'OK',
			'msg' : 'I love you Dean',
			'ksresults' : result_set,
			'num_of_matches' : num_of_matches,
			'bucket': _BUCKET_NAME
			# 'alpha' : alpha
			# 'ksresults' : [{'awardnumber':'12345','carriers':'Delta, Virgin'}, 'reject']
		}

		""" assemble and send the response """
		self.response.content_type = 'application/json'
		self.response.write(json.encode(rspObj))