from django.db import models
from datetime import date
from django.contrib.auth.models import User


class LabRatUser(models.Model):
    user = models.OneToOneField(User)
    title = models.CharField(max_length=128) 
    phone = models.CharField(max_length=128)
    userType = models.CharField(max_length=128)
    picture = models.ImageField(upload_to='/',blank=True)
    webpage = models.URLField(blank=True) #Experimenter
    school = models.CharField(max_length=128)#Rat
    age = models.IntegerField()#Rat
    userType = models.CharField(max_length=128)
   

    def __unicode__(self):
        return self.user.username

'''
class Experimenter(models.Model):
    user = models.ForeignKey(LabRatUser)
    webpage = models.URLField(blank=True)

    def __unicode__(self):
        return self.user

class Rat(moLabRatUserdels.Model):
    user = models.ForeignKey(LabRatUser)
    school = models.CharField(max_length=128)
    age = models.IntegerField()

    def __unicode__(self):
        return self.user

'''

class Experiment(models.Model):
    experimentID = models.IntegerField(unique=True,primary_key=True) 
    user = models.ForeignKey(LabRatUser) 
    description  = models.CharField(max_length=128)
    requirements = models.CharField(max_length=128)
    reward = models.CharField(max_length=128)
    max_participants = models.IntegerField()
    num_of_participants = models.IntegerField()

    def __unicode__(self):
        return self.experimentID

class Timeslot(models.Model):
    timeslotID = models.IntegerField(unique = True, primary_key=True)
    experimentID = models.ForeignKey(Experiment) #Primary key
    date = models.DateField(null=False)
    time_from = models.TimeField(null=False)
    time_to  = models.TimeField(null=False)

    def __unicode__(self):
	return self.timeslotID

#weak entity
class Tags(models.Model):
    tag  = models.CharField(max_length=128,primary_key=True)

    def __unicode__(self):
	return self.tag


# M2M between Tags and Experiment
class HaveTags(models.Model):
    experimentID = models.ForeignKey(Experiment)   
    tag = models.ForeignKey(Tags)

    def __unicode__(self):
         return u'%s %s' % (self.experimentID , self.tag)

    class Meta:
       unique_together = (("experimentID", "tag"),)
    

# M2M between Rat and Experiment
class BidFor(models.Model):
    user = models.ForeignKey(LabRatUser)
    experimentID = models.ForeignKey(Experiment)

    date = models.DateField(null=False)  #default=datetime.date.today

    def __unicode__(self):
        return u'%s %s' % (self.user , self.experimentID)

    class Meta:
        unique_together = (("user", "experimentID"),)


# M2M between Rat and Experiment
class ParticipateIn(models.Model):
    user = models.ForeignKey(LabRatUser)
    experimentID = models.ForeignKey(Experiment)

    def __unicode__(self):
        return u'%s %s' % (self.user,self.experimentID)

    class Meta:
       unique_together = (("user", "experimentID"),)


# M2M between Rat and Timeslot  
class EnrolIn(models.Model):
    user = models.ForeignKey(LabRatUser)
    timeslotID = models.ForeignKey(Timeslot)

    def __unicode__(self):
	return u'%s %s' % (self.user,self.timeslotID)

    class Meta:
       unique_together = (("user", "timeslotID"),)


