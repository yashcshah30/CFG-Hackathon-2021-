from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    CHOICES = (
        ('J','J'),
        ('S','S'),
        ('M','M')
    )

    # is_student = models.BooleanField(default = False)
    # is_mentor = models.BooleanField(default= False)
    # is_judge = models.BooleanField(default= False)
    role = models.CharField(choices=CHOICES, max_length=1, default = 'S')
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.username

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.TextField()

    def __str__(self):
        return self.user.username

class Team(models.Model):
    CHOICES = (
        ('1','Identify'),
        ('2','Investigate'),
        ('3','Ideate'),
        ('4','Implement'),
        ('5','Inform'),
        ('6','Completed')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number_of_members = models.IntegerField()
    member1 = models.CharField(max_length=20)
    member2 = models.CharField(max_length=20, null = True , blank = True)
    member3 = models.CharField(max_length=20, null = True , blank = True)
    member4 = models.CharField(max_length=20, null = True , blank = True)
    member5 = models.CharField(max_length=20, null = True , blank = True)
    mentor = models.OneToOneField(Mentor, null = True, on_delete=models.CASCADE, blank = True,related_name = 'teams')
    phase = models.CharField(choices=CHOICES, max_length = 1, default = '1')
    final_submission = models.URLField(null = True)
    phase1_score = models.IntegerField(default=0)
    phase2_score = models.IntegerField(default=0)
    phase3_score = models.IntegerField(default=0)
    phase4_score = models.IntegerField(default=0)
    phase5_score = models.IntegerField(default=0)
    total_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Phase(models.Model):
    name = models.CharField(max_length=20)

class Question(models.Model):
    question = models.TextField()
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)

class Document(models.Model):
    document = models.ImageField(upload_to='uploads/')
    phase = models.ForeignKey(Phase,on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class Answer(models.Model):
    ques = models.ForeignKey(Question, on_delete=models.CASCADE)
    ans = models.TextField(default="")
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time']

    def _str_(self):
        return self.user.username