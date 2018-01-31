from rest_framework import serializers

from sample.models import Movement
from sample.models import MovementAnnex
from sample.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class MovementSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField('name', many=True, queryset=Tag.objects.all())

    class Meta:
        model = Movement
        fields = '__all__'


class MovementAnnexSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementAnnex
        fields = '__all__'


class NestedMovementAnnexSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementAnnex
        exclude = ('movement',)


class DetailMovementSerializer(MovementSerializer):
    annexes = NestedMovementAnnexSerializer(
        'annexes',
        many=True,
        read_only=True
    )
