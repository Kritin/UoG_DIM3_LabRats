import os

def populate():


    add_LabRatUser(user="Nitirk2",pas="alwaysForgetMyPassword",title="Mr.",name="KRITIN",sur="Singh",school="University of Nitirk",mail="0000003@founder.nit.ac.world",phone="AintNoBodyGotTimeForThat",userType="FatherOfAdmin",web="www.nitirk.world",pic='labRatsLogo.jpg')
  



def add_LabRatUser(user,pas,title,name,sur,school,mail,phone,userType,web,pic):
    u = LabRatUser.objects.get_or_create(user.username=user,user.password=pas,title=title,user.first_name=name,user.last_name = sur,school=school,user.email=mail,phone=phone,userType=userType,webpage=web,picture=pic)
    return u


def add_exper(user,experID,des,req,reward,max_parti, partiNum):
    exper = Experiment.objects.get_or_create(username=user,experimentID=experID,description=des,requirements=req,reward=reward,max_participants=max_parti, num_of_participant = partiNum)
    return exper


def add_timeslots(experID,date,time_from,time_to):
    tslot = Timeslots.objects.get_or_create(experimentID=experID,date=date,time_from=time_from,time_to=time_to)
    return tslot

def add_tags(tag):
    tags = Tags.objects.get_or_create(tag=tag)
    return tags

def add_haveTags(experID,tag):
    hTags = HaveTags.objects.get_or_create(experimentID=experID,tag=tag)
    return hTags

def add_bidFor(user,experID,date):
    bidF = BidFor.objects.get_or_create(username = user,experimentID=experID,date=date)
    return bidF

def add_participateIn(user,experID):
    partiIn = ParticipateIn.objects.get_or_create(username = user,experimentID=experID)
    return partiIn



# Start execution here!
if __name__ == '__main__':
    print "Starting labRatsApp population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LabRats.settings')
    from labRatsApp.models import User, Experiment,Timeslot,Tags,HaveTags,BidFor,ParticipateIn
    populate()



