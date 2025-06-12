
function handlePriceModals(data) {

    $('#itemsModal').modal('show');
    console.log('Frete antes', data.taxa_frete_item);
    isDolar = data.is_dolar;
    let preco = data.preco;
    let taxa_frete_item = parseFloat(data.taxa_frete_item)
    let $selectApp = $('#id_cnpj_faturamento');
    taxa_frete_item = (taxa_frete_item !== undefined && taxa_frete_item !== null) ? Number(taxa_frete_item)
        .toFixed(2)
        .replace('.', ',') : 0;
    console.log('FRETE DEPOIS', taxa_frete_item);

    $selectApp.empty();
    $selectApp.append('<option value="">---------</option>');

    $.each(data.cnpj_faturamento_options, function(index, item) {
        $selectApp.append(
        $('<option>', {
            value: item.id,
            text: item.sigla
        })
        );
    });

    if (data.selected_cnpj_faturamento){
        $selectApp.val(data.selected_cnpj_faturamento);
    }

    // Atualiza o valores do modal de adição de produto
    /** Caso o preço seja cadastrado como dolar, já verificar e multiplica corretamente,
    adicionando as labels corretamente
    */
    if(isDolar){
        preco = (data.preco * parseFloat($('#id_dolar_ptax').val())).toFixed(4);
    }
    $('#id_preco').val(preco);
    $('#id_conta_corrente').val(data.cc);
    $('#id_prazo_item').val(data.prazo_item).trigger('change');


    if(data.origem_frete == 'tabela_preco'){
        $('#info_preco').html('*Taxa do Produto');
    }else{
        $('#info_preco').html('*Taxa original do Cliente');

    }

    $("#id_quantidade").val(1);
    $("#hidden_dolar_id").val(isDolar);
    $('#id_item_pedido').val(data.item_pedido);
    $('#id_vendedor_item').val(data.vendedor);
    $('#id_taxa_frete_item').val(taxa_frete_item);
    $('#id_tipo_frete_item').val(data.tipo_frete_item);
    $('#id_m2').val(data.m2);
    $('#hidden_m2_id').val(data.m2);
    $('#hidden_categoria_id').val(data.categoria);
    $("#nome_produto").text(`${productName} (${data.unidade})`);

    configProductFormLabels(data.categoria);
    calcProductFieldsArea(data.m2);

    $("#div_id_preco label").append(`/ <b>Condição: ${paymentTerms}</b>`);

    $("#div_id_preco label").html('Preço pç (R$)');
    $('#hidden_m2_id').val(0);
    $('#hidden_categoria_id').val(0);
    $('#itemsModalLabel').contents().first().replaceWith(`Adicionar Produto - `);

}
    // $('#itemsModal').modal('show');
