/************************  VALIDAÇÕES DO FORMULÁRIO   ************************/


const validaCPF = (cpf) => {
  /**
   * Valida CPF
   * @param {string} cpf - String com o CPF
   * @returns {boolean}
   */
  cpf = cpf.replace(/[^\d]/g, '');
  // Verifica se tem 11 dígitos numéricos
  if (cpf.length !== 11) {
    return false;
  }
  // Verifica se todos os dígitos são iguais, o que não é válido para o CPF
  if (/^(\d)\1{10}$/.test(cpf)) {
    return false;
  }
  // Validação usando algoritmo do próprio CPF
  let soma = 0;
  let resto;
  for (let i = 1; i <= 9; i++) {
    soma = soma + parseInt(cpf.substring(i - 1, i)) * (11 - i);
  }
  resto = (soma * 10) % 11;

  if ((resto === 10) || (resto === 11)) {
    resto = 0;
  }
  if (resto !== parseInt(cpf.substring(9, 10))) {
    return false;
  }

  soma = 0;
  for (let i = 1; i <= 10; i++) {
    soma = soma + parseInt(cpf.substring(i - 1, i)) * (12 - i);
  }
  resto = (soma * 10) % 11;

  if ((resto === 10) || (resto === 11)) {
    resto = 0;
  }
  if (resto !== parseInt(cpf.substring(10, 11))) {
    return false;
  }
  return true;
}


const validaCNPJ = (cnpj) => {
  /**
   * Valida CNPJ
   * @param {string} cnpj - String com o CNPJ
   * @returns {boolean}
   */
  cnpj = cnpj.replace(/[^\d]/g, '');
  // Verifica se o CNPJ tem 14 dígitos numéricos
  if (cnpj.length !== 14) {
    return false;
  }
  // Valida CNPJ usando algoritmo
  if (cnpj.length !== 14) {
    return false;
  }

  // Validação do CNPJ usando algoritmo
  let tamanho = cnpj.length - 2;
  let numeros = cnpj.substring(0, tamanho);
  let digitos = cnpj.substring(tamanho);
  let soma = 0;
  let pos = tamanho - 7;
  for (let i = tamanho; i >= 1; i--) {
    soma += numeros.charAt(tamanho - i) * pos--;
    if (pos < 2) {
      pos = 9;
    }
  }
  let resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
  if (resultado !== parseInt(digitos.charAt(0))) {
    return false;
  }

  tamanho = tamanho + 1;
  numeros = cnpj.substring(0, tamanho);
  soma = 0;
  pos = tamanho - 7;
  for (let i = tamanho; i >= 1; i--) {
    soma += numeros.charAt(tamanho - i) * pos--;
    if (pos < 2) {
      pos = 9;
    }
  }
  resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
  if (resultado !== parseInt(digitos.charAt(1))) {
    return false;
  }

  return true;
}



const validaCampoCPFCNPJ = (input) => {
  /**
   * Valida CPF/CNPJ
   * @param {HTMLInputElement} input - Input com o CPF/CNPJ
   */
  const inputCPFCNPJ = input.value.trim().replace(/[.]|[-]|[\/]/g, '');
  const errorElement = document.getElementById(`${input.id}-error`);
  let inputValido = false;
  const inputFieldCNPJ = $('#id_cnpj');

  // Verifica retorno de CPF ou CNPJ válido
  if (inputCPFCNPJ.length === 11) {
    inputValido = validaCPF(inputCPFCNPJ);
  } else if (inputCPFCNPJ.length === 14) {
    if (!inputFieldCNPJ.prop(':disabled')) {
      inputValido = validaCNPJ(inputCPFCNPJ);
    }

  }
  // Se CPF ou CNPJ for invalido, aplica o aviso
  if (!inputValido) {
    input.classList.add('is-invalid');
    if (!errorElement) {
      const newErrorElement = document.createElement('div');
      newErrorElement.id = `${input.id}-error`;
      newErrorElement.className = 'invalid-feedback show';
      newErrorElement.innerText = 'CPF/CNPJ inválido, digite um CPF válido';
      input.parentNode.appendChild(newErrorElement);
      input.focus();
    } else {
      errorElement.innerText = 'CPF/CNPJ inválido, digite um CPF válido.';
      errorElement.classList.add('show');
    }

  } else {
    input.classList.remove('is-invalid')
    if (errorElement) {
      errorElement.classList.remove('show');
      errorElement.innerText = '';
    }
  }
};



/* Valida campos obrigatórios em abas inativas  */
document.addEventListener('DOMContentLoaded', function () {
  // Captura o formulário
  const form = document.getElementsByClassName('form_fill_content');

  if (form[0]) {

    // Captura todas as abas
    const tabs = document.querySelectorAll('.nav-link');
    // captura os paineis das abas
    const tabPanes = document.querySelectorAll('.tab-pane');

    // Remove `required` dos campos em abas inativas ao carregar a página
    tabPanes.forEach(tabPane => {
      if (!tabPane.classList.contains('active')) {
        const inputs = tabPane.querySelectorAll('[required]');
        inputs.forEach(input => {
          input.dataset.required = 'true';
          input.removeAttribute('required');
        });
      }
    });

    // Adiciona/remove `required` mudar de aba
    tabs.forEach(tab => {
      tab.addEventListener('show.bs.tab', function (event) {
        const targetTabPane = document.querySelector(event.target.getAttribute('href'));
        const previousTabPane = document.querySelector(event.relatedTarget.getAttribute('href'));

        // Adiciona `required` ao mudar de aba
        const activeInputs = targetTabPane.querySelectorAll("[data-required='true']");
        activeInputs.forEach(input => {
          input.setAttribute('required', 'true');
        })

        // Remove `required dos campos da aba inativa
        const inactiveInputs = previousTabPane.querySelectorAll('[required]');
        inactiveInputs.forEach(input => {
          input.removeAttribute('required');
        });
      });
    });

    // Valida o formulário na submissão
    form[0].addEventListener('submit', function (event) {
      if (!form[0].checkValidity()) {
        event.preventDefault();
        event.stopPropagation();

        // Encontra o primeiro campo inválido
        const firstinvalidField = form[0].querySelector(':invalid');

        if (firstinvalidField) {
          // Econtra a aba que contém o campo inválido
          const invalidFieldTabPane = firstinvalidField.closest('.tab-pane');
          if (invalidFieldTabPane) {
            const tabId = invalidFieldTabPane.id;
            // Ativa a aba correspondente
            const tabToActivate = document.querySelector(`a[href="#${tabId}"]`);
            if (tabToActivate) {
              $(tabToActivate).tab('show');
            }
          }

          // Define o foco no primeiro campo inválido após a aba ser ativada
          firstinvalidField.focus();
        }
      }
      form[0].classList.add('was-validated');
    }, false);
  }
});


