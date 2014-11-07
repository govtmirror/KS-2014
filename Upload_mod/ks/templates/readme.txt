*********************************************************************
This document describes how to combine all of the polymer files
into one single file to reduce page load times.

Since the resulting file cannot be located in the static directory
(we don't want direct access to it), we'll also need to change some 
of the paths.
*********************************************************************


1) Run the vulcanize command like this: vulcanize -o build.html upload.html
2) Wrap the entire resulting upload.html content with the Jina "raw" tags like so:
{% raw %}
...
{% endraw %}

3) Change all references to the path:
bower_components/...
to
/ks/static/bower_components/..

4)Change all refereence to the pah:
img/...
to
/ks/st


Note:  doing a replace of all "../static" with "../ks/static" seems to work.