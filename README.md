# Slither

## Linux Setup
```bash
sudo aptitude install libapache2-mod-wsgi
```

## Python Setup
```bash
# install pip if you need it
curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python 
# lets us use mustache templates
pip install pystache
```

## Apache VirtualHost Setup
Learn more about [WSGI setup](http://webpython.codepoint.net/wsgi_application_interface).
```.htaccess
WSGIDaemonProcess site.com threads=1 # remove in prod
WSGIProcessGroup site.com # remove in prod
<VirtualHost *:80>
	ServerName site.com
	WSGIScriptAlias / /var/host/site/wsgi.py
</VirtualHost>
```
