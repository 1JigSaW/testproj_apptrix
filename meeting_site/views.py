from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from .serializers import RegistrationSerializer, MatchSerializer
from .models import Participant, Match, GENDER_CHOICES

class RegisterView(generics.CreateAPIView):
	serializer_class = RegistrationSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save()

class MatchView(APIView):
	serializer_class = MatchSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, id):
		matching = get_object_or_404(Participant, id=id)
		context = {
			"request": self.request,
			"matching": matching
		}
		serializer = RegistrationSerializer(matching, context=context, many=False)
		return Response(serializer.data)

	def post(self, request, id):
		matching = get_object_or_404(Participant, id=id)
		context = {
			"request": self.request,
			"matching": matching
		}
		serializer = MatchSerializer(data=request.data, context=context)
		if serializer.is_valid():
			match = serializer.save(Match, id_from=request.id_from, id_to=matching)
			if match.mark:
				check_matching(match)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def patch(self, request, id):
		matching = get_object_or_404(
			Match, user=request.id_from, matching_id=id
		)
		context = {
			"request": self.request
		}
		serializer = MatchSerializer(matching, data=request.data, context=context, partial=True)
		if serializer.is_valid():
			match = serializer.save()
			if match.reciprocity:
				check_matching(match)
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def check_matching(match):
	    user = match.id_from
	    match = match.id_to
	    if not Match.objects.filter(id_from=match, id_to=user, reciprocity=True).exists():
	        return

	    return send_match(user, match), send_match(match, user)


	def send_match(id_from, id_to):
	    subject = 'У вас есть пара!'
	    message = f'Вы понравились {id_to.first_name}!  Почта участника: {id_to.email}'
	    admin_email = settings.EMAIL
	    user_email = [id_from.email]
	    return send_mail(subject, message, admin_email, user_email)

class ParticipantFilter(filters.FilterSet):
    gender = filters.ChoiceFilter(choices=GENDER_CHOICES)
    first_name = filters.CharFilter(field_name='first_name')
    last_name = filters.CharFilter(field_name='last_name')

    class Meta:
        model = Participant
        fields = ['gender', 'first_name', 'last_name']

class ParticipantListView(generics.ListAPIView):
    queryset = Participant.objects.all()
    serializer_class = RegistrationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ParticipantFilter
