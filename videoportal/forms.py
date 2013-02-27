from django.forms import ModelForm
from django import forms

from videoportal.models import Video
from videoportal.models import Comment

class VideoForm(ModelForm):
    ''' Used for the uploading form '''

    class Meta:
        model = Video
        fields = ('title', 'date', 'description', 'channel', 
            'linkURL', 'kind', 'tags', 'originalFile')

class CommentForm(ModelForm):
    ''' Used for the comments '''
    class Meta:
        model = Comment
        exclude = ["ip","moderated","video"]
