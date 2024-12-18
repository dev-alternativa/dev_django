$(document).ready(() => {
  /* Calcula metro quadrado do produto baseado no tipo da categoria */
  const calculaArea = () => {
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

  $('#id_largura, #id_comprimento').on('input', calculaArea);
  $('#id_tipo_categoria').on('change', calculaArea);

  /* Bloqueia o campo CNPJ quando o fornecedor for estrangeiro */
  const bloqueiaInputCNPJ = () => {
    const switchInternacional = $('#id_is_international');
    const cnpjInput = $('#id_cnpj');
    const btn_consulta_cnpj = $('#btn_consulta_cnpj');

    if (switchInternacional.is(':checked')) {
      cnpjInput.val('');
      cnpjInput.prop('disabled', true);
      btn_consulta_cnpj.prop('disabled', true);
    }
  }

  $('#id_is_international').on('change', bloqueiaInputCNPJ);

  // Ativa tooltip
  $(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });

});