from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    street_address = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length = 5000, blank=True, null=True)
    profile_pic = models.ImageField(default='default.jpg', upload_to= 'profile_pics', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.profile_pic.path)

        if img.height > 720 or img.width > 720:
            output_size = (720, 720)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)
            