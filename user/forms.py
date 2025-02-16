from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']
class VerificationForm(forms.Form):
    code = forms.CharField(max_length=6, label='Введите код верификации')



class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)
    shop_name = forms.CharField(required=False)
    shop_description = forms.CharField(widget=forms.Textarea, required=False)
    contact_number = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role', 'shop_name', 'shop_description', 'contact_number')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")


        if role == 'seller':
            if not cleaned_data.get("shop_name") or not cleaned_data.get("contact_number"):
                raise forms.ValidationError("Для продавца обязательны название магазина и контактный номер.")
        return cleaned_data
