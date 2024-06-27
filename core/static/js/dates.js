/*  VALIDA DATA */

const validaData = (value) => {
  const regex = /^\d{4}-\d{2}-\d{2}$/;
  if (!value.match(regex)) {
    return false;
  }

  // Separação de cada parte da data, dia, mês e ano
  let partes = value.split('-');
  let ano = parseInt(partes[0], 10);
  let mes = parseInt(partes[1], 10);
  let dia = parseInt(partes[2], 10);

  // Verifica se os valores de ano, mês e dia são válidos
  if (ano < 1000 || ano > 3000 || mes == 0 || mes > 12) {
    return false;
  }

  let tamanhoMeses = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

  // Ajusta ano bissexto
  if (ano % 400 == 0 || (ano % 100 != 0 && ano % 4 ==0)) {
    tamanhoMeses[1] = 29;
  }

  // Verifica se o dia é válido para o mês
  return dia > 0 && dia <= tamanhoMeses[mes - 1];

};

// Verifica se foi informado uma data correta, é chamada quando o input perde o foco
const validaCampoData = (input) => {
  const inputData = document.getElementById('id_data_recebimento');
  const errorElement = document.getElementById(`${input.id}-error`);
  let dataValida = false;

  
  if (inputData) {
    dataValida = validaData(inputData.value);
  }

  if (!dataValida) {
    input.classList.add('is-invalid');
    if (!errorElement) {
      const newErrorElement = document.createElement('div');
        newErrorElement.id = `${input.id}-error`;
        newErrorElement.className = 'invalid-feedback show';
        newErrorElement.innerText = 'Data inválida, digite uma Data válida';
        input.parentNode.appendChild(newErrorElement);
        input.focus();
    }else{
      errorElement.innerText = 'Data inválida, digite uma Data válida.';
      errorElement.classList.add('show');
    }
  }else {
    input.classList.remove('is-invalid')
    if (errorElement) {
      errorElement.classList.remove('show');
      errorElement.innerText = '';
    }
  }

};