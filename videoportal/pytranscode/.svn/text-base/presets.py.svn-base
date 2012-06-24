"""

    Presets for the ffmpeg manager
    ==============================
    
    Import these presets for quick access to transcode settings

"""

# YouTube Quality
# ===============

STANDARD_FLV_VIDEO = {'size':'420x340',
                      'vcodec':'flv',
                      'format':'flv',
                      'bitrate':'4000'}

STANDARD_FLV_AUDIO = {'rate':'256k',
                      'freq':'44100',
                      'acodec':'libmp3lame'}

                        
# IPOD Video
# ==========
IPOD_MP4_VIDEO = {'format':'mp4',
                  'vcodec':'mpeg4',
                  'qmin':'3',
                  'qmax':'5',
                  'g':'300',
                  'size':'480x320',
                  'bitrate':'700k'}

IPOD_MP4_AUDIO = {'acodec':'libfaac',
                  'rate':'128k'}


                     
                        
# HD Video (780p)
# ===============
HD_H264_AUDIO = {'acodec':'libfaac',
                 'rate':'96k',
                 'freq':'44100'}
           
HD_H264_VIDEO = {'vcodec':'libx264',
                 'level':'41',
                 'crf':'25',
                 'bufsize': '20000k',
                 'maxrate': '25000k',
                 'g':'30',
                 'fps':'20',
                 'size':'1280x720',
                 'coder':'1',
                 'flags': '+loop -cmp +chroma -partitions +parti4x4+partp8x8+partb8x8',
                 'flags2': '+dct8x8+bpyramid',
                 'me_method': 'umh',
                 'subq':'7',
                 'me_range':'16',
                 'keyint_min':'25',
                 'sc_threshold':'40',
                 'i_qfactor':'0.71',
                 'rc_eq': "'blurCplx^(1-qComp)'",
                 'bf':'16',
                 'b_strategy':'1',
                 'bidir_refine': '1',
                 'refs': '6',
                 'deblockalpha':'0',
                 'deblockbeta':'0',                 
                 }


# High Quality FLV
# ================
HQ_FLV_AUDIO = {'acodec':'libmp3lame',
                'rate': '128k',
                'channels':'2',
                'freq':'44100'}

HQ_FLV_VIDEO = {'format':'flv',
                'deinterlace':'',
                'nr': '500',
                'size':'640x420',
                'fps':'30',
                'bitrate':'270k',
                'me_range':'25',
                'i_qfactor':'0.9',
                'qmin':'12',
                'qmax':'12',
                'g':'500'}
