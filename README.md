OwnTube
=======

OwnTube is your personal video portal based on Django.

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

The status could be described as early beta. It is feature complete but not yet tested in a real world scenario and the code isn't as elegant as it could be.

Requirements
------------

I would recommend to use virtualenv to create a runtime enviroment for the django site package. Also you would need a settings.py (TODO: Make a generator for this) and you should install all dependencies as in dependencies.txt. Most of them should be available in pip. Also you need to install the transloadit Python "API" which you can find [here](https://github.com/joestump/python-transloadit).
But there is a (https://github.com/Piratenfraktion-Berlin/OwnTube/wiki/Installation-and-Setup)[HowTo]

Support
-------

Not available, but if you have any issues use the github issue tracker or contact pbrechler@piratenfraktion-berlin.de

Fork?
-----

Yes, please!

License
-------

BSD 2-clause (See LICENSE file)
