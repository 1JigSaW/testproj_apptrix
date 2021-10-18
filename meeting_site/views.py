from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import RegistrationSerializer
from .models import Participant


class RegisterView(generics.CreateAPIView):
	serializer_class = RegistrationSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save()


