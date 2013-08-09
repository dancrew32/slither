from cgi import escape as e

class App:
	headers = []
	status = "200 OK"
	request = {}


	@classmethod
	def bootstrap(cls, env, response):
		""" Bootstrap the application, send back headers and body """
		cls.handle_wsgi_reboot(env)
		cls.build_request_obj(env)

		body = cls.view('test', {
				"foo":  'bar',
				"post": e(cls.fetch('post', 'foo', '')),
			});

		cls.add_header('Content-type', 'text/html')
		cls.add_header('Content-Length', str(len(body)))
		response(cls.status, cls.headers)
		return [body]


	@classmethod
	def add_header(cls, key, value):
		""" Add a header to the request """
		cls.headers.append((key, value))


	@staticmethod
	def handle_wsgi_reboot(env):
		""" Handle refreshable wsgi server """
		if env['mod_wsgi.process_group'] != '':
			import signal, os
			os.kill(os.getpid(), signal.SIGINT)


	@staticmethod
	def view(file, data):
		""" Render a view in /views """
		import os
		from string import Template
		root_dir = os.path.dirname(__file__)
		v = Template(open(root_dir +'/../view/'+ file +'.html').read())
		return v.substitute(data)


	@classmethod
	def build_request_obj(cls, env):
		""" Parse server environment headers """
		from urlparse import urlparse, parse_qs
		try:
			request_body_size = int(env.get('CONTENT_LENGTH', 0))
		except (ValueError):
			request_body_size = 0
		cls.request = {
					"remote_ip":   env["REMOTE_ADDR"],
					"server_ip":   env["SERVER_ADDR"],
					"user_agent":  env["HTTP_USER_AGENT"],
					"host":        env["HTTP_HOST"],
					"method":      env["REQUEST_METHOD"],
					"query":       env["QUERY_STRING"],
					"uri":         env["REQUEST_URI"],
					"scheme":      env["wsgi.url_scheme"],
					"get":         {},
					"post":        {},
					"put":         {},
					"delete":      {},
				}
		cls.request["post"]   = parse_qs(env['wsgi.input'].read(request_body_size))
		cls.request["parsed"] = urlparse(cls.request["scheme"] + "://" + cls.request["host"] + cls.request["uri"]);
		cls.request["get"]    = parse_qs(cls.request.get('parsed').query)


	@classmethod
	def fetch(cls, method, param, default):
		""" Get a GET or POST parameter, fallback to default if it doesn't exist """
		return cls.request[method].get(param, [default])[0]


