/* ****************************** Funções de chamadas de APIs ****************************** */

// Consulta o CNPJ numa API pública
const consultarCNPJ = () => {
  let cnpj = $('#id_cnpj').val();
  let cleaned_cnpj = cnpj.replace(/[^\d]/g, '');
  const url = `/api/cnpj/${cleaned_cnpj}`;
  let erroDivCNPJ = $('#id_cnpj-error');
  const btnConsultaCNPJ = $('#btn_consulta_cnpj');

   // Adiciona div que conterá mensagem de erro, se ela não existir
  if (erroDivCNPJ.length === 0) {
    $('<div id="id_cnpj-error"></div>').insertAfter('.btn-primary');
    erroDivCNPJ = $('#id_cnpj-error');
  }

  // se não for um CNPJ, retorna erro, senão, faz a requisição da API
  if (cleaned_cnpj.length < 14) {
    $('#id_cnpj').addClass('is-invalid');
    erroDivCNPJ.addClass('invalid-feedback show');
    erroDivCNPJ.text('Não é um CNPJ válido')
  }else{
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
        erroDivCNPJ.text('')
        $('#id_cnpj').addClass('is-valid');
        messageBox("Preenchimento de Dados?", "Deseja usar os dados consultados para preencher o formulário?")
        .then((result) => {
          if(result){
            tratarJSONCNPJ();
          }
        });
      },
      error: (err) => {
        $('id_cnpj').addClass('is-invalid');
        erroDivCNPJ.addClass('invalid-feedback show');
        btnConsultaCNPJ.html('Consultar CNPJ');
        btnConsultaCNPJ.attr('disabled', false);
      }
    });
  }
};


/* Retorna o o endereço completo no formato:

{
  "cep": "65073120",
  "state": "MA",
  "city": "São Luís",
  "neighborhood": "Parque Shalon",
  "street": "Rua V-13",
  "service": "open-cep",
  "location": {
      "type": "Point",
      "coordinates": {}
  }
}
  */
const consultarCEP = () => {
  let cep = $('#id_cep').val();
  let cleaned_cep = cep.replace(/[^\d]/g, '');
  const url = `/api/cep/${cleaned_cep}`;
  let erroDivCEP = $('#id_cep-error');
  const btnConsultaCEP = $('#btn_consulta_cep');

  // Adiciona div que conterá mensagem de erro, se ela não existir
  if (erroDivCEP.length === 0) {
    $('<div id="id_cep-error"></div>').insertAfter('.btn-warning');
    erroDivCEP = $('#id_cep-error');
  }

  if(cleaned_cep.length != 8){
    $('#id_cep').addClass('is-invalid');
    erroDivCEP.addClass('invalid-feedback show');
    erroDivCEP.text('Não é um CEP Válido')
  }else{
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
          erroDivCEP.addClass('invalid-feedback show');
          erroDivCEP.text('Não é um CEP Válido')
        }else{
          // se for válido, remove a classe de erro do campo CEP
          $('#id_cep').removeClass('is-invalid');
          erroDivCEP.text('')
          $('#id_cep').addClass('is-valid');
                  
        }
      },
      error: (errorThrown,  jqXHR, textStatus) => {
        // Caso eu CEP inválido seja inserido, cairá aqui
        // avisará o erro, e habilitará novamente o botão de consulta
        $('#id_cep').addClass('is-invalid');
        erroDivCEP.addClass('invalid-feedback show');
        erroDivCEP.text(`${errorThrown.responseJSON.message}`)
        btnConsultaCEP.html('Consultar CEP');
        btnConsultaCEP.attr('disabled', false);
      }
    });
  }
};


const tratarJSONCNPJ = () => {
  jsonFile = {
    "cnpj_raiz": "27865757",
    "razao_social": "GLOBO COMUNICACAO E PARTICIPACOES S/A",
    "capital_social": "6983568523.86",
    "responsavel_federativo": null,
    "atualizado_em": "2024-06-26T23:57:40.000Z",
    "porte": {
        "id": "05",
        "descricao": "Demais"
    },
    "natureza_juridica": {
        "id": "2054",
        "descricao": "Sociedade Anônima Fechada"
    },
    "qualificacao_do_responsavel": null,
    "socios": [
        {
            "cpf_cnpj_socio": "***050187**",
            "nome": "PEDRO BORGES GARCIA",
            "tipo": "Pessoa Física",
            "data_entrada": "2024-03-21",
            "cpf_representante_legal": "***000000**",
            "nome_representante": null,
            "faixa_etaria": "51 a 60 anos",
            "atualizado_em": "2024-06-08T03:00:00.000Z",
            "pais_id": "1058",
            "qualificacao_socio": {
                "id": 10,
                "descricao": "Diretor "
            },
            "qualificacao_representante": null,
            "pais": {
                "id": "1058",
                "iso2": "BR",
                "iso3": "BRA",
                "nome": "Brasil",
                "comex_id": "105"
            }
        },
        {
            "cpf_cnpj_socio": "***048947**",
            "nome": "PAULO DAUDT MARINHO",
            "tipo": "Pessoa Física",
            "data_entrada": "2020-01-16",
            "cpf_representante_legal": "***000000**",
            "nome_representante": null,
            "faixa_etaria": "41 a 50 anos",
            "atualizado_em": "2024-06-08T03:00:00.000Z",
            "pais_id": "1058",
            "qualificacao_socio": {
                "id": 10,
                "descricao": "Diretor "
            },
            "qualificacao_representante": null,
            "pais": {
                "id": "1058",
                "iso2": "BR",
                "iso3": "BRA",
                "nome": "Brasil",
                "comex_id": "105"
            }
        },
        {
            "cpf_cnpj_socio": "***486498**",
            "nome": "RAYMUNDO COSTA PINTO BARROS",
            "tipo": "Pessoa Física",
            "data_entrada": "2021-03-15",
            "cpf_representante_legal": "***000000**",
            "nome_representante": null,
            "faixa_etaria": "61 a 70 anos",
            "atualizado_em": "2024-06-08T03:00:00.000Z",
            "pais_id": "1058",
            "qualificacao_socio": {
                "id": 10,
                "descricao": "Diretor "
            },
            "qualificacao_representante": null,
            "pais": {
                "id": "1058",
                "iso2": "BR",
                "iso3": "BRA",
                "nome": "Brasil",
                "comex_id": "105"
            }
        },
        {
            "cpf_cnpj_socio": "***189808**",
            "nome": "AMAURI SERGIO SOARES",
            "tipo": "Pessoa Física",
            "data_entrada": "2022-02-11",
            "cpf_representante_legal": "***000000**",
            "nome_representante": null,
            "faixa_etaria": "51 a 60 anos",
            "atualizado_em": "2024-06-08T03:00:00.000Z",
            "pais_id": "1058",
            "qualificacao_socio": {
                "id": 10,
                "descricao": "Diretor "
            },
            "qualificacao_representante": null,
            "pais": {
                "id": "1058",
                "iso2": "BR",
                "iso3": "BRA",
                "nome": "Brasil",
                "comex_id": "105"
            }
        },
        {
            "cpf_cnpj_socio": "***610997**",
            "nome": "GEORGES AYOUB RICHE",
            "tipo": "Pessoa Física",
            "data_entrada": "2023-12-05",
            "cpf_representante_legal": "***000000**",
            "nome_representante": null,
            "faixa_etaria": "41 a 50 anos",
            "atualizado_em": "2024-06-08T03:00:00.000Z",
            "pais_id": "1058",
            "qualificacao_socio": {
                "id": 10,
                "descricao": "Diretor "
            },
            "qualificacao_representante": null,
            "pais": {
                "id": "1058",
                "iso2": "BR",
                "iso3": "BRA",
                "nome": "Brasil",
                "comex_id": "105"
            }
        }
    ],
    "simples": null,
    "estabelecimento": {
        "cnpj": "27865757000102",
        "atividades_secundarias": [
            {
                "id": "5911102",
                "secao": "J",
                "divisao": "59",
                "grupo": "59.1",
                "classe": "59.11-1",
                "subclasse": "5911-1/02",
                "descricao": "Produção de filmes para publicidade"
            },
            {
                "id": "5911199",
                "secao": "J",
                "divisao": "59",
                "grupo": "59.1",
                "classe": "59.11-1",
                "subclasse": "5911-1/99",
                "descricao": "Atividades de produção cinematográfica, de vídeos e de programas de televisão não especificadas anteriormente"
            },
            {
                "id": "5912002",
                "secao": "J",
                "divisao": "59",
                "grupo": "59.1",
                "classe": "59.12-0",
                "subclasse": "5912-0/02",
                "descricao": "Serviços de mixagem sonora em produção audiovisual"
            },
            {
                "id": "5913800",
                "secao": "J",
                "divisao": "59",
                "grupo": "59.1",
                "classe": "59.13-8",
                "subclasse": "5913-8/00",
                "descricao": "Distribuição cinematográfica, de vídeo e de programas de televisão"
            },
            {
                "id": "5920100",
                "secao": "J",
                "divisao": "59",
                "grupo": "59.2",
                "classe": "59.20-1",
                "subclasse": "5920-1/00",
                "descricao": "Atividades de gravação de som e de edição de música"
            },
            {
                "id": "6022501",
                "secao": "J",
                "divisao": "60",
                "grupo": "60.2",
                "classe": "60.22-5",
                "subclasse": "6022-5/01",
                "descricao": "Programadoras"
            },
            {
                "id": "6204000",
                "secao": "J",
                "divisao": "62",
                "grupo": "62.0",
                "classe": "62.04-0",
                "subclasse": "6204-0/00",
                "descricao": "Consultoria em tecnologia da informação"
            },
            {
                "id": "6209100",
                "secao": "J",
                "divisao": "62",
                "grupo": "62.0",
                "classe": "62.09-1",
                "subclasse": "6209-1/00",
                "descricao": "Suporte técnico, manutenção e outros serviços em tecnologia da informação"
            },
            {
                "id": "6311900",
                "secao": "J",
                "divisao": "63",
                "grupo": "63.1",
                "classe": "63.11-9",
                "subclasse": "6311-9/00",
                "descricao": "Tratamento de dados, provedores de serviços de aplicação e serviços de hospedagem na Internet"
            },
            {
                "id": "6319400",
                "secao": "J",
                "divisao": "63",
                "grupo": "63.1",
                "classe": "63.19-4",
                "subclasse": "6319-4/00",
                "descricao": "Portais, provedores de conteúdo e outros serviços de informação na Internet"
            },
            {
                "id": "6463800",
                "secao": "K",
                "divisao": "64",
                "grupo": "64.6",
                "classe": "64.63-8",
                "subclasse": "6463-8/00",
                "descricao": "Outras sociedades de participação, exceto holdings"
            },
            {
                "id": "7020400",
                "secao": "M",
                "divisao": "70",
                "grupo": "70.2",
                "classe": "70.20-4",
                "subclasse": "7020-4/00",
                "descricao": "Atividades de consultoria em gestão empresarial, exceto consultoria técnica específica"
            },
            {
                "id": "7490104",
                "secao": "M",
                "divisao": "74",
                "grupo": "74.9",
                "classe": "74.90-1",
                "subclasse": "7490-1/04",
                "descricao": "Atividades de intermediação e agenciamento de serviços e negócios em geral, exceto imobiliários"
            },
            {
                "id": "7739099",
                "secao": "N",
                "divisao": "77",
                "grupo": "77.3",
                "classe": "77.39-0",
                "subclasse": "7739-0/99",
                "descricao": "Aluguel de outras máquinas e equipamentos comerciais e industriais não especificados anteriormente, sem operador"
            },
            {
                "id": "7740300",
                "secao": "N",
                "divisao": "77",
                "grupo": "77.4",
                "classe": "77.40-3",
                "subclasse": "7740-3/00",
                "descricao": "Gestão de ativos intangíveis não financeiros"
            },
            {
                "id": "9001902",
                "secao": "R",
                "divisao": "90",
                "grupo": "90.0",
                "classe": "90.01-9",
                "subclasse": "9001-9/02",
                "descricao": "Produção musical"
            },
            {
                "id": "9319101",
                "secao": "R",
                "divisao": "93",
                "grupo": "93.1",
                "classe": "93.19-1",
                "subclasse": "9319-1/01",
                "descricao": "Produção e promoção de eventos esportivos"
            },
            {
                "id": "9512600",
                "secao": "S",
                "divisao": "95",
                "grupo": "95.1",
                "classe": "95.12-6",
                "subclasse": "9512-6/00",
                "descricao": "Reparação e manutenção de equipamentos de comunicação"
            }
        ],
        "cnpj_raiz": "27865757",
        "cnpj_ordem": "0001",
        "cnpj_digito_verificador": "02",
        "tipo": "Matriz",
        "nome_fantasia": "Tv/rede/canais/g2c+globo Globo.com Globoplay",
        "situacao_cadastral": "Ativa",
        "data_situacao_cadastral": "2005-11-03",
        "data_inicio_atividade": "1986-01-31",
        "nome_cidade_exterior": null,
        "tipo_logradouro": null,
        "logradouro": "Rua Lopes Quintas",
        "numero": "303",
        "complemento": null,
        "bairro": "Jardim Botanico",
        "cep": "22460901",
        "ddd1": "21",
        "telefone1": "21554552",
        "ddd2": null,
        "telefone2": null,
        "ddd_fax": null,
        "fax": null,
        "email": null,
        "situacao_especial": null,
        "data_situacao_especial": null,
        "atualizado_em": "2024-06-26T23:57:40.000Z",
        "atividade_principal": {
            "id": "6021700",
            "secao": "J",
            "divisao": "60",
            "grupo": "60.2",
            "classe": "60.21-7",
            "subclasse": "6021-7/00",
            "descricao": "Atividades de televisão aberta"
        },
        "pais": {
            "id": "1058",
            "iso2": "BR",
            "iso3": "BRA",
            "nome": "Brasil",
            "comex_id": "105"
        },
        "estado": {
            "id": 19,
            "nome": "Rio de Janeiro",
            "sigla": "RJ",
            "ibge_id": 33
        },
        "cidade": {
            "id": 3243,
            "nome": "Rio de Janeiro",
            "ibge_id": 3304557,
            "siafi_id": "6001"
        },
        "motivo_situacao_cadastral": null,
        "inscricoes_estaduais": [
            {
                "inscricao_estadual": "84295760",
                "ativo": true,
                "atualizado_em": "2024-03-11T19:23:54.833Z",
                "estado": {
                    "id": 19,
                    "nome": "Rio de Janeiro",
                    "sigla": "RJ",
                    "ibge_id": 33
                }
            },
            {
                "inscricao_estadual": "113717433112",
                "ativo": false,
                "atualizado_em": "2024-03-11T19:23:54.833Z",
                "estado": {
                    "id": 26,
                    "nome": "São Paulo",
                    "sigla": "SP",
                    "ibge_id": 35
                }
            },
            {
                "inscricao_estadual": "84347353",
                "ativo": false,
                "atualizado_em": "2024-03-11T19:23:54.833Z",
                "estado": {
                    "id": 19,
                    "nome": "Rio de Janeiro",
                    "sigla": "RJ",
                    "ibge_id": 33
                }
            },
            {
                "inscricao_estadual": "211426987",
                "ativo": true,
                "atualizado_em": "2024-03-11T19:23:54.833Z",
                "estado": {
                    "id": 5,
                    "nome": "Bahia",
                    "sigla": "BA",
                    "ibge_id": 29
                }
            },
            {
                "inscricao_estadual": "9000073850",
                "ativo": true,
                "atualizado_em": "2024-04-20T03:00:00.000Z",
                "estado": {
                    "id": 23,
                    "nome": "Rio Grande do Sul",
                    "sigla": "RS",
                    "ibge_id": 43
                }
            },
            {
                "inscricao_estadual": "0629985490214",
                "ativo": true,
                "atualizado_em": "2024-04-27T03:00:00.000Z",
                "estado": {
                    "id": 11,
                    "nome": "Minas Gerais",
                    "sigla": "MG",
                    "ibge_id": 31
                }
            },
            {
                "inscricao_estadual": "819017430118",
                "ativo": true,
                "atualizado_em": "2024-06-07T03:00:00.000Z",
                "estado": {
                    "id": 26,
                    "nome": "São Paulo",
                    "sigla": "SP",
                    "ibge_id": 35
                }
            }
        ]
    }
  };

  // Parse do JSON com os dados que serão utilizados para preencher o formulário
  const razao_social = (jsonFile.razao_social) ? jsonFile.razao_social : "";
  console.log(razao_social);
  const nome_fantasia = (jsonFile.estabelecimento.nome_fantasia) ? jsonFile.estabelecimento.nome_fantasia : "";
  console.log(nome_fantasia);
  const cep = (jsonFile.estabelecimento.cep) ? jsonFile.estabelecimento.cep : "";
  const ddd1 = (jsonFile.estabelecimento.ddd1) ? jsonFile.estabelecimento.ddd1 : "";
  const bairro = (jsonFile.estabelecimento.bairro) ? jsonFile.estabelecimento.bairro : "";
  const numero = (jsonFile.estabelecimento.numero) ? jsonFile.estabelecimento.numero : "";
  const logradouro = (jsonFile.estabelecimento.logradouro) ? jsonFile.estabelecimento.logradouro : "";
  const complemento = (jsonFile.estabelecimento.complemento) ? jsonFile.estabelecimento.complemento : "";
  const telefone1 = (jsonFile.estabelecimento.telefone1) ? jsonFile.estabelecimento.telefone1 : "";
  const estado = (jsonFile.estabelecimento.estado.sigla) ? jsonFile.estabelecimento.estado.sigla : "";
  const cidade = (jsonFile.estabelecimento.cidade.nome)  ? jsonFile.estabelecimento.cidade.nome : "";
  const inscricoes_estaduais = (message.estabelecimento.inscricoes_estaduais) ? message.estabelecimento.inscricoes_estaduais : "";

  // Elimina inscrições não ativas
  if (inscricoes_estaduais.length > 0) {
    const inscricoesAtivas = inscricoes_estaduais.filter( inscricao => inscricao.ativo )
  }else{
    const inscricoesAtivas = "";
  }

};