/* FUNÇÕES PARA APLICAR MÁSCARA EM CAMPOS DO TIPO TEXTO */


// substitui `.` por `,` nos inputs
document.addEventListener('DOMContentLoaded', function () {

  // só é disparada na rota de update
  if (window.location.pathname.includes('update')) {
    // Função para substituir ponto por vírgula
    function formatDecimal(value) {
        return value.replace(/\./g, ',');
    }
  
    // Seleciona os inputs que precisam de formatação
    const decimalInputs = document.querySelectorAll('input');
    if(decimalInputs){
      // Aplica a formatação aos valores dos inputs que tenham a classe money
      decimalInputs.forEach(input => {
          if (input.classList.contains("money")) {
            if(input.value.includes('.')){
              input.value = formatDecimal(input.value);
            }
          }
      });
    }
  }
});


// Lida com diferentes tipos de campos numéricos: Apenas númerico, números e a vírgula
const removeNaoNumerico = (input) => {
  input.addEventListener('input', () => {
    let valor = input.value.trim();
    if (input.classList.contains('money')) {
      valor = valor.replace(/[^0-9,]/g, ''); // Permitir apenas números e vírgula
      input.value = valor;
    } else {
      valor = valor.replace(/\D/g, ''); // Remover caracteres não numéricos
      input.value = valor;
    }
  });
};


/** FORMATACAO DE VALORES MONETÁRIOS EM CAMPOS INPUT **/
/*****************************************************************************************/
const formataPeso = (input) => {
  
}



// Chamada quando campo monetario perder o foco
const formataValorMonetario = (input) => {
  const formatValue = () => {
    // remove espaços
    let valor = input.value.trim();
    
    // verifica se existe ','
    if (valor.includes(',')) {
      // se existir, separa as partes decimal e inteira
      let partes = valor.split(',');
      let partInteira = partes[0];
      let parteDecimal = partes[1] || '';

      // Verifica quantas casas decimais existem
      if (parteDecimal.length === 0) {
        if(partInteira.length === 0 || !partInteira){
          input.value = `0,00`;
        }else{
          // Acrescenta 2 '0' caso não existam valores após a vírgula
          input.value = `${partInteira},00`;
        }
        
      } else if(parteDecimal.length === 1){
        
        // acrescenta 1 '0' caso só exista 1 casa decimal
        input.value = `${partInteira},${parteDecimal}0`;
      }else{

        // garante a existencia de apenas 2 casas decimais, sempre removerá o última caractere digitado além das 2 casas, inclusive uma segunda ','
        input.value = `${partInteira},${parteDecimal.slice(0, 2)}`;
      }
    } else {
      //  não existindo vírgula, acrescenta 2 casas decimais com 2 '0'
      if (!valor) {
        input.value = `0,00`;
      } else {
        input.value = `${valor},00`;
      }
    }
  };
  // evento de perder o foco e execução da função
  input.addEventListener('blur', formatValue);
};


/** RESTRIÇÃO DE VALORES NUMÉRICOS EM CAMPOS INPUT **/
/*****************************************************************************************/

// Verifica todos os campos dos formulários que possam ser numericos e/ou monetários
document.addEventListener('DOMContentLoaded', () => {
  const inputs = document.querySelectorAll("input");
  inputs.forEach(input => {
    if (input.classList.contains('numericValorOnly')) {
      removeNaoNumerico(input); // Garante que apenas números e vírgula sejam permitidos
    }
    if (input.classList.contains('money')) {
      removeNaoNumerico(input);
      formataValorMonetario(input); // Formata o valor ao perder o foco
    }
  });
});


/** MASCARÁ PARA CNPJ e CPF **/
/*****************************************************************************************/

// Listener do input de CPF/CNPJ, verifica se o valor digitado é um CPF ou CNPJ
// Verifica quantidade de caracteres entrados e aplica a máscara conforme o tamanho
const input_cnpj_cpf = document.querySelector('input[name="cnpj"]');
if (input_cnpj_cpf){

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

