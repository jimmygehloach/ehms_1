from rest_framework import serializers

from ehms.addresses.models import Region, District, Town, Postcode


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']


class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = ['id', 'name']


class PostcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postcode
        fields = ['id', 'name']
