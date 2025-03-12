
const requestDolarPTAX = (event) => {
    /**
     * Recupera o dólar PTAX do dia e preenche o campo id_dolar_ptax
     *
     */
    event.preventDefault();
    console.log('Consultando Dolar PTAX');
    $.ajax({
        url: '/api/dolar_hoje/',
        method: 'GET',
        success: (data) => {
            const dolar = data.value[0].cotacaoVenda.toFixed(2);
            $('#id_dolar_ptax').val(dolar);
        },
        error: (err) => {
            console.log(err);
        }
    });

};


$(document).ready(function () {
    /**
     * Funções para Novo Pedido
     */

    // Seleciona Taxa de Frete conforme Cliente selecionado
    $('#id_cliente').on('change', function () {
        const id = $(this).val();
        const url = `/cliente/${id}/taxa_frete/`;
        $.ajax({
            url: url,
            type: 'GET',
            success: function (response) {
                if (response.data) {
                    const taxa_frete = parseFloat(response.data.taxa_frete).toFixed(2);
                    console.log(taxa_frete);
                    $("#id_taxa_frete").val(taxa_frete.replace('.', ','));
                }
            },
            error: function (response) {
                console.log(response);
                let erro = response.responseJSON.error;
                $("#id_taxa_frete").val('0,00');

            }
        });
    });
});
