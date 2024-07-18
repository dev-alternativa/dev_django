// TEMPORIZADOR DE ALERTS DE AVISO NAS PÁGINAS
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
      }, 6000);  // 3 segundos
  });
});


/* MESSAGE BOX CUSTOMIZADA */
const messageBox = (titulo, mensagem) => {
  return new Promise((resolve) => {
    // Personaliza Título do message box
    const modalTitulo = document.getElementById("staticBackdropLabel");
    modalTitulo.textContent = titulo;
  
    // Personaliza conteúdo do message box
    const modalCorpo = document.querySelector('#staticBackdrop .modal-body');
    modalCorpo.innerHTML = `<p>${mensagem}</p>`;
  
    //  retornar true caso `Ok` seja clicado
    const btnOk = document.getElementById('btnOK');
    
    // resolve a Promise do clique no botão OK
    const handleOkClick = () => {
      resolve(true);
      btnOk.removeEventListener('click', handleOkClick);
      messageBox.hide();
    };

    btnOk.addEventListener('click', handleOkClick);
    // Mostra modal do message box
    const messageBox = new bootstrap.Modal(document.getElementById('staticBackdrop'), { keyboard: false });
    messageBox.show();

  });

};



/* Retorna para página de listagem do cadastro correspondente */
function goBack() {
  window.history.back();
// const urlPath = window.location.pathname;
// const dominio = window.location.origin
// let regex = /^\/([^/]+)/;
// let match = urlPath.match(regex);

// if(match){
//   let textoCapturado = match[1];
//   // console.log(`Texto: ${textoCapturado}`)
//   window.location.href = `${dominio}/${textoCapturado}`;
// }else{
//   console.log(`Texto não encontrado.`)
// }

}

/* BARRA DE PROGRESSO */
$(document).ready(function() {
  $('#upload-form').on('submit', function(event) {
    $('#loading').show();
    $('#overlay').show();
  });
});