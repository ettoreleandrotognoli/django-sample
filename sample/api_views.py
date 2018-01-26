from rest_framework import generics

from sample.models import Movement
from sample.serializers import MovementSerializer


class MovementListView(generics.ListCreateAPIView):
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer


class MovementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer
