from django.db import models

GENDER_CHOICES = (
	('M', 'Male'),
	('F', 'Female'),
)

class Participant(models.Model):
	photo = models.ImageField(upload_to='static/photos')
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(max_length=254)
	password = models.CharField(max_length=30)

	def __str__(self):
		return f"{self.first_name} {self.last_name}"

	class Meta:
		verbose_name = 'Участник'
		verbose_name_plural = 'Участники'

