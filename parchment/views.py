"""
Views for CRUD operations (mostly filtering
and retrieving) for the Parchment model. Creating
is tricky since we don't want a special page
for creating new Parchments since that is usually
done by the admin panel but a JSON view for
doing it from a native app is not a bad idea yet.
"""
import typing

from parchment.models import Parchment

from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, View


class ParchmentListView(ListView):
    """
    A simple generic view that returns and renders
    a template of Parchments ordered by timestamp.
    """
    paginate_by = 10
    model = Parchment
    context_object_name = 'parchments'
    template_name = 'parchment/list.html'
    queryset = Parchment.objects.filter(draft=False)


class ParchmentDetailView(DetailView):
    """
    Gets all the data about a particular
    parchment singled out by its slug field.
    TODO test slug vs primary key lookups.
    """
    model = Parchment
    context_object_name = 'parchment'
    template_name = 'parchment/detail.html'
    queryset = Parchment.objects.filter(draft=False)


class ParchmentByTagListView(ListView):
    """
    Group Parchments by a single tag.
    Support for multiple tags is something
    that I'll have to look into but that'd
    require a different way of parsing the
    tags. Then there will be the issue of.
    """
    paginate_by = 10
    model = Parchment
    context_object_name = 'parchments'
    template_name = 'parchment/list.html'

    def get_queryset(self):
        return Parchment.objects.filter(tags__in=[self.kwargs['tag']])


class ParchmentSearchAPIView(View):
    """
    Filters Parchment by querying case
    insensitive titles and tags. Full
    body text search will be too expensive.
    """

    @staticmethod
    def get(request):

        query = request.GET.get('query')

        if query:

            # serialize data into proper
            # JSON format by using an internal
            # custom serializer per model.

            data: typing.List[typing.Dict[str, str]] = []

            # make query
            parchments = Parchment.objects.filter(
                Q(title__icontains=query) |
                Q(tags__in=query.split(' '))
            )

            # insert serialized model into data array
            for parchment in parchments:
                data.append(parchment.serialize())

            return JsonResponse({
                'results': data
            })

        else:
            # no query passed
            return JsonResponse({
                'error': 'Query not provided.'
            }, 401)
