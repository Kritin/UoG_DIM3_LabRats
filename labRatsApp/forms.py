from django import forms
from labRatsApp.models import User

typee = [('rat','Rat'),('experimenter','Experimenter')]
class UserForm(forms.ModelForm):
	#username = forms.CharField(max_length = 128)
	password = forms.CharField(widget=forms.PasswordInput())
	#title = forms.CharField(max_length=128) 
	#name = forms.CharField(max_length = 128)
	#school = forms.CharField(max_length = 128)
	phone = forms.IntegerField()
    	userType = forms.ChoiceField(widget=forms.RadioSelect(),choices = typee)
	#webpage = forms.URLField(max_length=200)
    	#picture = forms.ImageField(upload_to='/users/level3/2107613s/Desktop/LabRats', blank=True)


	class Meta:
		model = User
		fields = ('username', 'password','userType','email','title','name','school','phone','webpage','picture')
