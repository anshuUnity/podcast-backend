import os
import uuid
from azure.storage.blob import BlobServiceClient, ContentSettings
from django.conf import settings
from django.core.exceptions import ValidationError
import logging

def upload_file_to_azure(file, container_name, content_type):
    try:
        # Initialize the BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_CONNECTION_STRING)

        # Create a unique filename using uuid
        filename = f"{uuid.uuid4()}_{file.name}"
        
        # Get a blob client for the container and blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

        # Set content settings based on the file type
        content_settings = ContentSettings(content_type=content_type)

        # Upload the file
        blob_client.upload_blob(file, overwrite=True, content_settings=content_settings)

        # Get the URL of the uploaded file
        blob_url = blob_client.url

        return blob_url

    except Exception as e:
        # Log the exception and raise a validation error
        # Assuming logging is set up correctly
        logging.exception("Failed to upload file to Azure Blob Storage")
        raise ValidationError(f"Failed to upload file: {str(e)}")

# Example usage for image file
def upload_image(file):
    if not file.content_type.startswith('image/'):
        raise ValidationError("File is not an image.")
    
    return upload_file_to_azure(file, container_name='podcast-covers', content_type=file.content_type)

# Example usage for audio file
def upload_audio(file):
    if not file.content_type.startswith('audio/'):
        raise ValidationError("File is not an audio file.")
    
    return upload_file_to_azure(file, container_name='podcast-audio', content_type=file.content_type)
