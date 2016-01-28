


import webapp2
from webapp2_extras import json
from google.appengine.api import taskqueue
from google.appengine.api import search
import cloudstorage as gcs
import logging
import re

class RegexFilter(webapp2.RequestHandler):
  def post(self):
    qStr = self.request.get('query')
    rStr = self.request.get('regex')
    filename = self.request.get('filename')

    ccc = search.Cursor()
    counter = 0
    hits = 0

    filename1 = "/regex-results/" + filename #+ str(counter)
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)

    gcs_file = gcs.open(filename1,
                'w',
                content_type="text/plain",
                # options={'x-goog-acl': 'public-read'},
                retry_params=write_retry_params)
    gcs_file.write("Query = " + rStr.encode('ascii','ignore') + "\n\n")

    
    while ccc != None:

      logging.info("starting another batch")
      options=search.QueryOptions(
        limit=100,
        cursor=ccc,
        returned_fields=[
          'link',
          'doctext'
        ]
      )
      query = search.Query(qStr, options)
      regexresults = search.Index(name="ksdocs2").search(query)

      ccc = regexresults.cursor

      for doc in regexresults.results:
        counter += 1
        candidateLink = doc.fields[0].value.encode('ascii','ignore')
        candidateStr = doc.fields[1].value.encode('ascii','ignore') 
         
        candidateId = doc.doc_id.encode('ascii','ignore') 

        # nospaces=candidateStr.replace(' ','')
        # nospacesorlinefeeds = nospaces.replace('\n','')
        # modified = re.findall(rStr,nospacesorlinefeeds)

        modified = re.findall(rStr,candidateStr)

        if len(modified) > 0:
          hits += 1
          charlieStr = ""
          for charlie in modified:
            charlieStr = charlieStr + "    " + charlie + "\n"
          yoStr = "found regex, " + candidateId + ", " + candidateLink + "\n" + charlieStr
          gcs_file.write(yoStr)
          logging.info("found one! " + candidateLink)


    gcs_file.write("\n\nfound " + str(hits) + " out of " + str(counter))
    gcs_file.close()
    logging.info("finished")

