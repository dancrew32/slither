import os, sys
sys.path.append(os.path.dirname(__file__))
from classes.app import App

def application(env, response):
	return App.bootstrap(env, response)
