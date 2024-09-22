from django.contrib import admin
from .models import Podcast, Tag

# Register the Tag model with default admin interface
admin.site.register(Tag)

# Define a custom admin interface for the Podcast model
@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'host', 'publish_date', 'is_explicit')
    list_filter = ('is_explicit', 'publish_date', 'tags', 'language')
    search_fields = ('title', 'host', 'description')
    date_hierarchy = 'publish_date'
    ordering = ('-publish_date',)
    filter_horizontal = ('tags',)

    # This defines which fields are displayed in the form
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'host', 'category', 'language', 'duration', 'is_explicit', 'tags')
        }),
        ('Media', {
            'fields': ('cover_image', 'audio_file'),
        })
    )
