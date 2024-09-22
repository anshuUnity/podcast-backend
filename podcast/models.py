from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Podcast(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    host = models.CharField(max_length=255)
    cover_image = models.URLField(blank=True)  # URL field to store the image URL
    audio_file = models.URLField(blank=True)   # URL field to store the audio file URL
    category = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    publish_date = models.DateField(auto_now_add=True)
    duration = models.DurationField()
    is_explicit = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='podcasts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
