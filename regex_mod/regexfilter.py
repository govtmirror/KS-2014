


import webapp2
from webapp2_extras import json
from google.appengine.api import taskqueue
from google.appengine.api import search
import cloudstorage as gcs
import logging

class RegexFilter(webapp2.RequestHandler):
  def post(self):
    qStr = self.request.get('query')
    rStr = self.request.get('regex')
    filename = self.request.get('filename')

    MY_OFFSET = 1000

    load = "This is a test file.  I love the NMB."

    num_returned = 1

    ccc = search.Cursor()

    counter = 0

    while ccc != None:


      options=search.QueryOptions(
        limit=MY_OFFSET,
        cursor=ccc,
        returned_fields=[
          'link',
          'doctext'
        ]
      )
      query = search.Query(qStr, options)
      regexresults = search.Index(name="ksdocs2").search(query)

      num_returned = regexresults.number_found
      ccc = regexresults.cursor

      result_set = []
      for doc in regexresults.results:
        temp_str = ""
        for stuff in doc.fields:
          temp_str = temp_str + " " + stuff.value
        result_set.append(temp_str)


      counter += 1

      filename1 = "/regex-results/" + filename + str(counter)
      write_retry_params = gcs.RetryParams(backoff_factor=1.1)

      gcs_file = gcs.open(filename1,
                'w',
                content_type="text/plain",
                # options={'x-goog-acl': 'public-read'},
                retry_params=write_retry_params)
      for docStr in result_set:
        yoStr = docStr.encode('ascii','ignore') 
        gcs_file.write(yoStr)

      gcs_file.close()

