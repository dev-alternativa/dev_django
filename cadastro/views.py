

# ********************************* LISTAGENS  *********************************

# class LoteListView(ListView):
#   model = Lote
#   template_name = 'lote/lote.html'
#   context_object_name = 'itens_lote'

# ********************************* INCLUSÃO  *********************************

# class LoteNovoView(FormMessageMixin, CreateView):
#   model = Lote
#   form_class = LoteForm
#   template_name = 'lote/adicionar_lote.html'
#   success_url = reverse_lazy('lote')
#   success_message = 'Lote incluído com sucesso!'

# *********** ATUALIZAÇÃO ***********

# class LoteUpdateView(FormMessageMixin, UpdateView):
#   model = Lote
#   form_class = LoteForm
#   template_name = 'lote/update_lote.html'
#   success_url = reverse_lazy('lote')
#   success_message = 'Lote atualizado com sucesso!'


# class LoteDeleteView(DeleteSuccessMessageMixin, DeleteView):
#   model = Lote
#   template_name = "lote/delete_lote.html"
#   success_url = reverse_lazy("lote")

# ********************** VISUALIZAÇÃO DE ITENS **********************

# class LoteDetailView(DetailView):
#   model = Lote
#   template_name = 'lote/visualizar_lote.html'

