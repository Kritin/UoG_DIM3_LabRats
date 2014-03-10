from django.db import models
from datetime import date
from django.contrib.auth.models import User


class LabRatUser(models.Model):
    user = models.OneToOneField(User)
    title = models.CharField(max_length=128) 
    phone = models.CharField(max_length=128)
    userType = models.CharField(max_length=128)
    picture = models.ImageField(upload_to='media/', default = "default.png")
    webpage = models.URLField(blank=True)

    def __unicode__(self):
        return str(self.user.username)

class DemographicsSurvey(models.Model):
    user = models.OneToOneField(LabRatUser, primary_key=True)
    school = models.CharField(max_length=128)
    age = models.IntegerField()
    sex = models.CharField(max_length=1)
    firstLanguage = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    educationLevel = models.CharField(max_length=128)

    def __unicode__(self):
        return str(self.user.user.username)

class Experiment(models.Model):
    experimentID = models.IntegerField(unique=True,primary_key=True) 
    user = models.ForeignKey(LabRatUser) 
    title = models.CharField(max_length=128) 
    description  = models.CharField(max_length=128)
    requirements = models.CharField(max_length=128)
    reward = models.CharField(max_length=128)
    max_participants = models.IntegerField()
    num_of_participants = models.IntegerField(default= "0")

    def __unicode__(self):
        return str(self.experimentID)

#weak entity
class Timeslot(models.Model):
    timeslotID = models.IntegerField(unique = True, primary_key=True)
    experimentID = models.ForeignKey(Experiment) #Primary key
    date = models.DateField(null=False)
    time_from = models.TimeField(null=False)
    time_to  = models.TimeField(null=False)

    def __unicode__(self):
	return str(self.timeslot)

#weak entity
class Tags(models.Model):
    tag  = models.CharField(max_length=128,primary_key=True)

    def __unicode__(self):
	return str(self.tag)


# M2M between Tags and Experiment
class HaveTags(models.Model):
    experimentID = models.ForeignKey(Experiment)   
    tag = models.ForeignKey(Tags)

    def __unicode__(self):
         return u'%s %s' % (self.experimentID , self.tag)

    class Meta:
       unique_together = (("experimentID", "tag"),)

'''
# M2M between User and Experiment
class BidFor(models.Model):
    user = models.ForeignKey(LabRatUser)
    experimentID = models.ForeignKey(Experiment)

    date = models.DateField(null=False)  #default=datetime.date.today

    def __unicode__(self):
        return u'%s %s' % (self.user , self.experimentID)

    class Meta:
        unique_together = (("user", "experimentID"),)
'''

# M2M between User and Experiment
class ParticipateIn(models.Model):
    user = models.ForeignKey(LabRatUser)
    experimentID = models.ForeignKey(Experiment)
    status = models.CharField(max_length=128) # bidding / accepted / rejected
    date = models.DateField(null=False) # date of last status change

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



