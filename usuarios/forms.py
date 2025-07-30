from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class CustomSignupForm(UserCreationForm):
    """Formulario personalizado de registro usando email en lugar de username."""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Correo Electrónico'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Nombre'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Apellido'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Contraseña'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Confirmar Contraseña'
        })
    )

    class Meta:
        model = Usuario
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user