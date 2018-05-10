``django-service-autodiscovery`` is a simple Django app that helps to auto
discover and orchestrate services in a development environment. With this app
it is possible to automatically initialize additional services that your website
might need such as Redis, Celery, Postgres, etc.

The service auto-discovery will auto-spawn services only during development. It
tries to find those services in your local installation and can even attempt to
use Docker if the server is not locally installed.

During production, it provides hooks and signals to broadcast and handle
connection with those services.


Installation
============

Install with ``pip3 install django-services-autodiscovery`` and add the
"services_autodiscovery" application to the INSTALLED_APPS setting of your
Django project.


Supported services
==================

Redis
-----

Tell me more ;)


Celery
------

Yeah!


Postgres
--------

Not yet...
