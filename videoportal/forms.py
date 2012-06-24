from django.forms import ModelForm

from videoportal.models import Video
from videoportal.models import Comment

class VideoForm(ModelForm):
''' Used for the uplaading form '''
    class Meta:
        model = Video
        exclude = ["slug","mp4URL","mp4Size","flashURL","flashSize","webmURL","webmSize","mp3URL","mp3Size","oggURL","oggSize","ogvURL","ogvSize","duration","videoThumbURL","published","encodingDone","assemblyid","torrentURL"]

class CommentForm(ModelForm):
''' Used for the comments '''
    class Meta:
        model = Comment
        exclude = ["ip","moderated","video"]