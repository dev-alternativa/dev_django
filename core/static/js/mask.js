/* Funções para aplicar máscara em campos do tipo texto */


// Listener do input de CPF/CNPJ, verifica se o valor digitado é um CPF ou CNPJ

// Verifica quantidade de caracteres entrados e aplica a máscara conforme o tamanho
const input_cnpj_cpf = document.querySelector('input[name="cnpj"]');

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

