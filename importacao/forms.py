from django import forms


class UploadPrazoForm(forms.Form):
  file = forms.FileField(
    label="Importar Planilha",
      widget=forms.ClearableFileInput(attrs={
        'class': 'form-control'  # Classe Bootstrap para inputs de arquivos
      })
  )  