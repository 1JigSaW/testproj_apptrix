from rest_framework import serializers
from meeting_site.models import Participant, Match


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = ['id', 'photo', 'gender', 'first_name', 'last_name', 'email', 'password']

class MatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = ['id_from', 'id_to', 'reciprocity']