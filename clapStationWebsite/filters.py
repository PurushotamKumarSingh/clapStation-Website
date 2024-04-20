import django_filters
from clapStationWebsite.models import(Event)


class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            'category':['exact',],
            }
