from rest_framework import serializers

from ehms.practitioners.models import Practitioner


class WardPractitionerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Practitioner
        fields = ['id', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.middle_name} {obj.last_name}"

