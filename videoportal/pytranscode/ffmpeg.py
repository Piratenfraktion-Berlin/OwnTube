"""
    FFMPEG Management Class
    =======================
    
    Can be used to build a command line to run ffmpeg for various
    settings

    
    Usage:
    ------
    
    >>> from ffmpeg import *
    >>> f = ffmpeg( 'video.avi',
                    'test.flv',
                    'logfile.txt',
                    {'format':'flv', 'size':'320x240'},
                    {'freq':'22050', 'rate':'32'})
    >>> f.build_command_line()
    'ffmpeg  -loglevel quiet -i video.avi  -s 320x240 -f flv -ar 22050 -ab 32 test.flv 2> logfile.txt'
    
    You can get the various options from the classes param_options.keys() and advanced_options.keys()
    lists
    
    See: http://ffmpeg.org/ffmpeg-doc.html for defintions of the options
"""

# not used, but may do later
vcodec_options = ['libx264', 'mpeg4', 'flv']
format_options = ['flv', 'mp4']

class audio_settings:
    """
        Handles audio settings and build command line for these
    """
    
    def __init__(self, options = {}):
        self.options = options
        
        self.param_options = {
            'aframes':'-aframes',
            'freq': '-ar',
            'rate': '-ab',
            'channels': '-ac',
            'acodec': '-acodec',
            'stream_filter': '-absf',
            'format': '-f',
        }
        
    def command(self):
        cmd = ''
        for option in self.options.keys():
            if (option in self.param_options.keys()) or (option in self.advanced_options.keys()):
                pair = ' %s %s' % (self.param_options[option], self.options[option])
                cmd += pair
        
        return cmd
        
class video_settings:
    """
        Handles video settings and builds command line for these
    """
    
    def __init__(self, options = {}):
        self.options = options
        
        self.param_options = {
            'bitrate': '-b',
            'vframes': '-vframes',
            'fps': '-r',
            'size': '-s',
            'aspect': '-aspect',
            'croptop': '-croptop',
            'cropbottom': '-cropbottom',
            'cropleft': '-cropleft',
            'cropright': '-cropright',
            'padcolor': '-padcolor',
            'padtop': '-padtop',
            'padbottom': '-padbottom',
            'padleft': '-padleft',
            'padcolor': '-padcolor',
            'tolerance': '-bt',
            'maxrate': '-maxrate',
            'minrate': '-minrate',
            'bufsize': '-bufsize',
            'vcodec': '-vcodec',
            'passn': '-pass',
            'format': '-f',
            'deinterlace': '-deinterlace',
            'vf': '-vf',
        }
        
        self.advanced_options = {
            'pix_fmt':'-pix_fmt', 
            'g': '-g', 
            'intra':'-intra',            
            'vdt': '-vdt',            
            'qscale':'-qscale',            
            'qmin': '-qmin',
            'qmax': '-qmax',            
            'qdiff': '-qdiff',            
            'qblur':'-qblur',           
            'qcomp': '-qcomp',               
            'lmin':'-lmin',          
            'lmax':'-lmax', 
            'mblmin':'-mblmin',            
            'mblmax': '-mblmax',
            'rc_init_cplx': '-rc_init_cplx',
            'b_qfactor':'-b_qfactor',            
            'i_qfactor': '-i_qfactor',           
            'b_qoffset':'-b_qoffset',             
            'i_qoffset':'-i_qoffset',         
            'rc_eq':'-rc_eq',           
            'rc_override':'-rc_override',            
            'me_method method':'-me_method method',            
            'dct_algo':'-dct_algo',             
            'idct_algo':'-idct_algo',                
            'er':'-er',                
            'ec':'-ec',              
            'bf':'-bf',              
            'mbd':'-mbd',           
            '4mv':'-4mv',               
            'part':'-part',                  
            'strict':'-strict',               
            'aic':'-aic',              
            'umv':'-umv',          
            'deinterlace':'-deinterlace',            
            'ilme':'-ilme',             
            'psnr':'-psnr',
            'top':'-top',            
            'dc':'-dc',            
            'vtag':'-vtag',                       
            'vbsf':'-vbsf',
            'coder':'-coder',
            'flags':'-flags',
            'flags2':'-flags2',
            'subq':'-subq',
            'me_range':'-me_range',
            'keyint_min':'-keyint_min',
            'sc_threshold':'-sc_threshold',
            'i_qfactor':'-i_qfactor',
            'b_strategy':'-b_strategy',
            'bidir_refine':'-bidir_refine',
            'refs':'-refs',
            'deblockalpha':'-deblockalpha',
            'deblockbeta':'-deblockbeta',
            'nr':'-nr',
        }
    
    def command(self):
        cmd = ''
        for option in self.options.keys():
            if option in self.param_options.keys():
                pair = ' %s %s' % (self.param_options[option], self.options[option])
                cmd += pair
                
            if option in self.advanced_options.keys():
                pair = ' %s %s' % (self.advanced_options[option], self.options[option])
                cmd += pair
            
        
        return cmd
        

class ffmpeg:
    """
        Combines the above two classes to build an ffmpeg command that can
        be run by the shell.
    """
    def __init__(self, input_file, output_file, logfile, video_options, audio_options):
        self.options = {'-i': input_file,
                        }
        
        self.video_options = video_options
        self.audio_options = audio_options
        self.output_file = output_file
        self.logfile = logfile
    
    def build_command_line(self):
        v = video_settings(self.video_options)
        a = audio_settings(self.audio_options)
        
        avcmd = ' %s%s' % (v.command(), a.command())
        
        defcmd = ''
        for option in self.options.keys():
            if self.options[option]:
                pair = ' %s %s' % (option, self.options[option])
                defcmd += pair
        
        #TODO: The path to ffmpeg may not be clear, set this as a global?
        cmd = 'ffmpeg %s%s %s 2> %s' % (defcmd, avcmd, self.output_file, self.logfile)
        
        return cmd
        
