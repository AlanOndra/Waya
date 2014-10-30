# -*- coding: utf-8 -*-

from os.path import abspath, join
import pickle
from datetime import *
from http.cookies import *
from cms.fs import *


class Status:
	OK            = '200 OK'
	Created       = '201 Created'
	Moved         = '301 Moved Permanently'
	Found         = '302 Found'
	Redirect      = '307 Temporary Redirect'
	PermRedirect  = '308 Permanent Redirect'
	BadRequest    = '400 Bad Request'
	Unauthorized  = '401 Unauthorized'
	Forbidden     = '403 Forbidden'
	NotFound      = '404 Not Found'
	NotAllowed    = '405 Method Not Allowed'
	NotAcceptable = '406 Not Acceptable'
	Teapot        = '418 I\'m a teapot'
	ServerError   = '500 Internal Server Error'
	Unavailable   = '503 Service Unavailable'


class ContentType:
	BMP   = 'image/x-windows-bmp'
	CSS   = 'text/css'
	CSV   = 'text/csv'
	GIF   = 'image/gif'
	HTML  = 'text/html'
	JS    = 'application/javascript'
	JPEG  = 'image/jpeg'
	JSON  = 'application/json'
	MPEG  = 'video/mpeg'
	MP3   = 'audio/mpeg'
	MP4   = 'video/mp4'
	OGG   = 'audio/ogg'
	PDF   = 'application/pdf'
	TXT   = 'text/plain'
	PNG   = 'image/png'
	QT    = 'video/quicktime'
	RDF   = 'application/rdf+xml'
	RSS   = 'application/rss+xml'
	SOAP  = 'application/soap+xml'
	SVG   = 'image/svg+xml'
	VORB  = 'audio/vorbis'
	Wave  = 'audio/vnd.wave'
	WMV   = 'video/x-ms-wmv'
	XHTML = 'application/xhtml+xml'
	XML   = 'application/xml'
	ZIP   = 'application/zip'


class Request:
	def __init__(self, env, cookies, path='/', root='/', matches=[], get={}, post={}):
		self.env = env
		self.path = path or '/'
		self.root = root or '/'
		self.get = get or {}
		self.post = post or {}
		self.cookies = cookies


class Response:
	def __init__(self, status=Status.OK, headers={}, content='', cookies=None):
		self.status = status or Status.OK
		self.headers = headers or {}
		self.content = content or ''

		if cookies is not None:
			self.cookies = cookies
		else:
			self.cookies = None


class Session:
	key      = ''
	filename = None
	data     = {}

	def get(key, default=None):
		if key in Session.data.keys():
			return Session.data[key]
		else:
			return default

	def set(key, value):
		if key in Session.data.keys():
			if value is None:
				data = dict(Session.data)
				del data[key]
				Sssion.data = data
			else:
				Session.data[key] = value
			return True
		else:
			return False

	def load():
		if Session.filename is None:
			Session.filename = abspath(join(FS.sessdir, Session.key + '.session'))

		try:
			f = open(Session.filename, 'r')
			Session.data = pickle.load(f)
			return True
		except:
			return False

	def save():
		if Session.filename is None:
			Session.filename = abspath(join(FS.sessdir, Session.key + '.session'))

		try:
			f = open(Session.filename, 'w')
			pickle.dump(Session.data, f)
			return True
		except:
			return False
