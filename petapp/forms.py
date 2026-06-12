from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Your Email")
    subject = forms.CharField(max_length=200, required=False, label="Subject")
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), label="Your Message")

class AdoptionForm(forms.Form):
    name = forms.CharField(max_length=100, label="Full Name")
    email = forms.EmailField(label="Email Address")
    phone = forms.CharField(max_length=20, label="Phone Number")
    address = forms.CharField(widget=forms.Textarea, label="Address")
    pet_name = forms.CharField(max_length=100, required=False, label="Which pet do you want to adopt?")
    message = forms.CharField(widget=forms.Textarea, required=False, label="Why do you want to adopt a pet?")

class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, label="Search")
