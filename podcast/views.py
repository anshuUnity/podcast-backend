from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PodcastForm
from django.http import JsonResponse
from .util import upload_audio, upload_image
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .models import Podcast
from .serializers import PodcastSerializer

def create_podcast(request):
    if request.method == 'POST':
        form = PodcastForm(request.POST)
        if form.is_valid():
            podcast = form.save(commit=False)

            # Retrieve the uploaded file URLs from the form data
            cover_image_url = form.cleaned_data.get('cover_image')
            audio_file_url = form.cleaned_data.get('audio_file')

            # Assign the URLs to the podcast instance
            podcast.cover_image = cover_image_url
            podcast.audio_file = audio_file_url

            # Save the podcast instance
            podcast.save()

            # Save the many-to-many relationships (tags)
            form.save_m2m()

            # Return a success response
            return JsonResponse({"message": "Podcast created successfully!"}, status=201)

        else:
            # If form is invalid, return the errors
            return JsonResponse({"errors": form.errors}, status=400)

    else:
        form = PodcastForm()

    return render(request, 'create_podcast.html', {'form': form})


def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        file_type = request.POST.get('file_type')

        if not file or not file_type:
            return JsonResponse({"error": "No file or file type provided."}, status=400)

        try:
            if file_type == 'image':
                url = upload_image(file)
            elif file_type == 'audio':
                url = upload_audio(file)
            else:
                return JsonResponse({"error": "Invalid file type."}, status=400)

            return JsonResponse({"url": url}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)

class PodcastListView(generics.ListAPIView):
    queryset = Podcast.objects.all().order_by('-publish_date')
    serializer_class = PodcastSerializer
