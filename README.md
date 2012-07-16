OwnTube
=======

OwnTube is your personal video portal based on Django

Features
--------

* Encode Videos using ffmpeg or transloadit.com
* Uses Bittorrent and Transmission to distribute original files (Using original Bittorrent python libs and transmissionrpc)
* Task Managment using djangotasks
* Uses Projekktor or audio.js to show videos in a modern way
* Upload files using AJAX
* Schedule live streaming events with the livestream app
* Static pages app for, well, static pages

Status
------

The status could be desciped as early beta. It is feature complete but not yet tested in a real world scenario and the code isn't that elegant as it could be

Requierments
------------

I would recommend to use virtualenv to make a runtime enviroment for the django site package. Also you would need a settings.py (TODO: Make a generator for this) and you schuld install all dependencies as in dependencies.txt most of them should be available in pip. Also you need to install the transloadit Python "API" which you can find [here](https://github.com/joestump/python-transloadit)

Support
-------

Not available but if you have any issues use the issue tracker of github or contact pbrechler@piratenfraktion-berlin.de

Fork?
-----

Yes, please!
