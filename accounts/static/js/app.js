$('#formCriarUsuario').submit(function(event) {
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function(response) {
            if (response.success) {
                $('#modalCriarUsuario').modal('hide');
                // Faça qualquer ação de sucesso desejada, como recarregar a página ou exibir uma mensagem de sucesso
            }
        }
    });
});