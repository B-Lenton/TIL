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
        related_name = "profile"
    )
    image = ImageField(upload_to='profiles')
    
    # # added this morning (10/11/21) using stack overflow answer on phone - Django 1.4 Creating an Edit User Profile Account Settings View:
    # birthdate = models.DateField(blank=False)
    # gender = models.CharField(max_length=1, choices=GENDER_CHOICE, null=True)

    # def __unicode__(self):
    #     # TODO: stopped here...
    #     pass

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
    