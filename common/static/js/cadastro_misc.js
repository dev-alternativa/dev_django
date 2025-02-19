$(document).ready(() => {
  /**
   * Calcula a área do produto com base na largura, comprimento e categoria.
   *
   * Esta função realiza as seguintes etapas:
   * 1. Obtém os valores de largura, comprimento e categoria dos campos do formulário.
   * 2. Verifica se os valores de largura e comprimento são números válidos e se a categoria está selecionada.
   * 3. Calcula a área com base na categoria:
   *    - Para a categoria "Nyloflex", a área é arredondada para o inteiro mais próximo.
   *    - Para a categoria "Nyloprint", a área é arredondada para duas casas decimais.
   *    - Para outras categorias, a área é arredondada para duas casas decimais.
   * 4. Atualiza o campo de área no formulário com o valor calculado ou exibe uma mensagem de erro se os valores forem inválidos.
   *
   * @function
   * @name calcArea
   */
  const calcArea = () => {
    let largura = parseFloat($('#id_largura').val());
    let comprimento = parseFloat($('#id_comprimento').val());
    let categoria = $('#id_tipo_categoria').val();
    let area = 0

    if (!isNaN(largura) && !isNaN(comprimento) && categoria) {
      if (categoria === "Nyloflex") {
        area = Math.floor(largura * comprimento / 1000000);
      } else if (categoria === "Nyloprint") {
        area = math.floor(largura * comprimento / 1000000 * 100) / 100; //arredondar para 2 casas decimais
      } else {
        area = Math.floor(largura * comprimento / 1000 * 100) / 100; // arredonda para 2 casas decimais
      }

      $('#id_m_quadrado').val(area.toFixed(2));

    } else {
      $('#id_m_quadrado').val('Informe "Largura", "Comprimento" e a "Categoria"');
    }
  }

  $('#id_largura, #id_comprimento').on('input', calcArea);
  $('#id_tipo_categoria').on('change', calcArea);

  /* Bloqueia o campo CNPJ quando o fornecedor for estrangeiro */
  const blockCNPJInput = () => {
    const switchInternacional = $('#id_is_international');
    const cnpjInput = $('#id_cnpj');
    const btn_consulta_cnpj = $('#btn_consulta_cnpj');

    if (switchInternacional.is(':checked')) {
      cnpjInput.val('');
      cnpjInput.prop('disabled', true);
      btn_consulta_cnpj.prop('disabled', true);
    }
  }

  $('#id_is_international').on('change', blockCNPJInput);

  // Ativa tooltip
  $(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });

});