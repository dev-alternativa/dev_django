
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
            const dolar = data.value[0].cotacaoVenda;
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
                let taxa_frete = response.taxa_frete;
                console.log(parseFloat(taxa_frete));
                if (taxa_frete && parseFloat(taxa_frete) != 0) {
                    taxa_frete = parseFloat(taxa_frete).toFixed(2);
                    $("#id_taxa_frete").val(taxa_frete.replace('.', ','));
                    let message = `Atenção, cliente com taxa de frete encontrado.`;
                    let alertElement = `
                        <div class="alert alert-secondary alert-dismissible fade show" role="alert">
                            ${message}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>`;
                    $("#messages").append(alertElement);
                }
            },
            error: function (response) {

                let erro = response.responseJSON.error;
                console.log(erro);
                // $("#id_taxa_frete").val('0,00');

            }
        });
    });
});
