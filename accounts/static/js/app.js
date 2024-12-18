/**
 * Esconde modal de criar usuário após o submit
 */
$('#formCriarUsuario').submit(function (event) {
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function (response) {
            if (response.success) {
                $('#modalCriarUsuario').modal('hide');
            }
        }
    });
});