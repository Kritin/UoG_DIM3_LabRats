from django import forms
from labRatsApp.models import LabRatUser, User, DemographicsSurvey, Experiment, Requirement, Timeslot

class UserForm(forms.ModelForm):

	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'password','first_name','last_name','email')

class UserDetailsForm(forms.ModelForm):
	title = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=[('mr','Mr.'), ('mrs','Mrs.'), ('miss', 'Miss'), ('dr', 'Dr.'), ('prof', 'Prof.')])
	userType = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-control'}), label="Role", choices=[('rat','Rat'), ('experimenter','Experimenter')])
	phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	picture = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
	webpage = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	class Meta:
		model = LabRatUser
		fields = ('title', 'phone', 'picture', 'userType', 'webpage')

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

'''
class UserForm2(forms.ModelForm):
	userType = forms.ChoiceField(widget=forms.RadioSelect(),choices=[('rat','Rat'),('experimenter','Experimenter')])

	class Meta:
		model = LabRatUser
		fields = ('title','phone','webpage','school','age','picture','userType')
'''

class ExperimentForm(forms.ModelForm):

	max_participants = forms.ChoiceField(choices=[(x, x) for x in range(1, 100)])
	rewardType = forms.ChoiceField(widget=forms.Select(), choices=[('volunteer','Volunteer'), ('paid','Paid'),('credit', 'Credit')])

	date_start  = forms.DateField(widget=forms.widgets.DateInput(format="%m/%d/%Y")) 
	date_end = forms.DateField(widget=forms.widgets.DateInput(format="%m/%d/%Y")) 
	rewardAmount = forms.IntegerField(required=False, widget=forms.HiddenInput(),initial=123)
	class Meta:
		model = Experiment
		fields = ( 'title','description', 'max_participants','date_start','date_end','tags','rewardType','rewardAmount', 'location')

class RequirementsForm(forms.ModelForm):
	ageMin = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Minimum Age")
	ageMax = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Maximum Age")
	sex = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=[('m','M'), ('f','F')], label="Sex")
	firstLanguage = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="First Language")
	educationLevel = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), label="Education Level", choices=[('primary', 'Primary School'), ('secondary school', 'Secondary School'), ('undergraduate', 'Undergraduate'), ('postgraduate', 'Postgraduate')])
	location = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Location")

	class Meta:
		model = Requirement
		fields = ('ageMin', 'ageMax', 'sex', 'firstLanguage', 'educationLevel', 'location')

class TimeslotForm(forms.ModelForm):
	class Meta:
		model = Timeslot
		fields = ('date', 'time_from', 'time_to')

class EditUserForm(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		super(EditUserForm,self).__init__(*args,**kwargs)
		#self.fields.insert(len(self.fields)-1, 'first_name',forms.ModelChoiceField(queryset=User.objects.filter(first_name=self.initial['first_name'])))

		'''

		self.fields.insert(len(self.fields), 'first_name',forms.CharField(
User.objects.all().filter(first_name=self.initial['first_name'])[0]))
 
 		self.fields.insert(len(self.fields), 'last_name',forms.CharField(
User.objects.all().filter(last_name=self.initial['last_name'])[0]))

 		self.fields.insert(len(self.fields), 'email',forms.CharField(
User.objects.all().filter(email=self.initial['email'])[0]))
	
	'''

	class Meta:
		model = User
		fields = ('first_name','last_name','email')


class EditLabRatUserForm(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		super(EditLabRatUserForm,self).__init__(*args,**kwargs)
		#self.fields.insert(len(self.fields)-1, 'first_name',forms.ModelChoiceField(queryset=User.objects.filter(first_name=self.initial['first_name'])))


	class Meta:
		model = LabRatUser
		fields = ('title','phone','webpage')

'''
# Original class
class EditLabRatUserForm(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		super(EditLabRatUserForm,self).__init__(*args,**kwargs)
		#self.fields.insert(len(self.fields)-1, 'first_name',forms.ModelChoiceField(queryset=User.objects.filter(first_name=self.initial['first_name'])))


	class Meta:
		model = LabRatUser
		fields = ('title','phone','webpage','school','age')
'''




