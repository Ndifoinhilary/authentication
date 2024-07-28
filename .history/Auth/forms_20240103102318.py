from django import forms
from Auth.models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    comfirm_password = forms.CharField(min_length=6, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "first_name", "password", "comfirm_password"]

    def clean_comfirm_password(self):
        password = self.cleaned_data.get("password")
        comfirm_password = self.cleaned_data.get("comfirm_password")

        if password != comfirm_password:
            raise forms.ValidationError("Password does not match")
        return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        return user
