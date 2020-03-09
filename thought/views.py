import json
import typing
import datetime

from thought.models import Thought
from authtoken.models import Authtoken

from django.http import JsonResponse
from django.views.generic import ListView, View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


def think(body: str) -> typing.Dict[str, str]:
    return Thought.objects.create(body=body).serialize()


class ThoughtListView(ListView):
    queryset = Thought.objects.all()
    context_object_name = 'thoughts'
    template_name = 'thought/list.html'


class ThoughtListAPIView(View):

    @staticmethod
    def get(request):
        thoughts = [thought.serialize() for thought in Thought.objects.all()]
        return JsonResponse(thoughts, safe=False)


class ThoughtCreateAPIView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def post(request):

        token = request.POST.get('token')
        body = request.POST.get('body')

        if not (token and body):
            data = request.body.decode()
            try:
                data = json.loads(data)
                token = data['token']
                body = data['body']
            except Exception as e:
                return JsonResponse({'error': 'Invalid data provided.', 'traceback': str(e)}, status=400)

        print(token, body)

        if token and body:
            try:
                token = Authtoken.objects.get(key__exact=token)
                if token.valid:
                    return JsonResponse(think(body), status=201)
                else:

                    current = Authtoken.objects.last().timestamp.date()
                    delta: datetime.timedelta = token.timestamp.date() - current
                    days = delta.days

                    return JsonResponse({'error': f'Token {token} expired {days} ago.'}, status=400)

            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Token invalid.'}, status=400)
        else:
            return JsonResponse({'error': 'Token or body not provided.'}, status=400)


class ThoughtDeleteAPIView(View):
    """
    API view that only accepts a POST
    request with two pieces of data -
    the authtoken key and thought_id that
    has to be marked for deletion.
    """

    @staticmethod
    def post(request):

        token = request.POST.get('token')
        thought_pk = request.POST.get('thought_pk')

        if token and thought_pk:

            try:

                token = Authtoken.objects.get(key__exact=token)

                if token.valid:

                    try:
                        Thought.objects.get(pk=thought_pk).delete()
                        return JsonResponse({'deleted': True})
                    except ObjectDoesNotExist:
                        return JsonResponse({'error': 'Thought does not exist.'}, status=400)

                else:

                    # calculate number of days since
                    # last token expired and new one
                    # was generated for error message
                    current = Authtoken.objects.get(valid=True).timestamp.date()
                    delta: datetime.timedelta = current - token.timestamp.date()
                    days = delta.days

                    return JsonResponse({
                        'error': f'Token ending with {token.key[-5:]} expired {days} days ago.'
                     }, status=400)

            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Token invalid.'}, status=400)

        else:
            return JsonResponse({'error': 'Token or thought id not provided.'}, status=400)
