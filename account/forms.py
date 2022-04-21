
from secrets import choice
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib import messages
from django_countries.widgets import CountrySelectWidget
from django_countries import widgets, countries
from account.models import GENDER_CHOICES, Registration

YEARS= [x for x in range(1940,2021)]

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(widget=forms.TextInput, max_length=254, help_text='Required. Add a valid email address.')
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput, help_text='password must not be entirely numeric and must contain at least 8 characters')
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	gender = forms.ChoiceField(widget=forms.RadioSelect(), choices=GENDER_CHOICES)
	country = forms.ChoiceField(widget=CountrySelectWidget, choices=countries)
	dob = forms.DateField(initial="1990-06-21",widget=forms.SelectDateWidget(years=YEARS))
	class Meta:
		model = Registration
		fields = ('email', 'contact','first_name','last_name','country','dob','gender','password1', 'password2', )
		widgets = {
			'email': forms.EmailInput(attrs={'class': 'input'}),
		}
		widgets = {'country': CountrySelectWidget()}
		'{widget}<img class="country-select-flag" id="{flag_id}" style="margin: 6px 4px 0" src="{country.flag}">'

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password1'] != cd['password2']:
			raise forms.ValidationError('passwords do not match.')
		return cd['password2']
		
class UserAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	username = forms.EmailField()

	class Meta:
		model = Registration
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")



class UserRegistrationForm(forms.ModelForm):

	class Meta:
		model = Registration
		fields = ('email', 'contact', 'first_name', 'last_name', 'country','dob')

	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			try:
				account = Registration.objects.exclude(pk=self.instance.pk).get(email=email)
			except Registration.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" is already in use.' % account)


class UserUpdateForm(forms.ModelForm):

	class Meta:
		model = Registration
		fields = ('email', 'contact','first_name','last_name','country','dob')

	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			try:
				account = Registration.objects.exclude(pk=self.instance.pk).get(email=email)
			except Registration.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" is already in use.' % account)
