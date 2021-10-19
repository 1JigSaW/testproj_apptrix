from django.db import models
from django.conf import settings
import os
from PIL import Image
#from dating.utils.Mailer import Mailer

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

	class Meta:
		verbose_name = 'Участник'
		verbose_name_plural = 'Участники'

	def __str__(self):
		return f"{self.first_name} {self.last_name}"

	def save(self, *args, **kwargs):
		super().save()
		if not self.photo:
			return
		img = Image.open(self.photo.path)
		width, height = img.size
		watermark = Image.open(settings.WATERMARK_PATH)
		watermark.thumbnail((200, 200))
		mark_width, mark_height = watermark.size
		paste_mask = watermark.split()[3]
		x = width - mark_width - 5
		y = height - mark_height - 5
		img.paste(watermark, (x, y), paste_mask)
		img.save(self.photo.path)

class Match(models.Model):
	id_from = models.ForeignKey(Participant, on_delete=models.CASCADE, 
		related_name='id_from')
	id_to = models.ForeignKey(Participant, on_delete=models.CASCADE, 
		related_name='id_to')
	reciprocity = models.BooleanField(default=False)

	class Meta:
		constraints = [
            models.UniqueConstraint(
                fields=['id_from', 'id_to'],
                name='unique matches')
        ]
		verbose_name = 'Взаимность'
		verbose_name_plural = 'Взаимности'

	def __str__(self):
		return f"{self.id_from} + {self.id_to}"