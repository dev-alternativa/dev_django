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