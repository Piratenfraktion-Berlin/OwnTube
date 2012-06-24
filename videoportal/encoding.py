from videoportal.models import Video
import appsettings as settings

from pytranscode.ffmpeg import *
from pytranscode.presets import *
from pytranscode.runner import *

def encode_media(path, name, video, outputdir, kind):
    logfile = settings.ENCODING_OUTPUT_DIR + 'encodinglog.txt'
    outfile = outputdir + name + '.mp4'
    
   
    
    # Create the command line
    cl = ffmpeg(path, outfile, logfile, IPOD_MP4_VIDEO, IPOD_MP4_AUDIO).build_command_line()
    
    # setup the command thread
    run = FuncThread(runTranscode, cl, logfile)
    
    # Set up the tracking thread
    track = FuncThread(runTracker, logfile)
    
    
    
    # Start run and tracker
    run.start()
    track.start()
    
    video.mp4URL = settings.ENCODING_VIDEO_BASE_URL + name + '.mp4'
    video.encodingDone = True
    video.save()