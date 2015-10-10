from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from .models import UsedSkills, Diary

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'input-block-level',}))
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class DiaryForm(forms.ModelForm):

	class Meta:
		model = Diary
		exclude = ('user', 'time', 'mood')
		widgets = {
			
			'urge_suicide': forms.RadioSelect(),
			'urge_sh': forms.RadioSelect(),
		  	'used_skills': forms.CheckboxSelectMultiple(),
			'pain': forms.RadioSelect(),
			'sad': forms.RadioSelect(),
			'shame': forms.RadioSelect(),
			'anger': forms.RadioSelect(),
			'fear': forms.RadioSelect(),
			'disgust': forms.RadioSelect(),
			'jealousy': forms.RadioSelect(),
			'guilt': forms.RadioSelect(),
			'agitation': forms.RadioSelect(),
			'joy': forms.RadioSelect(),
            'happy': forms.RadioSelect(),
            'content': forms.RadioSelect(),
            'calm': forms.RadioSelect(),
            'grateful': forms.RadioSelect(),
            'excitement': forms.RadioSelect(),
            'optimism': forms.RadioSelect(),
            'hope': forms.RadioSelect(),
            'confidence': forms.RadioSelect(),
            'notes': forms.Textarea(attrs={'class':'input-block-level'})
		}

 
class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=False)
 
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
 
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user