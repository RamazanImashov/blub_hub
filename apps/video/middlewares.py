from .models import Video


class VideoViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method == 'GET' and 'videos/' in request.path:
            video_id = int(request.path.split('/')[4])

            video = Video.objects.get(pk=video_id)
            video.views += 1
            video.save()

        return response
