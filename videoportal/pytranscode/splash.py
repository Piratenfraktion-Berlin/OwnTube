"""
    Snapshot Grabber
    ================
    
    Uses ffmpeg to grab a series of snapshots of a video file for thumbnail
    and/or splash use
    
    Outputs a series of images with the filenames set using:
    input filename + snapshot location (seconds) + jpg
    
    The filenames are appended to the opject 'images' list
    
    Usage:
    ------
    >>> this = SplashImages(input_file='video.avi', count=5)
    >>> this.get_images()
    >>> print this.images
    

"""


from video_info import *
import re

class SplashImages:
    def __init__(self, input_file=None, count=None):
        self.input_file = input_file
        self.count = count
        self.images = []
        
    def get_images(self):
        if self.input_file:
            if self.count:
                split = self.get_info()
                split2 = split
                for a in xrange(self.count):
                    self.run_command(split2)
                    split2 += split
        
    def get_info(self):
        info = VideoObject(self.input_file)    
        length = info.length
        
        # we increment the count + 1 in order to never hit the EOF
        split = info.length / (self.count + 1)
        
        return split
        
    def run_command(self, loc):
        output_file = self.input_file
        
        output_file = output_file + '.' + str(int(loc)) + '.jpg'
        
        commandline = 'ffmpeg -y -i %s -f mjpeg -ss %s -vframes 1 -an %s' % (self.input_file, loc, output_file)
        outcode = Popen(commandline, stdout=PIPE, stderr=PIPE)
        
        self.output = outcode.stderr.read()
        self.images.append(output_file)
        

#Uncomment to test
#this = SplashImages(input_file='video.avi', count=5)
#this.get_images()
#print this.images
