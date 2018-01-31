from rest_framework import generics

from sample.models import Movement
from sample.models import MovementAnnex
from sample.models import Tag
from sample.serializers import DetailMovementSerializer
from sample.serializers import MovementAnnexSerializer
from sample.serializers import MovementSerializer
from sample.serializers import TagSerializer


class TagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class MovementAnnexListView(generics.ListCreateAPIView):
    queryset = MovementAnnex.objects.all()
    serializer_class = MovementAnnexSerializer


class MovementAnnexDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovementAnnex.objects.all()
    serializer_class = MovementAnnexSerializer


class MovementListView(generics.ListCreateAPIView):
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer


class MovementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movement.objects.all()
    serializer_class = DetailMovementSerializer
