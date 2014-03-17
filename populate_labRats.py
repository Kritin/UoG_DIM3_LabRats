import os

def populate():

	# User
	velizar = add_user(
		user="velizar",
		pas="1234",
		firstN="Velizar",
		lastN="Shulev",
		email="1103834s@student.gla.ac.uk",
	)

	kritin = add_user(
		user="kritin",
		pas="1234",
		firstN="Kritin",
		lastN="Singh",
		email="2107613S@student.gla.ac.uk",
	)
	
	flavia = add_user(
		user="flavia",
		pas="1234",
		firstN="Flavia",
		lastN="Veres",
		email="flavia@student.gla.ac.uk",
	)
	
	mircea = add_user(
		user="mircea",
		pas="1234",
		firstN="Mircea",
		lastN="Iordache",
		email="mircea@student.gla.ac.uk",
	)
	
	matthew = add_user(
		user="matthew",
		pas="1234",
		firstN="Matthew",
		lastN="Bown",
		email="matthew@student.gla.ac.uk",
	)

	alfred = add_user(
		user="alfred",
		pas="1234",
		firstN="Alfred",
		lastN="Binet",
		email="abinet@example.com",
	)

	solomon = add_user(
		user="solomon",
		pas="1234",
		firstN="Solomon",
		lastN="Asch",
		email="sasch@example.com",
	)

	# LabRatUser
	velizar = add_labRatUser(
		user=velizar,
		title="Mr.",
		phone="0123456789",
		userType="rat",
		webpage=""
	)

	kritin = add_labRatUser(
		user=kritin,
		title="Mr.",
		phone="0123456789",
		userType="rat",
		webpage=""
	)

	flavia = add_labRatUser(
		user=flavia,
		title="Miss",
		phone="0123456789",
		userType="rat",
		webpage=""
	)

	mircea = add_labRatUser(
		user=mircea,
		title="Mr.",
		phone="0123456789",
		userType="rat",
		webpage=""
	)

	matthew = add_labRatUser(
		user=matthew,
		title="Mr.",
		phone="0123456789",
		userType="rat",
		webpage=""
	)

	alfred = add_labRatUser(
		user=alfred,
		title="Dr.",
		phone="0123456789",
		userType="experimenter",
		webpage="http://en.wikipedia.org/wiki/Alfred_Binet"
	)

	solomon = add_labRatUser(
		user=solomon,
		title="Dr.",
		phone="0123456789",
		userType="experimenter",
		webpage="http://en.wikipedia.org/wiki/Solomon_Asch"
	)

	#Demographics Survey
	add_demographicsSurvey(
		user=velizar,
		school="University of Glasgow",
		age=21,
		sex="m",
		firstLanguage="Bulgarian",
		country="Bulgaria",
		educationLevel="undergraduate",
		location="Glasgow"
	)

	add_demographicsSurvey(
		user=kritin,
		school="University of Glasgow",
		age=21,
		sex="m",
		firstLanguage="Thai",
		country="Thailand",
		educationLevel="undergraduate",
		location="Glasgow"
	)

	add_demographicsSurvey(
		user=flavia,
		school="University of Glasgow",
		age=21,
		sex="f",
		firstLanguage="Romanian",
		country="Romania",
		educationLevel="undergraduate",
		location="Glasgow"
	)

	add_demographicsSurvey(
		user=mircea,
		school="University of Glasgow",
		age=21,
		sex="m",
		firstLanguage="Romanian",
		country="Romania",
		educationLevel="undergraduate",
		location="Glasgow"
	)

	add_demographicsSurvey(
		user=matthew,
		school="University of Glasgow",
		age=21,
		sex="m",
		firstLanguage="German",
		country="Scotland",
		educationLevel="undergraduate",
		location="Glasgow"
	)

	# Experiment
	experiment1 = add_exper (
		user=solomon,
		title="Participants required for insomnia & depression study",
		des="Would you like to take part in a research study being conducted by the University of Glasgow, funded by the National Institutes of Health (NIH) in America? The research seeks to understand the relationship between poor sleep and depression. We are currently looking for the following individuals, aged 25-65: people with insomnia (problems falling asleep and/or staying asleep) and depression, who are currently being treated with an anti-depressant. people with insomnia (problems falling asleep and/or staying asleep), who have experienced depression in the past, but are not currently depressed, and may or may not still be taking an anti-depressant.The study involves an initial medical and mental health screening assessment, to ensure that participants meet eligibility criteria. The main component of the study involves sleeping overnight, for two nights, at the University of Glasgow Sleep Centre, Southern General Hospital.Each participant will receive 250 for completing all aspects of the study and will be offered, as a 'thank you' for participation, the opportunity to take part in group cognitive behavioural therapy (CBT) for their sleep difficulties. If you are interested in taking part in the study, or want to find out more information, please contact Dr Simon Kyle on 0141 232 7700, or alternatively email glasgowsleepcentre@clinmed.gla.ac.uk",
		max_parti=100,
		num_participants=21,
		date_start="2014-4-12",
		date_end="2014-5-12",
		tags="research, university, glasgow, isomnia, depression, nih, murica",
		rewardType="paid",
		rewardAmount=250,
		status="open",
		location="Glasgow"
	)

	experiment2 = add_exper (
		user=solomon,
		title="Participants wanted to take part in a nutrition study!",
		des="We are looking for healthy volunteers aged 19 - 64 to take part in a nutrition study investigating the effects of dietary fibre and protein on gut health. What would you be required to do? - Record your weighed dietary intake for 3 days - Collecting urine for 24 hours What are the benefits of taking part?- We will provide you with detailed analysis of your diet and offer advice on how to improve it - You will be entered into a draw to win a Nintendo Wii Console (alternative prizes may be available) If you are interested in taking part in this study or wish further information please do not hesitate to contact: Laura Hanske Human Nutrition University of Glasgow Laura.Hanske@clinmed.gla.ac.uk 0141 232 1857",
		max_parti=20,
		num_participants=3,
		date_start="2014-4-21",
		date_end="2014-6-8",
		tags="research, university, glasgow, healthy, nutrition, food, dietary, fibre, much, protein, wow, gut, health",
		rewardType="paid",
		rewardAmount=25,
		status="open",
		location="Glasgow"
	)

	experiment3 = add_exper (
		user=solomon,
		title="Participants wanted for study on visual perception",
		des="We are currently running a behavioural study to examine how visual information associated to the self or others influences visual perception. Expiry Date: 16th December 2013. We would like to invite you to take part in our  study if you are: right handed aged 19-35 have normal or corrected-to-normal vision The study takes place at the Department of Experimental Psychology in the University of Oxford, and will last around 60 min. You will be reimbursed for your time at a rate of 10/hour. If you are interested in participating in the study and/or would like further information, please write an email to moritz.stolte@psy.ox.ac.uk and indicate when you could take part.",
		max_parti=20,
		num_participants=3,
		date_start="2014-4-23",
		date_end="2014-4-30",
		tags="research, university, oxford, visual, perception, information",
		rewardType="paid",
		rewardAmount=100,
		status="open",
		location="Oxford"
	)

	experiment4 = add_exper (
		user=alfred,
		title="Participants needed for a driving simulator study at the Illinois Simulator Lab",
		des="Participants needed for a driving simulator study at the Illinois Simulator Lab. Participants should be between ages 18-30, have normal color vision (20/40 or better) without glasses (contacts are fine), and hold a valid driver's license for at least two years. The study lasts 2 hours and you will be paid $8 per hour plus parking.",
		max_parti=400,
		num_participants=127,
		date_start="2014-4-23",
		date_end="2014-4-30",
		tags="research, university, illinois, driving, simulator, lab, driving, license",
		rewardType="paid",
		rewardAmount=8,
		status="open",
		location="Illinois"
	)

	experiment5 = add_exper (
		user=alfred,
		title="Wanted: Focus Group Participants - two free tickets for Glasgow Film Festival 2012",
		des="** AHRC-Funded Collaborative Doctorate between the University of Glasgow and Glasgow Film ** I am in the process of conducting fieldwork for an qualitative audience study (doctoral level) which looks at contemporary cinema-going in Glasgow and the cultural impact of cinemas and film festivals. Taking Glasgow Film Festival (GFF) as a case study, I will run focus groups throughout the festival and I'm now recruiting participants. Sessions take place at Glasgow Film Theatre on Rose Street and last approximately one hour. They are very informal and involve a  small group of people (maximum of 8 people per session). What's in it for you? Wine, nibbles and soft drinks are provided. Two FREE film festival tickets per participant as a thank you. A chance to talk about your festival experiences with other festival-goers. Participation in a very important piece of cultural research. The criteria for participation is: A)  You are OVER 18 YEARS OLD. B) You will have been to Glasgow Film Festival or a strand of the festival (youth film festival, short film festival etc) C) I also welcome participants who will be attending GFF for the first time in 2012, however, you must have attended prior to attending a session as you'll be chatting about your 'festival experience'.  If you would like to take part and you can commit to attending one of the sessions below, please email me on: cinemafocusgroups@gmail.com Hope to hear from you. Regards, Lesley Dickson Film and TV Studies - University of Glasgow",
		max_parti=50,
		num_participants=14,
		date_start="2014-5-16",
		date_end="2014-5-24",
		tags="university, glasgow, focus, group, film, festival, contemporary, cinema",
		rewardType="paid",
		rewardAmount=4,
		status="open",
		location="Glasgow"
	)

	experiment6 = add_exper (
		user=alfred,
		title="The One Show requires participants on Tuesday 25th May for filming in Glasgow",
		des=" BBC's The One Show are filming a science item in Glasgow. Participants will be required to take part in a psychology demonstration. Location: Glasgow, United Kingdom Payment details: no pay Applications to this casting call require: A phone number A profile photo",
		max_parti=100,
		num_participants=76,
		date_start="2014-5-14",
		date_end="2014-5-15",
		tags="one, show, bbc, filming, psychology, demonstration",
		rewardType="paid",
		rewardAmount=50000,
		status="open",
		location="Glasgow"
	)

	# Requirement

def add_user(user,pas,firstN,lastN,email):
	u = User.objects.get_or_create(username=user, password=pas, first_name=firstN, last_name=lastN, email=email)[0]
	u.set_password(u.password)
	u.save()
	return u

def add_labRatUser(user,title,phone,userType,webpage):
	return LabRatUser.objects.get_or_create(user=user, title=title, phone=phone, userType=userType, webpage=webpage)[0]

def add_demographicsSurvey(user, school, age, sex, firstLanguage, country, educationLevel, location):
	return DemographicsSurvey.objects.get_or_create(user=user, school=school, age=age, sex=sex, firstLanguage=firstLanguage, country=country, educationLevel=educationLevel, location=location)[0]

def add_exper(user, title, des, max_parti, num_participants, date_start, date_end, tags, rewardType, rewardAmount, status, location):
    return Experiment.objects.get_or_create(user=user, description=des, title=title, max_participants=max_parti, num_of_participants=num_participants, date_start=date_start, date_end=date_end, tags=tags, rewardType=rewardType, rewardAmount=rewardAmount, status=status, location=location)[0]

def add_requirement(experiment, ageMin, ageMax, sex, firstLanguage, educationLevel, location):
	return Requirement.objects.get_or_create(experiment=experiment, ageMin=ageMin, ageMax=ageMax, sex=sex, firstLanguage=firstLanguage, educationLevel=educationLevel, location=location)[0]

def add_timeslot(timeslotID, experimentID, date, time_from, time_to):
	return Timeslot.objects.get_or_create(timeslotID=timeslotID, experimentID=experimentID, date=date, time_from=time_from, time_to=time_to)[0]

def add_participateIn(user, experimentID, status, date):
	return ParticipateIn.objects.get_or_create(user=user, experimentID=experimentID, status=status, date=date)[0]

def add_enrolIn(user, timeslotID):
	return EnrolIn(user=user, timeslotID=timeslotID)[0]

# Start execution here!
if __name__ == '__main__':
	print "Starting labRatsApp population script..."
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LabRats.settings')
	from labRatsApp.models import User, LabRatUser, Experiment, Timeslot, ParticipateIn, EnrolIn, DemographicsSurvey, Requirement
	populate()



