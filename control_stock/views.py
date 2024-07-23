from pyexpat.errors import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import ListView
from .models import Estoque




class EstoqueListView(ListView):
  model = Estoque
  template_name = 'estoque/estoque.html'
  context_object_name = 'itens_estoque'
  