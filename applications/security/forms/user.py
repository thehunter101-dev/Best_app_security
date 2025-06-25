from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from applications.security.models import User



class UserUpdateForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={
            "class": "w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 h-32 resize-none",
            "multiple": "multiple"
        }),
        required=False,
        label="Grupos"
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'dni',
            'direction', 'phone', 'image',
            'is_active', 'is_staff',
            'groups',
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre de usuario',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Ingrese los nombres',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Ingrese los apellidos',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Ingrese el correo electrónico',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
            }),
            'dni': forms.TextInput(attrs={
                'placeholder': 'Ingrese DNI/Cédula o RUC',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
            }),
            'direction': forms.TextInput(attrs={
                'placeholder': 'Ingrese la dirección',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Ingrese el teléfono',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500 focus:ring-2 transition-colors'
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500 focus:ring-2 transition-colors'
            }),
            'groups': forms.SelectMultiple(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 h-32'
            }),
        }
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
            'dni': 'DNI/Cédula o RUC',
            'direction': 'Dirección',
            'phone': 'Teléfono',
            'image': 'Imagen de Perfil',
            'is_active': 'Activo',
            'is_staff': 'Personal de Administración (Staff)',
            'groups': 'Grupos',
        }
        help_texts = {
            'username': 'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.',
            'is_active': 'Designa si este usuario debe ser tratado como activo. Desmarque esto en lugar de borrar cuentas.',
            'is_staff': 'Designa si el usuario puede iniciar sesión en el sitio de administración y tiene permisos implícitos de staff.',
            'groups': 'Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos otorgados a cada uno de sus grupos.',
        }
        error_messages = {
            'username': {'unique': "Un usuario con ese nombre de usuario ya existe."},
            'email': {'unique': "Un usuario con ese correo electrónico ya existe."},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        # Optionally disable username editing for existing users
        # if self.instance and self.instance.pk:
        #     self.fields['username'].disabled = True
        #     self.fields['username'].help_text = "El nombre de usuario no se puede cambiar una vez creado."

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
        if self.instance and self.instance.pk:
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Un usuario con este correo electrónico ya existe.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance and self.instance.pk and not self.fields['username'].disabled:
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Un usuario con este nombre de usuario ya existe.")
        return username


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingrese la contraseña',
            'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
        }),
        label="Contraseña",
        required=True,
        help_text="Mínimo 8 caracteres. No puede ser muy común o completamente numérica."
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme la contraseña',
            'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
        }),
        label="Confirmar Contraseña",
        required=True,
        help_text="Ingrese la misma contraseña para verificación."
    )

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={
            "class": "w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 h-32",
            "multiple": "multiple"
        }),
        required=False,
        label="Grupos",
        help_text="Mantenga presionado Ctrl (Cmd en Mac) para seleccionar múltiples grupos."
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'dni',
            'direction', 'phone', 'image',
            'is_active', 'is_staff',
            'groups',
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre de usuario',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Ingrese los nombres',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Ingrese los apellidos',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Ingrese el correo electrónico',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
            }),
            'dni': forms.TextInput(attrs={
                'placeholder': 'Ingrese DNI/Cédula o RUC',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
            }),
            'direction': forms.TextInput(attrs={
                'placeholder': 'Ingrese la dirección',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Ingrese el teléfono',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500 focus:ring-2 transition-colors'
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500 focus:ring-2 transition-colors'
            }),
        }
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
            'dni': 'DNI/Cédula o RUC',
            'direction': 'Dirección',
            'phone': 'Teléfono',
            'image': 'Imagen de Perfil',
            'is_active': 'Activo',
            'is_staff': 'Personal de Administración (Staff)',
            'groups': 'Grupos',
        }
        help_texts = {
            'username': 'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.',
            'email': 'Ingrese una dirección de correo electrónico válida.',
            'dni': 'Documento de identidad único del usuario.',
            'direction': 'Dirección completa de residencia.',
            'phone': 'Número de teléfono de contacto.',
            'is_active': 'Designa si este usuario debe ser tratado como activo. Desmarque esto en lugar de borrar cuentas.',
            'is_staff': 'Designa si el usuario puede iniciar sesión en el sitio de administración y tiene permisos implícitos de staff.',
            'groups': 'Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos otorgados a cada uno de sus grupos.',
        }
        error_messages = {
            'username': {'unique': "Un usuario con ese nombre de usuario ya existe."},
            'email': {'unique': "Un usuario con ese correo electrónico ya existe."},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

        # Add custom validation attributes
        self.fields['password'].widget.attrs.update({
            'minlength': '8',
            'pattern': '^(?=.*[a-zA-Z])(?=.*\d).{8,}$',
            'title': 'La contraseña debe tener al menos 8 caracteres y contener letras y números'
        })

        # Make email required
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
        # Check for uniqueness if it's a new user or if the email has changed
        if self.instance and self.instance.pk:  # if updating
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Un usuario con este correo electrónico ya existe.")
        else:  # if creating
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Un usuario con este correo electrónico ya existe.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance and self.instance.pk:  # if updating
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Un usuario con este nombre de usuario ya existe.")
        else:  # if creating
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Un usuario con este nombre de usuario ya existe.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            # Basic password validation
            if len(password) < 8:
                raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
            if password.isdigit():
                raise forms.ValidationError("La contraseña no puede ser completamente numérica.")
            if password.lower() in ['password', '12345678', 'qwerty', 'abc123']:
                raise forms.ValidationError("La contraseña es muy común.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:  # Only set password if provided
            user.set_password(password)
        if commit:
            user.save()
            self.save_m2m()  # Important for saving ManyToMany fields like groups
        return user
