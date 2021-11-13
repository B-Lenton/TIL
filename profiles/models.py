from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField

# Create your models here.
# every user needs a profile attached to it...
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name = "profile",
        null=True, 
        blank=True,
    )
    image = ImageField(upload_to='profiles')
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=400)

    # class Meta:
    #     model = User
    #     fields = ['username', 'image', 'first_name', 'last_name', 'email', 'password']

    
# every profile should be called self.user.username (use its username)...
    def __str__(self):
        return self.user.username

# every time the user is saved, execute this function...
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Create a new Profile object when a Django User is created
    if created:
        Profile.objects.create(user=instance)


# class Account(Profile):
    