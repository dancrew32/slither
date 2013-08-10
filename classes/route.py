from classes.app import App

class Route:
	@staticmethod
	def init():
		path = App.get_url().path

		if path is '/':
			body = App.stache('test', {
					"title":  "Welcome to Slither",
					"output": "The path is: %s" % path,
					"post":   App.fetch('post', 'test_input', ''),
				});
		else:
			App.status = '404 Not Found'
			body       = '404. bummer.'
		return body
