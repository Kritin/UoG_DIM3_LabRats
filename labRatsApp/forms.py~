from django import forms
from labRatsApp.models import LabRatUser, User, DemographicsSurvey, Experiment

class UserForm(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'password','first_name','last_name','email')

class UserDetailsForm(forms.ModelForm):
	title = forms.ChoiceField(widget=forms.Select(), choices=[('mr','Mr.'), ('mrs','Mrs.'), ('miss', 'Miss'), ('dr', 'Dr.'), ('prof', 'Prof.')])
	userType = forms.ChoiceField(widget=forms.RadioSelect(),choices=[('rat','Rat'), ('experimenter','Experimenter')])
	class Meta:
		model = LabRatUser
		fields = ('title', 'phone', 'picture', 'userType', 'webpage')

class LabRatDetailsForm(forms.ModelForm):
	sex = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('m', 'M'), ('f', 'F')])
	educationLevel = forms.ChoiceField(widget=forms.Select(), choices=[('primary', 'Primary School'), ('secondary school', 'Secondary School'), ('undergraduate', 'Undergraduate'), ('postgraduate', 'Postgraduate')])

	class Meta:
		model = DemographicsSurvey
		fields = ('school', 'age', 'sex', 'firstLanguage', 'country', 'educationLevel')

'''
class UserForm2(forms.ModelForm):
	userType = forms.ChoiceField(widget=forms.RadioSelect(),choices=[('rat','Rat'),('experimenter','Experimenter')])

	class Meta:
		model = LabRatUser
		fields = ('title','phone','webpage','school','age','picture','userType')
'''

class ExperimentForm(forms.ModelForm):

	max_participants = forms.ChoiceField(choices=[(x, x) for x in range(1, 100)])
	
	class Meta:
		model = Experiment
		fields = ( 'title','description','requirements','max_participants')


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

