from django import forms
import re


ALFANUM_ESPACIOS = re.compile(r"^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ ]+$")
SOLO_LETRAS_ESPACIOS = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$")


class CapturaUsuarioForm(forms.Form):
    nomina = forms.CharField(max_length=30, required=True)
    nombre = forms.CharField(max_length=120, required=True)
    cantidad_videos = forms.IntegerField(min_value=1, required=True)

    def clean_nomina(self):
        v = self.cleaned_data["nomina"].strip()
        if not v:
            raise forms.ValidationError("Error: Nómina no puede estar vacía.")
        if not re.fullmatch(r"[A-Za-z0-9]+", v):
            raise forms.ValidationError("Error: Nómina debe ser alfanumérica (solo letras y números, sin espacios).")
        return v

    def clean_nombre(self):
        v = self.cleaned_data["nombre"].strip()
        if not v:
            raise forms.ValidationError("Error: Nombre no puede estar vacío.")
        if not SOLO_LETRAS_ESPACIOS.fullmatch(v):
            raise forms.ValidationError("Error: Nombre debe contener solo letras y espacios (sin números ni símbolos).")
        v = re.sub(r"\s+", " ", v).strip()
        return v


class VideoForm(forms.Form):
    titulo = forms.CharField(max_length=120, required=True)
    nombre = forms.CharField(max_length=120, required=True)
    extension = forms.CharField(max_length=20, required=True)
    tamano_mb = forms.DecimalField(min_value=0.1, max_value=3, decimal_places=1, max_digits=4, required=True)

    def _alfanum_ok(self, campo: str, valor: str):
        v = valor.strip()
        if not v:
            raise forms.ValidationError(f"Error: {campo} no puede estar vacío.")
        if not ALFANUM_ESPACIOS.fullmatch(v):
            raise forms.ValidationError(
                f"Error: {campo} debe ser alfanumérico (letras/números) y puede incluir espacios, sin símbolos."
            )
        v = re.sub(r"\s+", " ", v).strip()
        return v

    def clean_titulo(self):
        return self._alfanum_ok("Título", self.cleaned_data["titulo"])

    def clean_nombre(self):
        return self._alfanum_ok("Nombre del video", self.cleaned_data["nombre"])

    def clean_extension(self):
        return self._alfanum_ok("Extensión", self.cleaned_data["extension"])

    def clean_tamano_mb(self):
        v = self.cleaned_data["tamano_mb"]
        if v > 3:
            raise forms.ValidationError("Error: Tamaño (MB) excede el máximo permitido (3MB).")
        return v