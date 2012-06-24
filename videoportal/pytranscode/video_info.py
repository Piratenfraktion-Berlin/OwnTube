"""
    Video Information Class
    =======================
    
    Uses ffmpeg to grab video and audio info from a specified file and stores
    these values internally
    
    Usage:
    ------
    >>> this = VideoObject('video.avi')
    >>> this.printinfo()
    
    VIDEO INFO
    ==========
    Filename:       video.avi
    Video Length:   244.84 seconds
    Video Codec:    msmpeg4v2
    Video Size:     368x208
    Frame Rate:     25.0 fps
    Video Bitrate:  782 kb/s
    
    AUDIO INFO:
    ===========
    Audio Codec:    mp3
    Sampling Freq:  44100 Hz
    Audio Bitrate:  96 kb/s

"""


from subprocess import Popen, PIPE, STDOUT
import re

class VideoObject:
    def __init__(self, infile):
        self.source = infile
        self.output = None
        
        self.length = None  #
        self.video_codec = None #
        self.video_size = None #
        self.frame_rate = None #
        self.video_bitrate = None #

        self.audio_codec = None #
        self.audio_freq = None #
        self.audio_bitrate = None
        
        if self.source:
            # Get the output of the ffmpeg call
            self.grab_source()
            
            # Run through the various regex functions to get the info needed
            self.get_framerate()
            self.get_length()
            self.get_size()
            self.get_video_codec()
            self.get_video_bitrate()
            self.get_audio_codec()
            self.get_audio_freq()
            self.get_audio_bitrate()
            
        
    def grab_source(self):
        commandline = 'ffmpeg -i ' + self.source
        outcode = Popen(commandline, stdout=PIPE, stderr=PIPE)
        
        self.output = outcode.stderr.read()
        
    def get_framerate(self):
        output = self.output
        ex = r' \d+.\d+ tb\(r\)'
        n = re.compile(ex)
        found = n.findall(output)
        rate = 0.0
        if found:
            rate = float(found[0].replace('tb(r)', '').replace(' ', ''))
        
        self.frame_rate = rate

    def get_length(self):
        output = self.output
        ex = r'Duration: \d+:\d+:\d+.\d+'
        n = re.compile(ex)
        found = n.search(output)
        hours, min, sec = 0.0, 0.0, 0.0
        if found:
            clean = found.group(0).replace('Duration: ', '').replace(' ', '')
            ar = clean.split(':')
            hours = float(ar[0])
            min = float(ar[1])
            sec = float(ar[2])
    
        self.length = self.get_seconds(hours, min, sec)
    
    def get_seconds(self, hr, min, sec):
        secs = ((hr * 60) * 60) + (min * 60) + sec
        return  secs
    
    def get_size(self):
        output = self.output
        ex = r'\d+x\d+'
        n = re.compile(ex)
        found = n.findall(output)
        
        if found:
            self.video_size = found[0]
    
    def get_video_codec(self):
        output = self.output
        ex = r'Video: \w+'
        n = re.compile(ex)
        found = n.findall(output)
        
        if found:
            self.video_codec = found[0].replace('Video: ', '').replace(' ', '')
            
    def get_video_bitrate(self):
        output = self.output
        ex = r'\d+ kb/s'
        n = re.compile(ex)
        found = n.findall(output)
        
        if found:
            self.video_bitrate = found[0].replace('kb/s', '').replace(' ', '')
            
    def get_audio_codec(self):
        output = self.output
        ex = r'Audio: \w+'
        n = re.compile(ex)
        found = n.findall(output)
        
        if found:
            self.audio_codec = found[0].replace('Audio: ', '').replace(' ', '')
            
    def get_audio_freq(self):
        output = self.output
        ex = r'\d+ Hz'
        n = re.compile(ex)
        found = n.findall(output)
        
        if found:
            self.audio_freq = found[0].replace(' Hz', '').replace(' ', '')
        
    def get_audio_bitrate(self):
        output = self.output
        ex = r'\d+ kb/s'
        n = re.compile(ex)
        found = n.findall(output)
        
        if found:
            self.audio_bitrate = found[1].replace('kb/s', '').replace(' ', '')
            
    def printinfo(self):
        print "\nVIDEO INFO"
        print "=========="
        print "Filename: \t" + self.source
        print "Video Length: \t" + str(self.length) + " seconds"
        print "Video Codec: \t" + self.video_codec 
        print "Video Size: \t" + self.video_size  
        print "Frame Rate: \t" + str(self.frame_rate) + " fps"
        print "Video Bitrate: \t" + self.video_bitrate  + " kb/s"
        
        print "\nAUDIO INFO:"
        print "==========="
        print "Audio Codec: \t" + self.audio_codec  
        print "Sampling Freq: \t" + self.audio_freq  + " Hz"
        print "Audio Bitrate: \t" + self.audio_bitrate  + " kb/s"
    
    