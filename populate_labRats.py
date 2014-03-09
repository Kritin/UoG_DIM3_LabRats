import os

def populate():

	user_detail = add_user(user="Nitirk",pas="1234",firstN="Kritin",lastN="Singh",email="2107613S@student.gla.ac.uk")
	labRatUser_detail = add_labRatUser(user=user_detail,title="MR.",phone="07858143797",userType="rat",webpage="nitirk.com",school="UoG",age=120)

	user_detail = add_user(user="Nitirk",pas="1234",firstN="Kritin",lastN="Singh",email="2107613S@student.gla.ac.uk")
	labRatUser_detail = add_labRatUser(user=user_detail,title="MR.",phone="07858143797",userType="rat",webpage="nitirk.com",school="UoG",age=120)
	
	
	user_detail2 = add_user(user="Nitirk2",pas="1234",firstN="Kritin",lastN="Singh",email="2107613S@student.gla.ac.uk")
	labRatUser_detail2 = add_labRatUser(user=user_detail2,title="MR.",phone="07858143797",userType="experimenter",webpage="nitirk.com",school="UoG",age=120)


		
	user_detail3 = add_user(user="Nitirk3",pas="1234",firstN="Kritin",lastN="Singh",email="2107613S@student.gla.ac.uk")
	labRatUser_detail3 = add_labRatUser(user=user_detail3,title="MR.",phone="07858143797",userType="experimenter",webpage="nitirk.com",school="UoG",age=121)

	exper1 = add_exper(user= labRatUser_detail2  ,title = "nitirk2Exper1",des="Blah ",req="No req",reward="not implement yet",max_parti=121)

	exper2 = add_exper(user= labRatUser_detail2  ,title = "nitirk2Exper2",des="Blah Blah",req="No req",reward="not implement yet",max_parti=122)

	exper3 = add_exper(user= labRatUser_detail2  ,title = "nitirk2Exper3",des="Blah Blah Blah",req="No req",reward="not implement yet",max_parti=123)

	exper4 = add_exper(user= labRatUser_detail2  ,title = "nitirk2Exper4",des="Blah Blah Blah Blah",req="No req",reward="not implement yet",max_parti=124)

	exper5 = add_exper(user= labRatUser_detail3  ,title = "nitirk3Exper1",des="Blah Blah Blah",req="No req",reward="not implement yet",max_parti=131)
	exper6 = add_exper(user= labRatUser_detail3  ,title = "nitirk3Exper2",des="Blah Blah Blah Blah",req="No req",reward="not implement yet",max_parti=132)
	




"""
    add_user(user="Nitirk2",pas="alwaysForgetMyPassword",title="Mr.",name="KRITIN",school="University of Nitirk",mail="0000003@founder.nit.ac.world",phone="AintNoBodyGotTimeForThat",userType="FatherOfAdmin",web="www.nitirk.world",pic='labRatsLogo.jpg')
  
"""

"""
def add_user(user,pas,title,name,school,mail,phone,userType,web,pic):
    u = LabRatUser.objects.get_or_create(username=user,password=pas,title=title,name=name,school=school,email=mail,phone=phone,userType=userType,webpage=web,picture=pic)
    return u
"""
"""
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
"""

def add_exper(user,title,des,req,reward,max_parti):
    exper = Experiment.objects.get_or_create(user=user,description=des,title=title,requirements=req,reward=reward,max_participants=max_parti)[0]
    return exper

def add_user(user,pas,firstN,lastN,email):
	u = User.objects.get_or_create(username=user,password=pas,first_name=firstN,last_name=lastN,email=email)[0]
	return u

def add_labRatUser(user,title,phone,userType,webpage,school,age):
	u2 = LabRatUser.objects.get_or_create(user=user,title=title,phone=phone,userType=userType,webpage=webpage,school=school,age=age)[0]
	return u2

# Start execution here!
if __name__ == '__main__':
    print "Starting labRatsApp population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LabRats.settings')
    from labRatsApp.models import User,LabRatUser, Experiment,Timeslot,Tags,HaveTags,BidFor,ParticipateIn
    populate()



