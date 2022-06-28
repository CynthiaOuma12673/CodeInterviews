from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    name = models.CharField(max_length=100)
    title =models.CharField(max_length=50)
    question = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title
    
    def create_question(self):
        self.save()
        
    def delete_question(self):
        self.delete()
        
    def update_question(self):
        self.update()
        
    @classmethod
    def find_question(cls, question_id):
        return cls.objects.filter(id=question_id)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=400, blank=True)
    name = models.CharField(blank=True,max_length=120)
    profile_pic = models.ImageField(blank=True, upload_to='profile_pic')
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, related_name='members', blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()