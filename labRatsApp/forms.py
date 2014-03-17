from django import forms
from labRatsApp.models import LabRatUser, User, DemographicsSurvey, Experiment, Requirement, Timeslot

class UserForm(forms.ModelForm):

	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'password','first_name','last_name','email')

class UserDetailsForm(forms.ModelForm):
	title = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=[('mr','Mr.'), ('mrs','Mrs.'), ('miss', 'Miss'), ('dr', 'Dr.'), ('prof', 'Prof.')])
	userType = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-control'}), label="Role", choices=[('rat','Rat'), ('experimenter','Experimenter')])
	phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	picture = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}), required=False)
	webpage = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
	class Meta:
		model = LabRatUser
		fields = ('title', 'phone', 'picture', 'userType', 'webpage')


class ExperimentForm(forms.ModelForm):
	
	title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
	max_participants = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
	rewardType = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=[('volunteer','Volunteer'), ('paid','Paid'),('credit', 'Credit')])
	tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	date_start  = forms.DateField(widget=forms.widgets.DateInput(attrs={'class':'form-control'}, format="%d/%m/%Y")) 
	date_end = forms.DateField(widget=forms.widgets.DateInput(attrs={'class':'form-control'}, format="%d/%m/%Y")) 
	rewardAmount = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'class':'form-control'}),initial=0)

	class Meta:
		model = Experiment
		fields = ( 'title','description', 'max_participants','date_start','date_end','tags','rewardType','rewardAmount')

class RequirementsForm(forms.ModelForm):
	ageMin = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Minimum Age")
	ageMax = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Maximum Age")
	sex = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=[(' ', ' '), ('m','M'), ('f','F')], label="Sex")
	firstLanguage = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="First Language")
	educationLevel = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label="Education Level", choices=[('primary', 'Primary School'), ('secondary school', 'Secondary School'), ('undergraduate', 'Undergraduate'), ('postgraduate', 'Postgraduate')])
	location = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Location")

	class Meta:
		model = Requirement
		fields = ( 'ageMin','ageMax', 'sex','firstLanguage','educationLevel','location')
		
class TimeslotForm(forms.ModelForm):
	date  = forms.DateField(widget=forms.widgets.DateInput(attrs={'class':'form-control'}, format="%d/%m/%Y"))
	time_from  = forms.TimeField(widget=forms.widgets.DateInput(attrs={'class':'form-control'}))
	time_to  = forms.TimeField(widget=forms.widgets.DateInput(attrs={'class':'form-control'}))

	class Meta:
		model = Timeslot
		fields = ('date', 'time_from', 'time_to')

class EditUserForm(forms.ModelForm):
	
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
	
	def __init__(self,*args,**kwargs):
		super(EditUserForm,self).__init__(*args,**kwargs)
		#self.fields.insert(len(self.fields)-1, 'first_name',forms.ModelChoiceField(queryset=User.objects.filter(first_name=self.initial['first_name'])))


	class Meta:
		model = User
		fields = ('password','first_name','last_name','email')
		
class EditUserDetailsForm(forms.ModelForm):
	title = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=[('mr','Mr.'), ('mrs','Mrs.'), ('miss', 'Miss'), ('dr', 'Dr.'), ('prof', 'Prof.')])
	phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	picture = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}), required=False)
	webpage = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
	
	def __init__(self,*args,**kwargs):
		super(EditUserDetailsForm,self).__init__(*args,**kwargs)


	class Meta:
		model = LabRatUser
		fields = ('title', 'phone', 'webpage', 'picture')

class LabRatDetailsForm(forms.ModelForm):
	school = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	age = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
	sex = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-control'}), choices=[('m', 'M'), ('f', 'F')])
	firstLanguage = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="First Language")
	country = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	educationLevel = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label="Education Level", choices=[('primary', 'Primary School'), ('secondary school', 'Secondary School'), ('undergraduate', 'Undergraduate'), ('postgraduate', 'Postgraduate')])
	location = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = DemographicsSurvey
		fields = ('school', 'age', 'sex', 'firstLanguage', 'country', 'educationLevel', 'location')





