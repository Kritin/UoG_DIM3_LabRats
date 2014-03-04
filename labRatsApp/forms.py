from django import forms
from labRatsApp.models import LabRatUser,User,Experiment

typee = [('rat','Rat'),('experimenter','Experimenter')]



class UserForm(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'password','first_name','last_name','email')

class UserForm2(forms.ModelForm):
 	#username = forms.CharField(max_length = 128)
 	#title = forms.CharField(max_length=128) 
 	#name = forms.CharField(max_length = 128)
 	#school = forms.CharField(max_length = 128)
 	phone = forms.IntegerField()
    	#userType = forms.MultipleChoiceField(widget=forms.RadioSelect,choices=('Experimenter','Rat'))
    	userType = forms.ChoiceField(widget=forms.RadioSelect(),choices = typee)
 	#webpage = forms.URLField(max_length=200)
     	#picture = forms.ImageField(upload_to='/users/level3/2107613s/Desktop/LabRats', blank=True)

	class Meta:
		model = LabRatUser
		fields = ( 'title','phone','webpage','school','age','picture','userType')

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
		fields = ('title','phone','webpage','school','age')



