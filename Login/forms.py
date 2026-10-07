from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import Users, userType
import re


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['name', 'lastname', 'email']

        widgets = {
            'name': forms.TextInput({'class': 'login-field mb-2 form-control', 'placeholder': ''}),
            'lastname': forms.TextInput({'class': 'login-field mb-2 form-control', 'placeholder': ''}),
            'email': forms.TextInput({'class': 'login-field mb-2 form-control', 'placeholder': ''}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or not name.strip():
            raise ValidationError("El nombre es obligatorio")
        if len(name.strip()) < 2:
            raise ValidationError("El nombre debe tener al menos 2 caracteres")
        if len(name) > 50:
            raise ValidationError("El nombre no puede tener más de 50 caracteres")
        return name.strip()

    def clean_lastname(self):
        lastname = self.cleaned_data.get('lastname')
        if not lastname or not lastname.strip():
            raise ValidationError("El apellido es obligatorio")
        if len(lastname.strip()) < 2:
            raise ValidationError("El apellido debe tener al menos 2 caracteres")
        if len(lastname) > 50:
            raise ValidationError("El apellido no puede tener más de 50 caracteres")
        return lastname.strip()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or not email.strip():
            raise ValidationError("El correo electrónico es obligatorio")
        
        email = email.lower().strip()
        
        # Validate email format
        validator = EmailValidator("Ingresa un correo electrónico válido")
        validator(email)
        
        # Check if email is already taken by another user
        existing = Users.objects.filter(email=email).exclude(pk=self.instance.pk)
        if existing.exists():
            raise ValidationError("Este correo electrónico ya está registrado")
        
        return email


class UsersForm(forms.ModelForm):
    termsofservice = forms.BooleanField(
        required=True,
         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Acepto los términos y condiciones",
        error_messages={'required': 'Debes aceptar los términos y condiciones para continuar.'}
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput({'class': 'login-field mb-2 form-control', 'placeholder': ''}),
        label="Confirmar Contraseña"
    )

    class Meta:
        model = Users
        fields = ['name', 'lastname', 'email', 'password']

        widgets = {
            'name': forms.TextInput({'class': 'login-field mb-2 form-control', 'placeholder': ''}),
            'lastname': forms.TextInput({'class': 'login-field mb-2 form-control', 'placeholder': ''}),
            'email': forms.TextInput({'class': 'login-field mb-2 form-control', 'placeholder': ''}),
            'password': forms.PasswordInput({'class': 'login-field mb-2 form-control', 'placeholder': ''}),
            'usertype': forms.HiddenInput()
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or not name.strip():
            raise ValidationError("El nombre es obligatorio")
        if len(name.strip()) < 2:
            raise ValidationError("El nombre debe tener al menos 2 caracteres")
        if len(name) > 50:
            raise ValidationError("El nombre no puede tener más de 50 caracteres")
        return name.strip()

    def clean_lastname(self):
        lastname = self.cleaned_data.get('lastname')
        if not lastname or not lastname.strip():
            raise ValidationError("El apellido es obligatorio")
        if len(lastname.strip()) < 2:
            raise ValidationError("El apellido debe tener al menos 2 caracteres")
        if len(lastname) > 50:
            raise ValidationError("El apellido no puede tener más de 50 caracteres")
        return lastname.strip()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or not email.strip():
            raise ValidationError("El correo electrónico es obligatorio")
        
        email = email.lower().strip()
        
        # Validate email format
        validator = EmailValidator("Ingresa un correo electrónico válido")
        validator(email)
        
        # Check if email already exists
        if Users.objects.filter(email=email).exists():
            raise ValidationError("El correo ingresado ya está registrado")
        
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if not password:
            raise ValidationError("La contraseña es obligatoria")
        
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres")
        
        if len(password) > 128:
            raise ValidationError("La contraseña no puede tener más de 128 caracteres")
        
        # Check for at least one letter
        if not re.search(r'[a-zA-Z]', password):
            raise ValidationError("La contraseña debe contener al menos una letra")
        
        # Check for at least one number
        if not re.search(r'\d', password):
            raise ValidationError("La contraseña debe contener al menos un número")
        
        return password

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if not password2:
            raise ValidationError("Debes confirmar tu contraseña")

        if password and password2 and password != password2:
            raise ValidationError("Las contraseñas no coinciden, inténtalo nuevamente")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.usertype = userType.objects.get(id=1)
            user.save()
        return user


class OwnersForm(forms.ModelForm):
    password2 = forms.CharField(
        widget=forms.PasswordInput({'class': 'login-field mb-2 form-control', 'placeholder': ''}),
        label="Confirmar Contraseña"
    )

    class Meta:
        model = Users
        fields = ['name', 'lastname', 'email', 'password']

        widgets = {
            'name': forms.TextInput({'class': 'login-field mb-2 form-control', 'placeholder': ''}),
            'lastname': forms.TextInput({'class': 'login-field mb-2 form-control', 'placeholder': ''}),
            'email': forms.TextInput({'class': 'login-field mb-2 form-control', 'placeholder': ''}),
            'password': forms.PasswordInput({'class': 'login-field mb-2 form-control', 'placeholder': ''}),
            'usertype': forms.HiddenInput()
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or not name.strip():
            raise ValidationError("El nombre es obligatorio")
        if len(name.strip()) < 2:
            raise ValidationError("El nombre debe tener al menos 2 caracteres")
        if len(name) > 50:
            raise ValidationError("El nombre no puede tener más de 50 caracteres")
        return name.strip()

    def clean_lastname(self):
        lastname = self.cleaned_data.get('lastname')
        if not lastname or not lastname.strip():
            raise ValidationError("El apellido es obligatorio")
        if len(lastname.strip()) < 2:
            raise ValidationError("El apellido debe tener al menos 2 caracteres")
        if len(lastname) > 50:
            raise ValidationError("El apellido no puede tener más de 50 caracteres")
        return lastname.strip()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or not email.strip():
            raise ValidationError("El correo electrónico es obligatorio")
        
        email = email.lower().strip()
        
        # Validate email format
        validator = EmailValidator("Ingresa un correo electrónico válido")
        validator(email)
        
        # Check if email already exists
        if Users.objects.filter(email=email).exists():
            raise ValidationError("El correo ingresado ya está registrado")
        
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if not password:
            raise ValidationError("La contraseña es obligatoria")
        
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres")
        
        if len(password) > 128:
            raise ValidationError("La contraseña no puede tener más de 128 caracteres")
        
        # Check for at least one letter
        if not re.search(r'[a-zA-Z]', password):
            raise ValidationError("La contraseña debe contener al menos una letra")
        
        # Check for at least one number
        if not re.search(r'\d', password):
            raise ValidationError("La contraseña debe contener al menos un número")
        
        return password

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if not password2:
            raise ValidationError("Debes confirmar tu contraseña")

        if password and password2 and password != password2:
            raise ValidationError("Las contraseñas no coinciden, inténtalo nuevamente")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.usertype = userType.objects.get(id=2)
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput({'class': 'login-field mb-2 form-control', 'placeholder': ''}),
        label="Correo Electrónico"
    )
    password = forms.CharField(
        widget=forms.PasswordInput({'class': 'login-field mb-2 form-control', 'placeholder': ''}),
        label="Contraseña"
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if not email or not email.strip():
            raise ValidationError("El correo electrónico es obligatorio")
        
        email = email.lower().strip()
        
        # Validate email format
        validator = EmailValidator("Ingresa un correo electrónico válido")
        validator(email)
        
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        
        if not password:
            raise ValidationError("La contraseña es obligatoria")
        
        return password

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            try:
                user = Users.objects.get(email=email)
                if not user.check_password(password):
                    raise ValidationError("Correo o contraseña incorrectos")
            except Users.DoesNotExist:
                raise ValidationError("Correo o contraseña incorrectos")

        return cleaned_data