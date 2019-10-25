from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

def getOccupationChoices():
    #this will be part of a model at some point.. being lazy
    occupationChoices = (('Physicist', 'Physicist'),
                         ('Dosimetrist', 'Dosimetrist'),
                         ('Radiation Therapist', 'Radiation Therapist'),
                         ('Radiation Oncologist', 'Radiation Oncologist'),
                         ('Other', 'Other'),
                         )
    return occupationChoices


class CustomUser(AbstractUser):
    # add additional fields in here
    # username = models.CharField(max_length=40, unique=False, default='')
    campep = models.BooleanField(default=False)
    mdcb = models.BooleanField(default=False)
    occupation = models.CharField(max_length=30,choices=getOccupationChoices(), default='Physicist')



    def __str__(self):
        return self.email


