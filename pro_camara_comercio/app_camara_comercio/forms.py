# core/forms.py

from django import forms
from .models import Afiliado, Contacto, DocumentosAfiliado, Solicitud



class LoginForm(forms.Form):
    """
    Formulario personalizado para el inicio de sesión.
    No se conecta a un modelo, solo valida la entrada del usuario.
    """
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Correo Electrónico',
            'autocomplete': 'email'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Contraseña',
            'autocomplete': 'current-password'
        })
    )

# --- FORMULARIOS DE CREACIÓN Y CONTACTO ---

class AfiliadoCreationForm(forms.ModelForm):
    """
    Formulario para la creación de nuevos afiliados, con widgets y clases de Bootstrap.
    """
    class Meta:
        model = Afiliado
        fields = [
            'first_name', 'last_name', 'email', 'telf', 'cedula', 'password',
            'tipo_plan', 'razon_social', 'nombre_comercial', 'RUC', 
            'direccion', 'ciudad', 'tipo_negocio', 'nombre_representante_legal', 
            'cedula_representante', 'red_social_preferida', 'acepta_terminos'
        ]

        widgets = {
            # Asignamos la clase 'form-control' de Bootstrap a todos los campos.
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pérez'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'telf': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Crea una contraseña segura'}),
            'tipo_plan': forms.Select(attrs={'class': 'form-select'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'form-control'}),
            'RUC': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_negocio': forms.Select(attrs={'class': 'form-select'}),
            'nombre_representante_legal': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula_representante': forms.TextInput(attrs={'class': 'form-control'}),
            'red_social_preferida': forms.Select(attrs={'class': 'form-select'}),
            'acepta_terminos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'first_name': 'Nombres', 'last_name': 'Apellidos', 'email': 'Correo Electrónico de Contacto',
            'telf': 'Teléfono de Contacto', 'password': 'Crea tu Contraseña',
            'RUC': 'RUC (Registro Único de Contribuyentes)',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class ContactoForm(forms.ModelForm):
    """
    Formulario para la página de contacto con clases de Bootstrap.
    """
    class Meta:
        model = Contacto
        fields = ['nombre_completo', 'correo_electronico', 'telefono', 'empresa', 'asunto', 'mensaje', 'acepto_politicas']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'asunto': forms.Select(attrs={'class': 'form-select'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe tu consulta aquí...'}),
            'acepto_politicas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# --- FORMULARIOS PARA SOCIOS ACTIVOS ---

class DocumentosAfiliadoForm(forms.ModelForm):
    """
    Formulario para que un afiliado suba o actualice sus documentos.
    """
    class Meta:
        model = DocumentosAfiliado
        # Excluimos el campo 'afiliado' porque se asignará automáticamente en la vista.
        exclude = ['afiliado']
        widgets = {
            'titular_nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'titular_telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'titular_cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'beneficiario_nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'beneficiario_porcentaje': forms.NumberInput(attrs={'class': 'form-control'}),
            'copia_ruc': forms.FileInput(attrs={'class': 'form-control'}),
            'copia_cedula': forms.FileInput(attrs={'class': 'form-control'}),
            'copia_nombramiento': forms.FileInput(attrs={'class': 'form-control'}),
            'firma_electronica': forms.FileInput(attrs={'class': 'form-control'}),
            'consentimiento_datos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SolicitudForm(forms.ModelForm):
    """
    Formulario para que un afiliado cree una nueva solicitud de servicio.
    """
    class Meta:
        model = Solicitud
        # El afiliado y el estado se gestionan en la vista.
        fields = ['servicio_especifico', 'descripcion']
        widgets = {
            'servicio_especifico': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Añade detalles o comentarios sobre tu solicitud aquí.'}),
        }
        labels = {
            'servicio_especifico': 'Selecciona el Servicio o Beneficio que deseas solicitar',
            'descripcion': 'Descripción Adicional (Opcional)',
        }

class AfiliadoUpdateForm(forms.ModelForm):
    """
    Formulario para que un socio actualice su información de perfil.
    """
    class Meta:
        model = Afiliado
        # Seleccionamos los campos que el usuario SÍ puede modificar
        fields = [
            'first_name', 'last_name', 'telf', 'cedula',
            'razon_social', 'nombre_comercial', 'RUC', 
            'direccion', 'ciudad', 'nombre_representante_legal', 
            'cedula_representante', 'red_social_preferida'
        ]
        
        # Widgets con clases de Bootstrap para un diseño consistente
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'telf': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'form-control'}),
            'RUC': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_representante_legal': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula_representante': forms.TextInput(attrs={'class': 'form-control'}),
            'red_social_preferida': forms.Select(attrs={'class': 'form-select'}),
        }

class SocioForm(forms.ModelForm):
    class Meta:
        model = Afiliado
        fields = [
            'tipo_plan',
            'nombre_comercial',
            'RUC',
            'razon_social',
            'nombre_representante_legal',
            'cedula_representante',
            'fecha_visita',
            'red_social_preferida',
            'direccion',
            'ciudad',
            'tipo_negocio',
            'acepta_terminos',
        ]
        widgets = {
            'tipo_plan': forms.Select(attrs={'class': 'form-control'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'form-control'}),
            'RUC': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_representante_legal': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula_representante': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_visita': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'red_social_preferida': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_negocio': forms.Select(attrs={'class': 'form-control'}),
            'acepta_terminos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_acepta_terminos(self):
        acepta = self.cleaned_data.get("acepta_terminos")
        if not acepta:
            raise forms.ValidationError("Debes aceptar los términos y condiciones.")
        return acepta