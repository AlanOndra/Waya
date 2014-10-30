import sys, site, logging, traceback

sys.dont_write_bytecode = True

logging.basicConfig(stream=sys.stderr)

olddirs = list(sys.path)

dirs = [
	# set to site directory
	'/var/www/wsgi-bin/site'
]

for dir in dirs:
	site.addsitedir(dir)

newdirs = []
for item in list(sys.path):
	if item not in olddirs:
		newdirs.append(item)
		sys.path.remove(item)

sys.path[:0] = newdirs

from cms.fs import *
from cms.http import *
from cms.controller import *
from cms.cms import *

from app.model import *
from app.controller import *


def application(environ, start_response):
	try:
		return CMS.run(environ, start_response)

	except Exception as e:
		output = 'Error: ' + str(e)
		output += "\n" + traceback.format_exc()
		status = Status.ServerError
		headers = [
			('Content-Type', 'text/plain; charset=utf-8'),
			('Content-Length', str(len(output)))
		]
		start_response(status, headers)
		return [output]
