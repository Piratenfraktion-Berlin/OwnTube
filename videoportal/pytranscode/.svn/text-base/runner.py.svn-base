#!/usr/bin/env python

"""
    FFMPEG Tracker
    ==============
    
    Tracks an ffmpeg process and communicates the percentage status of when it is complete
    uses threading and an output file to track progress.
    
    Usage:
    ------
    code = FuncThread(runTranscode, Command_Line, 'read2.txt')
    track = FuncThread(runTracker, 'read2.txt')
    
    code.start()
    track.start()
"""

import os
from subprocess import Popen, PIPE, STDOUT
import sys
import re
import time
import threading

def get_framerate(output):
    ex = r' \d+.\d+ tb\(r\)'
    n = re.compile(ex)
    found = n.search(output)
    rate = 0.0
    if found:
        rate = float(found.group(0).replace('tb(r)', '').replace(' ', ''))
    
    return rate
    
def get_length(output):
    ex = r'Duration: \d+:\d+:\d+.\d+'
    n = re.compile(ex)
    found = n.search(output)
    hours, min, sec = 0.0, 0.0, 0.0
    if found:
        clean = found.group(0).replace('Duration: ', '')
        ar = clean.split(':')
        hours = float(ar[0])
        min = float(ar[1])
        sec = float(ar[2])
    
    return hours, min, sec

def get_seconds(hr, min, sec):
    secs = ((hr * 60) * 60) + (min * 60) + sec
    return  secs

def calculate_total_frames(hr, min, sec, frate):
    secs = get_seconds(hr, min, sec)
    frames = frate * secs
    
    return frames

def get_current_frame(output):
    ex = r'frame=\s+\d+'
    n = re.compile(ex)
    found = n.findall(output)
    rate = 0.0
    
    if found:
        rate = float(found[len(found) - 1].replace('frame=', '').replace(' ', ''))
    
    return rate

def get_current_time(output):
    ex = r'time=\d+.\d+'
    n = re.compile(ex)
    found = n.findall(output)
    time = 0.0
    
    if found:
        time = float(found[len(found) - 1].replace('time=', '').replace(' ', ''))
    
    return time

def check_tick(outfile):
    perc = 0.0

    try:
        f = open(outfile, 'rb')
        out = f.read()
        f.close()
        
        if out.lower().find('error') == -1:
        
            rate = get_framerate(out)
            hr, min, sec = get_length(out)
            frames = calculate_total_frames(hr, min, sec, rate)
            current_frame = get_current_frame(out)
            current_time = get_current_time(out)
            total_time_seconds = get_seconds(hr, min, sec)
            
            perc = (current_time / total_time_seconds) * 100
            perc = int(round(perc))
        else:
            return -1
        
    except:
        pass
    
    return perc

def get_final_output(outfile):
    f = open(outfile, 'rb')
    out = f.read()
    f.close()
    
    return out


# Thready things
class FuncThread(threading.Thread):
    """
        subclass of Thread in order to pass values to out transcode an tracking threads
    """
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)

def runTranscode(commandline, outfile):
    # Use the ffmpeg class here to build commands from options
    outcode = Popen(commandline, shell=True)
    
    while outcode.poll() == None:
        pass
    
    if outcode.poll() == 0:
        # All is well
        pass
    else:
        #Report error
        print get_final_output(outfile)
        
        # Signal other thread (output may not contain error message, so we
        # add one manually just in case)
        
        f = open(outfile, 'a')
        f.write('error code:' + (str(outcode.poll())))
        f.close()
        

def runTracker(outfile):
    a = 0
    while a <= 100:
        time.sleep(1)
        a = check_tick(outfile)
        
            
        if a == 100:
            print "%i%%" % a
            print "Transcode complete!"
            #TODO: Cleanup!
            break
        
        if a == -1:
            print "There was a problem"
            #TODO: Cleanup!
            
            break
        
        print "%i%%" % a

