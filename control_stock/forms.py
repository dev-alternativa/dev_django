from django import forms
from django.forms import ModelForm 
from cadastro.models import ClienteFornecedor, Produto
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit, HTML
from crispy_forms.bootstrap import TabHolder, Tab, PrependedText, AppendedText, FieldWithButtons, StrictButton 
from crispy_bootstrap5.bootstrap5 import Switch
from django_select2.forms import Select2MultipleWidget, Select2Widget


