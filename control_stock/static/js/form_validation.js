
/* Valida campos que recebem apenas valores numéricos */
const validateForm = () => {
  const inputs = document.querySelectorAll('.validate-number');
  for (let i = 0; i < inputs.length; i++) {
    if(!isNumeric(inputs[i].value)){
      alert(`O campo ${inputs[i].name} deve conter apenas números.`);
      inputs[i].focus();
      return false;
    }
  }
  return true;
};
/* Testa se argumento é um número */
const isNumeric = (value) => {
  return /^\d+$/.test(value);
}

/* Verifica se está na rota de adicionar produto para acionar
o a verificação do formulário */
const url_path = window.location.pathname;

if(url_path == '/produto/adicionar/'){
  document.getElementById("formAddProduto").addEventListener("submit", (event) => {
    if (!validateForm()) {
      event.preventDefault();
    }  
  } );
}