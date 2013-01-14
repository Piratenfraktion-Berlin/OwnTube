# Transloadit.com Settings

# Should we use transloadit? Otherwise we will try ffmpeg
USE_TRANLOADIT = False

# Our transloadit auth key and secret
TRANSLOAD_AUTH_KEY = 'f8773dab00b4418d87163172f486a881'
TRANSLOAD_AUTH_SECRET = 'ae4f43f2be75a67a00334b0d578fc4a0037ee95f'
TRANSLOAD_TEMPLATE_VIDEO_ID = 'dd8ba41a71424910b9f8191021cb753f'
TRANSLOAD_TEMPLATE_AUDIO_ID = '2e3fb41355d84acf8a08eff53c8fe74c'
TRANSLOAD_TEMPLATE_VIDEO_AUDIO_ID = '52d9861b7683484d9eb8af5208c020e0'

# The URL Transloadit should notify if it was done (please remember the trailing slash)
TRANSLOAD_NOTIFY_URL = 'http://owntube.piratenfraktion-berlin.de/encodingdone/'

TRANSLOAD_MP4_ENCODE = 'encode_iphone'
TRANSLOAD_WEBM_ENCODE = 'encode_webm'
TRANSLOAD_MP3_ENCODE = 'encode_mp3'
TRANSLOAD_OGG_ENCODE = 'encode_ogg'
TRANSLOAD_THUMB_ENCODE = 'create_thumb'

ENCODING_OUTPUT_DIR = '/mnt/iscsi0/media/encoded/'
# How can we reach this files (public access is needed)
ENCODING_VIDEO_BASE_URL = 'http://owntube.piratenfraktion-berlin.de/media/encoded/'

USE_BITTORRENT = True
BITTORRENT_TRACKER_ANNOUNCE_URL = 'udp://tracker.publicbt.com:80'
BITTORRENT_TRACKER_BACKUP = 'udp://tracker.openbittorrent.com:80,udp://tracker.ccc.de:80,udp://tracker.istole.it:80'
BITTORRENT_FILES_DIR = '/opt/owntube/owntube/media/torrents/'
# Where does transmission expects the original files? (This directory must be writeable for both transmission and owntube!)
BITTORRENT_DOWNLOADS_DIR = '/opt/transmission-folder'
# What is the URL of the BITTORRENT_FILES_DIR?
BITTORRENT_FILES_BASE_URL = 'http://owntube.piratenfraktion-berlin.de/media/torrents/'

# Host and port Transmission is listining on (probably localhost
TRANSMISSION_HOST = '127.0.0.1'
TRANSMISSION_PORT = 9091

# Base-Dir vor Hotfolders

HOTFOLDER_BASE_DIR = '/mnt/iscsi0/videostore/robotron/'
HOTFOLDER_MOVE_TO_DIR = '/opt/owntube/owntube/media/raw/'
