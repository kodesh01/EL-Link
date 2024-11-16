# forms.py

from django import forms

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'John'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Doe'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'name@example.com'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '+1234567890'}))
    country = forms.CharField(max_length=100, widget=forms.Select(choices=[('USA', 'USA'), ('Non USA', 'Non USA')]))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your message...'}))
