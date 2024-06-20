
// TEMPORIZADOR DE MENSAGENS DE AVISO NAS PÁGINAS
document.addEventListener('DOMContentLoaded', function() {
  // Selecione todos os alertas na página
  const alerts = document.querySelectorAll('.alert');

  // Para cada alerta encontrado
  alerts.forEach(alert => {
      // Defina um tempo de espera de 3 segundos (3000 milissegundos)
      setTimeout(() => {
          // Adicione a classe 'fade' para iniciar a transição de desvanecimento
          alert.classList.remove('show');
          alert.classList.add('fade');

          // Após a transição, remova o alerta do DOM
          setTimeout(() => {
              alert.remove();
          }, 150);  // Tempo de transição para o fade (pode ajustar conforme a necessidade)
      }, 3000);  // 3 segundos
  });
});


// *** Funcão para os botões 'close' fecharem os alerts ***
// const handleClose = () => {
//   const alertDiv = closeButton.parentNode; // Captura a div pai de `alert`
//   //alertDiv.style.display = 'none'; // Esconde a div
//   alertDiv.remove(); // remove a dive do DOM
// }
// const closeButton = document.querySelector('.alert .btn-close');
// if (closeButton != undefined) {
//   closeButton.addEventListener('click', handleClose);
// }


// **** ACIONAR BOTÕES DE EDIÇÃO DE ITENS DA LISTA ****
// Qualquer um dos botões de edição clicados 
// redirecionará para a página de edição de dados com o ID correspondente
document.querySelectorAll('.btn-edit').forEach(function(button) {
  button.addEventListener('click', function() {
    const currentURL = window.location.pathname;
    
     /* CATEGORIA */
    if(/\/categoria\//.test(currentURL)){
      const categoriaId = this.getAttribute('data-categoria-id');
      const editUrl = `/categoria/${categoriaId}/update/`;
      window.location.href = editUrl;

      /* COORDENADA */
    }else if(/\/coordenada\//.test(currentURL)){
      const coordenadaId = this.getAttribute(`data-coordenada-id`);
      const editUrl = `/coordenada/${coordenadaId}/update/`;
      window.location.href = editUrl;

      /* PRAZO */
    }else if(/\/prazo\//.test(currentURL)){
      const prazoId = this.getAttribute('data-prazo-id');
      const editUrl = `/prazo/${prazoId}/update/`;
      window.location.href = editUrl;

      /* PRODUTO */
    }else if(/\/produto\//.test(currentURL)){
      const produtoId = this.getAttribute(`data-produto-id`);
      const editUrl = `/produto/${produtoId}/update/`;
      window.location.href = editUrl;

      /* SUB-CATEGORIA */
    }else if(/\/sub_categoria\//.test(currentURL)){
      const subCategoriaId = this.getAttribute('data-sub-categoria-id');
      const editUrl = `/sub_categoria/${subCategoriaId}/update/`;
      window.location.href = editUrl;

    /* TRANSPORTADORA */
    }else if(/\/transportadora\//.test(currentURL)){
      const transportadoraId = this.getAttribute(`data-transportadora-id`);
      const editUrl = `/transportadora/${transportadoraId}/update/`;
      window.location.href = editUrl;
        
      /* UNIDADE */
    }else if(/\/unidade\//.test(currentURL)){
      const unidadeId = this.getAttribute(`data-unidade-id`);
      const editUrl = `/unidade/${unidadeId}/update/`;
      window.location.href = editUrl;
    }
  });
});

// **** ACIONAR BOTÕES PARA DELETAR RESPECTIVO ITEM DA LISTA ****
// Qualquer um dos botões 'Apagar'da lista clicados
// perguntará se realmente deseja apagar e removerá o item atualizando 
// a lista
document.querySelectorAll('.btn-delete').forEach(function(button) {
  button.addEventListener('click', function() {
    const currentURL = window.location.pathname;
    
    /* CATEGORIA */
    if (/\/categoria\//.test(currentURL)) {
      const categoriaId = this.getAttribute('data-categoria-id');
      const deleteUrl = `/categoria/${categoriaId}/delete/`;
      window.location.href = deleteUrl;

      /* COORDENADA */
    }else if(/\/coordenada\//.test(currentURL)){
      const coordenadaId = this.getAttribute(`data-coordenada-id`);
      const deleteUrl = `/coordenada/${coordenadaId}/delete/`;
      window.location.href = deleteUrl;

      /* PRAZO */
    }else if(/\/prazo\//.test(currentURL)){
      const prazoId = this.getAttribute('data-prazo-id');
      const deleteUrl = `/prazo/${prazoId}/delete/`
      window.location.href = deleteUrl;

      /* PRODUTO */
    }else if(/\/produto\//.test(currentURL)){
      const produtoId = this.getAttribute(`data-produto-id`);
      const deleteUrl = `/produto/${produtoId}/delete/`;
      window.location.href = deleteUrl;

      /* SUB-CATEGORIA */
    }else if(/\/sub_categoria\//.test(currentURL)){
      const subCategoriaId = this.getAttribute('data-sub-categoria-id');
      const deleteUrl = `/sub_categoria/${subCategoriaId}/delete`;
      window.location.href = deleteUrl;

      /* TRANSPORTADORA */
    }else if(/\/transportadora\//.test(currentURL)){
      const transportadoraId = this.getAttribute(`data-transportadora-id`);
      const deleteUrl = `/transportadora/${transportadoraId}/delete/`;
      window.location.href = deleteUrl;

      /* UNIDADE */
    }else if(/\/unidade\//.test(currentURL)){
      const unidadeId = this.getAttribute('data-unidade-id');
      const deleteUrl = `/unidade/${unidadeId}/delete`;
      window.location.href = deleteUrl;

    }
  });
});
