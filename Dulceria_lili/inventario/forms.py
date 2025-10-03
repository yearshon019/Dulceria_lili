from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Inventario
class InventarioForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=False)
    deleted_at = forms.DateTimeField(required=False)

    class Meta:
        model = Inventario
        fields = ["id_bodega", "id_lote", "id_producto"] 

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name and len(name) > 50:
            raise ValidationError("El nombre no puede tener más de 50 caracteres.")
        return name

    def clean_deleted_at(self):
        deleted_at = self.cleaned_data.get("deleted_at")
        if deleted_at and deleted_at < timezone.now():
            raise ValidationError("La fecha de eliminación no puede ser anterior a hoy.")
        return deleted_at













