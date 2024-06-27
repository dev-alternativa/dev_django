
/* Retorna para página de listagem do cadastro correspondente */
function goBack() {
  const urlPath = window.location.pathname;
  const dominio = window.location.origin
  let regex = /^\/([^/]+)/;
  let match = urlPath.match(regex);

  if(match){
    let textoCapturado = match[1];
    // console.log(`Texto: ${textoCapturado}`)
    window.location.href = `${dominio}/${textoCapturado}`;
  }else{
    console.log(`Texto não encontrado.`)
  }

}