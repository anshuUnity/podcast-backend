from django import forms
from .models import Podcast

class PodcastForm(forms.ModelForm):
    cover_image = forms.URLField(widget=forms.HiddenInput(), required=False)
    audio_file = forms.URLField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Podcast
        fields = [
            'title',
            'description',
            'host',
            'category',
            'language',
            'duration',
            'is_explicit',
            'tags',
            'cover_image',
            'audio_file',
        ]
