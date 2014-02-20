from django.db import models
from datetime import date

class User(models.Model):
    username = models.CharField(max_length=128, primary_key=True)  # Primary key
    password = models.CharField(max_length=128,null=False) #//// have to change to password field
    # user enrol to Time slot reletionship 

    title = models.CharField(max_length=128) 
    name = models.CharField(max_length=128)
    school = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    userType = models.CharField(max_length=128)
    webpage = models.URLField()

    def __unicode__(self):
        return self.username

class Experiment(models.Model):
    username = models.ForeignKey(User)  
    experimentID = models.IntegerField(unique=True,primary_key=True) 

    description  = models.CharField(max_length=128)
    requirements = models.CharField(max_length=128)
    reward = models.CharField(max_length=128)
    max_participants = models.IntegerField()
    num_of_participants = models.IntegerField()

    def __unicode__(self):
        return self.experimentID

#weak entity
class Timeslots(models.Model):
    experimentID = models.ForeignKey(Experiment,primary_key=True) #Primary key
    date = models.DateField(null=False)
    time_from = models.TimeField(null=False)
    time_to  = models.TimeField(null=False)

    def __unicode__(self):
        return self.experimentID

#weak entity
class Tags(models.Model):
    tag  = models.CharField(max_length=128,primary_key=True)

    def __unicode__(self):
	return self.tag


# M2M between Tags and Experiment
class HaveTags(models.Model):
    experimentID = models.ForeignKey(Experiment,primary_key=True)   
    tag = models.ForeignKey(Tags,primary_key=True)

    def __unicode__(self):
	return (self.experimentID , self.tag)
    

# M2M between User and Experiment
class BidFor(models.Model):
    username = models.ForeignKey(User,primary_key=True)
    experimentID = models.ForeignKey(Experiment,primary_key=True)

    date = models.DateField(null=False)  #default=datetime.date.today

    def __unicode__(self):
	return (self.username , self.experimentID)


# M2M between User and Experiment
class ParticipateIn(models.Model):
    username = models.ForeignKey(User,primary_key=True)
    experimentID = models.ForeignKey(Experiment,primary_key=True)

    def __unicode__(self):
	return (self.username,self.experimentID)




