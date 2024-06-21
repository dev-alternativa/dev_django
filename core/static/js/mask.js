/* Funções para aplicar máscara em campos do tipo texto */


// Para input de valor monetários
// Acrescenta vírgula e dois 0 caso não exista vírgula
// Acrescemta um 0 caso exista apenas 1 casa decimal
const formataValorMonetario = (input) => {
  let valor = input.value.trim();


  if (valor.includes(',')){
    let partes = valor.split(',');
    let parteInteira = partes[0];
    let parteDecimal = partes[1];


    if(parteDecimal.length === 1){
      input.value = `${parteInteira},${parteDecimal}0`;
    }else{
      input.value = valor;
    }
  }else{
    input.value = `${valor},00`;
  }
}

const numericOnlyInput = document.querySelector('.numericValorOnly');
if(numericOnlyInput != undefined){

  const removeNonNumericChar = (input) => {
    input.addEventListener('input', () => {
      let valor = input.value.replace(/D/, '');
      return valor;
    });
  }

  removeNonNumericChar(numericOnlyInput);
}


// Listener do input de CPF/CNPJ, verifica se o valor digitado é um CPF ou CNPJ
// Verifica quantidade de caracteres entrados e aplica a máscara conforme o tamanho
const input_cnpj_cpf = document.querySelector('input[name="cnpj"]');
if (input_cnpj_cpf != undefined){

  const applyMask = (input) => {
    input.addEventListener('input', () => {
      let value = input.value.replace(/\D/, '');
      if (value.length <=14 ){
        input.value = cpfMask(value);
      }else{
        input.value = cnpjMask(value);
      }
    });
  };
  
  // Máscara para CPF
  const cpfMask = (value) => {
    return value
      .replace(/\D/g, '') //Remove todos os caracteres não numéricos
      .replace(/(\d{3})(\d)/, '$1.$2') // Adiciona ponto após os três primeiros dígitos
      .replace(/(\d{3})(\d)/, '$1.$2') // Adiciona ponto após os seis primeiros dígitos
      .replace(/(\d{3})(\d{1,2})$/, '$1-$2'); // Adiciona hífen após os nove primeiros dígitos
  }
  
  // Máscara para CNPJ
  const cnpjMask = (value) => {
    return value
      .replace(/\D/g, '') // remove todos os caracteres não numéricos
      .replace(/(\d{2})(\d)/, '$1.$2') // Adiciona ponto após os dois primeiros dígitos
      .replace(/(\d{3})(\d)/, '$1.$2') // Adiciona ponto após os cinco primeiros dígitos
      .replace(/(\d{3})(\d)/, '$1/$2') // Adiciona barra após os oito primeiros dígitos
      .replace(/(\d{4})(\d{1,2})$/, '$1-$2'); // Adiciona hífen após os doze primeiros dígitos
  }
  
  // Aplica a função da máscara
  applyMask(input_cnpj_cpf);
}

