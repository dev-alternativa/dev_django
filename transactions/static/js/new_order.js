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
                alert(erro);
            }
        });
    });
});