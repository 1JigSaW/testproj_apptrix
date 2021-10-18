from rest_framework import serializers
from meeting_site.models import Participant


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = ['photo', 'gender', 'first_name', 'last_name', 'email', 'password']

