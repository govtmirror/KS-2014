


import webapp2
from webapp2_extras import json
from google.appengine.api import taskqueue
import cloudstorage as gcs
import logging

class RegexFilter(webapp2.RequestHandler):
  def post(self):
    qStr = self.request.get('query')
    rStr = self.request.get('regex')
    filename = self.request.get('filename')

    load = "This is a test file.  I love the NMB."

    filename1 = "/regex-results/" + filename
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    try:
      gcs_file = gcs.open(filename1,
                'w',
                content_type="text/plain",
                # options={'x-goog-acl': 'public-read'},
                retry_params=write_retry_params)
      gcs_file.write(load)
      gcs_file.close()
    except:
      self.redirect('/upload_failure.html')
