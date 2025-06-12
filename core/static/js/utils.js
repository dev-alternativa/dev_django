// TEMPORIZADOR DE ALERTS DE AVISO NAS PÁGINAS
document.addEventListener('DOMContentLoaded', function () {
  // Selecione todos os alertas na página
  const alerts = document.querySelectorAll('.alert');

  // Para cada alerta encontrado
  alerts.forEach(alert => {
    if (alert.classList.contains('not-fade')) {
      return;
    }

    // Defina um tempo de espera de 3 segundos (3000 milissegundos)
    setTimeout(() => {
      // Adicione a classe 'fade' para iniciar a transição de desvanecimento
      alert.classList.remove('show');
      alert.classList.add('fade');

      // Após a transição, remova o alerta do DOM
      setTimeout(() => {
        alert.remove();
      }, 150);  // Tempo de transição para o fade (pode ajustar conforme a necessidade)
    }, 6000);  // 3 segundos
  });
});

const messageBox = (titulo, mensagem) => {
  /**
   * Cria um modal de mensagem com o título e o conteúdo informado
   * @param {string} titulo - Título do modal
   * @param {string} mensagem - Mensagem do modal
   * @return {Promise} Promise do clique no botão OK
   */
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

const configProductFormLabels = (categoryID) => {
    /**
      Configura os campos do formulário de adição de produtos
      @param {int} categoryID - ID da categoria do produto
    */
    const categoriesByPiece = [2, 5, 6, 7, 8, 9];
    const categoriaMMporM = [2, 3, 4, 8];

    const rollDescription = [3, 4];
    const plateDescription = [6, 7];

    const enabledFields = [3, 4, 9, 10]
    const isMMporM = categoriaMMporM.includes(categoryID);
    const isRoll = rollDescription.includes(categoryID);
    const isPiece = categoriesByPiece.includes(categoryID);
    const isEnabled = enabledFields.includes(categoryID);

    // Oculta campo m2 se categoria for lâminas
    const $parentId_m2 = $("#id_m2").parent();
    if(categoryID === 8){
      $parentId_m2.addClass("d-none");
    }else{
      $parentId_m2.removeClass("d-none");
    }

    // Desativa edição do campo Item #
    $("#id_item_pedido").prop('disabled', true);

    // Configura se label é `Comp. (m)` ou `Comp. (mm)`
    $("#div_id_comprimento label").text(isMMporM ? 'Comp. (m)' : 'Comp. (mm)');
    // Configura se label é `Preço / m² (R$)` ou `Preço pç (R$)`
    $("#div_id_preco label").text(isPiece ? 'Preço pç (R$)' : 'Preço / m² (R$)');
    // Configura se input text é habilitado
    $('#id_comprimento').prop('disabled', !isEnabled);
    $('#id_largura').prop('disabled', !isEnabled);

  }

function calcProductFieldsArea(m2){
    /**
      Calcula metragem no modal de adição de produtos dependendo da categoria
    */
    categoryID = $("#hidden_categoria_id").val();

    const $quantidade = $('#id_quantidade');
    const $largura = $('#id_largura');
    const $comprimento = $('#id_comprimento');
    const $preco = $('#id_preco');
    const $m2_total = $('#id_m2');
    const initialArea = m2 && m2 != 0 ? parseFloat(m2) : 1;
    const $total = $('#id_total_preco');
    const $cnpjFaturamento = $('#id_cnpj_faturamento');

    /*
    [$largura, $comprimento, $preco].forEach(field => {
      const value = field.val();
      if(value && !isNaN(parseFloat(value))){
        field.val(parseFloat(value).toFixed(2));
      }
    });
    */
    const $inputs = [
      $quantidade,
      $largura,
      $comprimento,
      $preco,
      $cnpjFaturamento
    ];
    const requiredCategories = [3, 4];
    let $requiredInputs = [$quantidade, $preco];

    if(requiredCategories.includes(parseInt(categoryID))){
      $requiredInputs.push($largura, $comprimento);
    }

    productName = $('#nome_produto').text();

    // Obtém os valores dos campos obrigatórios
    const requiredValues = $requiredInputs.map(i => {
      const value = parseFloat(i.val());
      return !isNaN(value) && value > 0 ? value : null;
    });

    // Verifica se todos os calores são diferentes de 0
    const allValid = requiredValues.every(value => value !== null);

    if(!allValid){
      return;
    }

    // Obtém todos os valores (inclusive os opcionais, como metragem)
    const valores = $inputs.map(i => parseFloat(i.val()) || 0);
    // Executa o calculo
    const result = calculateProductValuesByCategory(
      parseInt(categoryID),
      valores,
      productName,
      initialArea,
    );

    // Quando lâmina, comprimento sempre é igual à quantidade
    $comprimento.val(categoryID == 8 ? $quantidade.val(): $comprimento.val());

    // Atualiza campos do form
    $("#id_dados_adicionais_item").val(result.dados_descritivo);
    $("#id_obs").val(result.dados_descritivo);
    $total.val(result.total_valor);
    $m2_total.val(result.area_total);

  }


$(document).ready(function () {

  /* BARRA DE PROGRESSO DE UPLOAD */
  $('#upload-form').on('submit', function (event) {
    $('#loading').show();
    $('#overlay').show();
  });

});
/** Escurece os selectbox com Select2 que não escurecem com o modal */
function aplicarEscurecimento(modal) {
  $('.select2-container').removeClass('escurecer');
  $('.select2-container').not($(modal).find('.select2-container')).addClass('escurecer');
}

// Remover tabindex após exibir o modal (já está OK em seu código)
$('.modal').on('shown.bs.modal', function () {
  $(this).removeAttr('tabindex');
  aplicarEscurecimento(this);
});

// Quando qualquer modal fechar, limpa tudo
$('.modal').on('hidden.bs.modal', function () {
  $('.select2-container').removeClass('escurecer');
});
