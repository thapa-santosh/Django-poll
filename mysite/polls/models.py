from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date Published')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username