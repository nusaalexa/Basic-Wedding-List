from django.db import IntegrityError
from rest_framework import serializers

from .models import Gift, GiftList


class GiftSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        try:
            if not validated_data:
                raise serializers.ValidationError("Invalid data")
            return super(GiftSerializer, self).create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError("Invalid data")

    def update(self, instance, validated_data):
        try:
            return super(GiftSerializer, self).update(instance, validated_data)
        except IntegrityError:
            raise serializers.ValidationError('Cannot update')

    class Meta:
        model = Gift
        fields = ('id', 'name', 'brand', 'price', 'purchased')
        read_only_fields = ('id', 'added_date')


class GiftListSerializer(serializers.ModelSerializer):
    gift = GiftSerializer(many=True)

    def create(self, validated_data):
        try:
            if not validated_data:
                raise serializers.ValidationError("Invalid data for gift list")
            validated_data['user'] = self.context['request'].user
            print(validated_data)
            return super(GiftListSerializer, self).create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError("Invalid data")

    def update(self, instance, validated_data):
        try:
            return super(GiftListSerializer, self).update(instance, validated_data)
        except IntegrityError:
            raise serializers.ValidationError('Cannot update')

    class Meta:
        model = GiftList
        fields = ('user', 'list_name', 'gift', 'created_date', 'updated_at')
        read_only_fields = ('user', 'created_date', 'updated_at')
