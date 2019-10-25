from django.db import models
from django.contrib.auth.models import User
from accounts.models import CustomUser
from datetime import datetime

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=200)
    weblink = models.CharField(max_length=200)
    urlshort = models.CharField(max_length=20, unique=True)
    # urlshortOrganization = models.CharField(max_length=20, unique=True)
    create_date = models.DateTimeField('date added')

    def __str__(self):
        return self.name

class Events(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=6000)
    location = models.TextField(max_length=2000)
    create_date = models.DateTimeField('date added')
    urlshort = models.CharField(max_length=20, unique=True)
    # urlshortEvents = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name

class session(models.Model):
    event=models.ForeignKey(Events, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=400)
    isSAM = models.BooleanField()
    isCAMPEP = models.BooleanField()
    isMDCB = models.BooleanField()
    start_datetime = models.DateTimeField('start time')
    end_datetime = models.DateTimeField('end time')
    # presenter = models.CharField(max_length=200)
    presenter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    CAMPEPReferenceID = models.CharField(max_length=100)
    def __str__(self):
        return self.title

    def session_happened(self):
        # print('#################################',self.start_datetime)
        # print('####',self.start_datetime.date(),self.start_datetime.date() > datetime.now().date())
        # print(self.state_datetime)
        return self.start_datetime.date() > datetime.now().date()

    def session_time(self):
        returnstr = ''
        for this in [self.start_datetime, self.end_datetime]:
            if this.hour < 10:
                returnstr += '0' + str(this.hour) + ':'
            else:
                returnstr +=       str(this.hour) + ':'
            if this.minute < 10:
                returnstr += '0' + str(this.minute)
            else:
                returnstr +=       str(this.minute)
            returnstr+='-'
        # str(self.end_datetime.minute)
        return returnstr[:-1]



class evaluation_Event(models.Model):
    event=models.ForeignKey(Events, on_delete=models.CASCADE)
    programContent = models.IntegerField()
    learningObjectives = models.IntegerField()
    facultyKnowledge = models.IntegerField()
    quality = models.IntegerField()
    handouts = models.IntegerField()
    meetingRoom = models.IntegerField()
    audio = models.IntegerField()
    additionalComments = models.TextField()
    create_date = models.DateTimeField(auto_now=True)#'date added')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class evaluation_Speaker(models.Model):
    session = models.ForeignKey(session, on_delete=models.CASCADE)
    learningObjectives = models.IntegerField()
    usefulness = models.IntegerField()
    quality = models.IntegerField()
    handout = models.IntegerField()
    worthiness = models.IntegerField()
    percentAttended = models.FloatField()
    additionalComments = models.TextField(default='')
    create_date = models.DateTimeField(auto_now=True)#'date added')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class attendance_Session(models.Model):
    session = models.ForeignKey(session, on_delete=models.CASCADE)
    # attendee = models.TextField(max_length=2000)
    needCAMPEP = models.BooleanField(default=False)
    needMDCB = models.BooleanField(default=False)
    percentAttended=models.FloatField()
    create_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class samQuestion(models.Model):
    session = models.ForeignKey(session, on_delete=models.CASCADE)
    question_text = models.TextField(max_length=900)
    reference = models.TextField(max_length=900)
    def choice_set(self):
        return samAnswer.objects.filter(samQuestion=self)

class samAnswer(models.Model):
    samQuestion=models.ForeignKey(samQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField(max_length=900)
    correct_answer = models.BooleanField(default=False)
    def __str__(self):
        return self.answer_text

class samResults(models.Model):
    samQuestion=models.ForeignKey(samQuestion, on_delete=models.CASCADE)
    selectedAnswer=models.ForeignKey(samAnswer, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)  # 'date added')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pass



