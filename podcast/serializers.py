from rest_framework import serializers
from .models import Podcast, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class PodcastSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)  # Nested serializer for tags
    tags_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, write_only=True, source='tags'
    )

    class Meta:
        model = Podcast
        fields = [
            'id', 
            'title', 
            'description', 
            'host', 
            'cover_image', 
            'category', 
            'language', 
            'publish_date', 
            'duration', 
            'audio_file', 
            'is_explicit', 
            'tags', 
            'tags_ids',  # To allow adding tags via their IDs
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['total_plays', 'created_at', 'updated_at']

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        podcast = Podcast.objects.create(**validated_data)
        podcast.tags.set(tags)
        return podcast

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)
        if tags:
            instance.tags.set(tags)
        return instance
    