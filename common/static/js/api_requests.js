/* ****************************** Funções de chamadas de APIs ****************************** */

/**
 * Verifica a validade de um CNPJ e consulta seus dados em uma API pública.
 *
 * Esta função realiza as seguintes etapas:
 * 1. Limpa o CNPJ removendo caracteres não numéricos.
 * 2. Verifica se o CNPJ foi digitado.
 * 3. Verifica se o CNPJ tem 14 caracteres.
 * 4. Realiza uma requisição AJAX para consultar os dados do CNPJ.
 * 5. Atualiza o formulário com os dados retornados pela API.
 *
 * @function
 * @name checkCNPJ
 * @returns {boolean} Retorna false se o CNPJ for inválido ou se a requisição não puder ser realizada.
 */
const checkCNPJ = () => {
  let cnpj = $('#id_cnpj').val();
  let cleanedCNPJ = cnpj.replace(/[^\d]/g, '');
  const url = `/api/cnpj/${cleanedCNPJ}/`;

  let errorDivCNPJ = $('#id_cnpj-error');
  const btnConsultaCNPJ = $('#btn_consulta_cnpj');

  // Adiciona div de erro se ela não existir
  if (errorDivCNPJ.length === 0) {
    $('<div id="id_cnpj-error"></div>').insertAfter('.btn-primary');
    errorDivCNPJ = $('#id_cnpj-error');
  }

  // Verifica se foi digitado algum CNPJ
  if (cnpj.length === 0) {
    $('#id_cnpj').addClass('is-invalid');
    errorDivCNPJ.addClass('invalid-feedback show');
    errorDivCNPJ.text('Preencha um CNPJ');
  }

  // Verifica se o campo está validado para prosseguir com a request
  if ($('#id_cnpj').hasClass('is-invalid')) {
    return false;
  }

  // Se campo for menor que 14 caracteres não executa a request
  if (cleanedCNPJ.length < 14) {
    $('#id_cnpj').addClass('is-invalid');
    errorDivCNPJ.addClass('invalid-feedback show');
    errorDivCNPJ.text('Não é um CNPJ válido');
    return false;
  } else {
    // desativa o botão de consultar até que a requisição termine
    btnConsultaCNPJ.html('<span class="spinner-border spinner-border-sm" aria-hidden="true"></span> <span role="status">Aguarde...</span>');
    btnConsultaCNPJ.attr('disabled', true);

    $.ajax({
      url: url,
      method: 'GET',
      success: (data, jqXHR, textStatus) => {
        const dataResponse = data;

        btnConsultaCNPJ.html('Consultar CNPJ');
        btnConsultaCNPJ.attr('disabled', false);
        $('#id_cnpj').removeClass('is-invalid');
        errorDivCNPJ.text('')
        $('#id_cnpj').addClass('is-valid');

        // messageBox("Preenchimento de Dados?", "CNPJ encontrado e validado. Deseja usar os dados consultados para preencher o formulário?")
        if (dataResponse) {
          handleJSONCNPJ(dataResponse);
        } else {
          alert('Não foram encontrados dados para o CNPJ informado.');
        }

      },
      error: (err) => {
        $('id_cnpj').addClass('is-invalid');
        errorDivCNPJ.addClass('invalid-feedback show');
        btnConsultaCNPJ.html('Consultar CNPJ');
        btnConsultaCNPJ.attr('disabled', false);
        console.log(err);
        alert(`Ocorreu um erro {err.status}: ${err.statusText}`);
      }
    });
  }
};

/**
 * Verifica a validade de um CEP e consulta seus dados em uma API pública.
 *
 * Esta função realiza as seguintes etapas:
 * 1. Limpa o CEP removendo caracteres não numéricos.
 * 2. Verifica se o CEP tem 8 caracteres.
 * 3. Realiza uma requisição AJAX para consultar os dados do CEP.
 * 4. Atualiza o formulário com os dados retornados pela API.
 *
 * @function
 * @name checkCEP
 * @returns {boolean} Retorna false se o CEP for inválido ou se a requisição não puder ser realizada.
 */
const checkCEP = () => {

  let cep = $('#id_cep').val();
  let cleaned_cep = cep.replace(/[^\d]/g, '');
  const url = `/api/cep/${cleaned_cep}`;
  let errorDivCEP = $('#id_cep-error');
  const btnConsultaCEP = $('#btn_consulta_cep');

  // Adiciona div que conterá mensagem de erro, se ela não existir
  if (errorDivCEP.length === 0) {
    $('<div id="id_cep-error"></div>').insertAfter('.btn-warning');
    errorDivCEP = $('#id_cep-error');
  }

  if (cleaned_cep.length != 8) {
    $('#id_cep').addClass('is-invalid');
    errorDivCEP.addClass('invalid-feedback show');
    errorDivCEP.text('Não é um CEP Válido')
  } else {
    // Trava o botão de consulta com mensagem e muda texto do mesmo para 'Aguardando'
    btnConsultaCEP.html('<span class="spinner-border spinner-border-sm" aria-hidden="true"></span> <span role="status">Aguarde...</span>')
    btnConsultaCEP.attr('disabled', true);

    $.ajax({
      url: url,
      method: 'GET',
      success: (data, jqXHR, textStatus) => {
        const dataResponse = JSON.stringify(data);
        // console.log(dataResponse);
        btnConsultaCEP.html('Consultar CEP');
        btnConsultaCEP.attr('disabled', false);
        // caso não venha um status 200, gera erro e marca o campo CEP
        if (textStatus.status != 200) {
          $('#id_cep').addClass('is-invalid');
          errorDivCEP.addClass('invalid-feedback show');
          errorDivCEP.text('Não é um CEP Válido')
        } else {
          // se for válido, remove a classe de erro do campo CEP
          $('#id_cep').removeClass('is-invalid');
          errorDivCEP.text('')
          $('#id_cep').addClass('is-valid');

        }
      },
      error: (errorThrown, jqXHR, textStatus) => {
        // Caso eu CEP inválido seja inserido, cairá aqui
        // avisará o erro, e habilitará novamente o botão de consulta
        $('#id_cep').addClass('is-invalid');
        errorDivCEP.addClass('invalid-feedback show');
        errorDivCEP.text(`${errorThrown.responseJSON.message}`)
        btnConsultaCEP.html('Consultar CEP');
        btnConsultaCEP.attr('disabled', false);
      }
    });
  }
};

/**
 * Parse do JSON com os dados que serão utilizados para preencher o formulário.
 *
 * Esta função realiza as seguintes etapas:
 * 1. Extrai os dados relevantes do JSON retornado pela API.
 * 2. Popula os campos do formulário com os dados extraídos.
 *
 * @function
 * @name handleJSONCNPJ
 * @param {object} jsonData - Dados em formato JSON retornados pela API.
 */
const handleJSONCNPJ = (jsonData) => {

  const razao_social = (jsonData.razao_social) ? jsonData.razao_social : "";
  const nome_fantasia = (jsonData.estabelecimento.nome_fantasia) ? jsonData.estabelecimento.nome_fantasia : "";
  const cep = (jsonData.estabelecimento.cep) ? jsonData.estabelecimento.cep : "";
  const ddd1 = (jsonData.estabelecimento.ddd1) ? jsonData.estabelecimento.ddd1 : "";
  const bairro = (jsonData.estabelecimento.bairro) ? jsonData.estabelecimento.bairro : "";
  const numero = (jsonData.estabelecimento.numero) ? jsonData.estabelecimento.numero : "";
  const logradouro = (jsonData.estabelecimento.logradouro) ? jsonData.estabelecimento.logradouro : "";
  const complemento = (jsonData.estabelecimento.complemento) ? jsonData.estabelecimento.complemento : "";
  const telefone1 = (jsonData.estabelecimento.telefone1) ? jsonData.estabelecimento.telefone1 : "";
  const email = (jsonData.estabelecimento.email) ? jsonData.estabelecimento.email : "";
  const estado = (jsonData.estabelecimento.estado.sigla) ? jsonData.estabelecimento.estado.sigla : "";
  const cidade = (jsonData.estabelecimento.cidade.nome) ? jsonData.estabelecimento.cidade.nome : "";
  const inscricoes_estaduais = (jsonData.estabelecimento.inscricoes_estaduais) ? jsonData.estabelecimento.inscricoes_estaduais : "";

  // Elimina inscrições não ativas e coleta apenas a primeira encontrada
  let inscricaoAtiva = "";
  if (inscricoes_estaduais.length > 0) {
    let inscricoesAtivas = inscricoes_estaduais.filter(inscricao => inscricao.ativo)
    inscricaoAtiva = inscricoesAtivas[0].inscricao_estadual;
  }

  // Popula campos do formulário com os valores consultados
  $('#id_nome_fantasia').val(nome_fantasia);
  $('#id_razao_social').val(razao_social);
  $('#id_inscricao_estadual').val(inscricaoAtiva);
  $('#id_cep').val(cep);
  $('#id_endereco').val(logradouro);
  $('#id_complemento').val(complemento);
  $('#id_bairro').val(bairro);
  $('#id_numero').val(numero);
  $('#id_cidade').val(cidade);
  $('#id_estado').val(estado);
  $('#id_email').val(email);
  $('#id_ddd').val(ddd1);
  $('#id_telefone').val(telefone1);

};