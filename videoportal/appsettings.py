# Transloadit.com Settings

USE_TRANLOADIT = False

TRANSLOAD_AUTH_KEY = 'f8773dab00b4418d87163172f486a881'
TRANSLOAD_AUTH_SECRET = 'd662543861a93eff01c108f52dbe2e1a6cb2f9a2'

TRANSLOAD_TEMPLATE_VIDEO_ID = 'dd8ba41a71424910b9f8191021cb753f'
TRANSLOAD_TEMPLATE_AUDIO_ID = '2e3fb41355d84acf8a08eff53c8fe74c'
TRANSLOAD_TEMPLATE_VIDEO_AUDIO_ID = '2e3fb41355d84acf8a08eff53c8fe74c'

TRANSLOAD_NOTIFY_URL = 'http://owntube.pltzchn.de:8080/encodingdone/'

TRANSLOAD_MP4_ENCODE = 'encode_iphone'
TRANSLOAD_WEBM_ENCODE = 'encode_webm'
TRANSLOAD_MP3_ENCODE = 'encode_mp3'
TRANSLOAD_OGG_ENCODE = 'encode_ogg'
TRANSLOAD_THUMB_ENCODE = 'create_thumb'

ENCODING_OUTPUT_DIR = '/opt/owntube/owntube/media/'
ENCODING_VIDEO_BASE_URL = 'http://owntube.pltzchn.de/media/'

USE_BITTORRENT = True
BITTORRENT_TRACKER_ANNOUNCE_URL = 'udp://tracker.ccc.de:80'
BITTORRENT_FILES_DIR = '/opt/owntube/owntube/media/torrents/'
BITTORRENT_DOWNLOADS_DIR = '/home/transmission/downloads/'
BITTORRENT_FILES_BASE_URL = 'http://owntube.pltzchn.de/media/torrents/'

TRANSMISSION_HOST = 'localhost'
TRANSMISSION_PORT = 9091
