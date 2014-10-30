# -*- coding: utf-8 -*-

import os.path
import urllib.parse
from http.cookies import *

from . import *

from cms.fs import *
from cms.http import *
from cms.controller import *


def byte2str(data):
	if isinstance(data, dict):
		new = {}
		for key in data.keys():
			nk = key.decode('utf-8')
			new[nk] = byte2str(data.get(key, []))
			if len(new[nk]) <= 1:
				new[nk] = new[nk][0] if len(new[nk]) > 0 else None
		return new
	elif isinstance(data, list):
		new = []
		for value in data:
			new.append(value.decode('utf-8'))
		return str(new)


class CMS:
	environ = None
	path = '/'
	docroot = '/'
	get = {}
	post = {}
	session = {}
	cookies = None
	sessionid = ''
	status = Status.NotFound
	headers = {'Content-Type': ContentType.PlainText + '; charset=utf-8'}
	output = ''

	def run(environ, start_response):
		CMS.environ = environ

		CMS.cookies = SimpleCookie(environ.get('HTTP_COOKIE', ''))

		CMS.path = environ['PATH_INFO']

		docroot = environ['REQUEST_URI']

		fi = (docroot.find(CMS.path))

		CMS.docroot = (docroot[:fi] + '/') if fi >= 1 else docroot

		CMS.get = byte2str(urllib.parse.parse_qs(environ['QUERY_STRING']))

		CMS.post = byte2str(
			urllib.parse.parse_qs(
				environ['wsgi.input'].read(
					int(environ.get('CONTENT_LENGTH', '0'))
				)
			)
		)

		response = None

		i = ControllerSet.find(CMS.path)

		if i is False:
			try:
				CMS.status = Status.NotFound
				f = open(os.path.join(FS.errdir, '404.html'), 'r')
				CMS.output = f.read()
				CMS.headers = {
					'Content-Type': ContentType.HTML + '; charset=utf-8',
					'Content-Length': str(len(CMS.output))
				}
			except Exception:
				CMS.output = 'File Not Found'
				CMS.headers = {
					'Content-Type': ContentType.PlainText + '; charset=utf-8',
					'Content-Length': str(len(CMS.output))
				}
		else:
			req = Request(
				env=CMS.environ,
				path=CMS.path,
				root=CMS.docroot,
				get=CMS.get,
				post=CMS.post,
				cookies=CMS.cookies
			)

			response = ControllerSet.execute(i, req)

			if isinstance(response, Response):
				CMS.status = response.status or Status.OK
				CMS.headers.update(response.headers)
				CMS.output = response.content
			elif response is False:
				try:
					CMS.status = Status.NotFound
					f = open(os.path.join(FS.errdir, '404.html'), 'r')
					CMS.output = f.read()
					CMS.headers = {
						'Content-Type': ContentType.HTML + '; charset=utf-8'
					}
				except Exception:
					CMS.output = 'File Not Found'
					CMS.headers = {
						'Content-Type': ContentType.PlainText + '; charset=utf-8'
					}
			else:
				CMS.status = Status.ServerError
				CMS.output = str(response)

		CMS.headers['Content-Length'] = str(len(CMS.output))

		headers = []

		for key in CMS.headers.keys():
			headers.append((key, CMS.headers[key]))

		if isinstance(response, Response) and (response.cookies is not None):
			headers.extend(
				('Set-Cookie', morsel.OutputString())
					for morsel in response.cookies.values()
			)

		start_response(CMS.status, headers)

		return CMS.output
