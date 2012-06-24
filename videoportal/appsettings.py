# Setting used by the videoportal app

# Should we use transloadit? Otherwise we will try ffmpeg
USE_TRANLOADIT = False

# Our transloadit auth key and secret
TRANSLOAD_AUTH_KEY = 'aksdaskldjaklsdjalksdj'
TRANSLOAD_AUTH_SECRET = 'lkjasdnalsdnlaksndllkj'

# The template IDs you use to render your videos a example can be found in assemblies.txt
TRANSLOAD_TEMPLATE_VIDEO_ID = 'dd8ba41a71424910b9f8191021cb753f'
TRANSLOAD_TEMPLATE_AUDIO_ID = '2e3fb41355d84acf8a08eff53c8fe74c'
TRANSLOAD_TEMPLATE_VIDEO_AUDIO_ID = '2e3fb41355d84acf8a08eff53c8fe74c'

# The URL Transloadit should notify if it was done (please remember the trailing slash)
TRANSLOAD_NOTIFY_URL = 'http://owntube.yourdomain.com/encodingdone/'

# The names of the encoding steps in transloadit (can be found in the assemblies.txt)
TRANSLOAD_MP4_ENCODE = 'encode_iphone'
TRANSLOAD_WEBM_ENCODE = 'encode_webm'
TRANSLOAD_MP3_ENCODE = 'encode_mp3'
TRANSLOAD_OGG_ENCODE = 'encode_ogg'
TRANSLOAD_THUMB_ENCODE = 'create_thumb'

# The directories for ffmpeg to work with
# Where should ffmpeg put the files?
ENCODING_OUTPUT_DIR = '/opt/owntube/owntube/media/'
# How can we reach this files (public access is needed)
ENCODING_VIDEO_BASE_URL = 'http://owntube.pltzchn.de/media/'

# Bittorrent settings
# Should we use Bittorrent?
USE_BITTORRENT = True
# The tracker(s) to use
BITTORRENT_TRACKER_ANNOUNCE_URL = 'udp://tracker.ccc.de:80'
# Where should we place the .torrent files?
BITTORRENT_FILES_DIR = '/opt/owntube/owntube/media/torrents/'
# Where does transmission expects the original files? (This directory must be writeable for both transmission and owntube!)
BITTORRENT_DOWNLOADS_DIR = '/home/transmission/downloads/'
# What is the URL of the BITTORRENT_FILES_DIR?
BITTORRENT_FILES_BASE_URL = 'http://owntube.pltzchn.de/media/torrents/'

# Host and port Transmission is listining on (probably localhost
TRANSMISSION_HOST = 'localhost'
TRANSMISSION_PORT = 9091
