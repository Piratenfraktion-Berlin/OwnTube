from ffmpeg import *
from presets import *
from runner import *

def testrun():
    infile = 'video.avi'
    outfile = 'result.flv'
    logfile = 'logthis.txt'
    
    # Create the command line
    cl = ffmpeg(infile, outfile, logfile, HQ_FLV_VIDEO, HQ_FLV_AUDIO).build_command_line()
    
    # setup the command thread
    run = FuncThread(runTranscode, cl, logfile)
    
    # Set up the tracking thread
    track = FuncThread(runTracker, logfile)
    
    # Start run and tracker
    run.start()
    track.start()
    
testrun()