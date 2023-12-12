$(document).ready(function () {
    $(".btn-aceptar").click(function () {
        var solicitudId = $(this).data("solicitud");
        $.ajax({
            url: `/cambiar_estado_solicitud/${solicitudId}/aceptar/`,
            type: "POST",
            dataType: "json",
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}', // Asegúrate de incluir el token CSRF
                // Otros datos que quieras enviar, si es necesario
            },
            success: function (response) {
                console.log("Estado cambiado exitosamente");
                // Realiza acciones después de cambiar el estado si es necesario
            },
            error: function (xhr, errmsg, err) {
                console.log("Error: No se pudo cambiar el estado");
                // Manejo de errores si es necesario
            },
        });
    });

    $(".btn-rechazar").click(function () {
        var solicitudId = $(this).data("solicitud");
        $.ajax({
            url: `/cambiar_estado_solicitud/${solicitudId}/rechazar/`,
            type: "POST",
            dataType: "json",
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}', // Asegúrate de incluir el token CSRF
                // Otros datos que quieras enviar, si es necesario
            },
            success: function (response) {
                console.log("Estado cambiado exitosamente");
                // Realiza acciones después de cambiar el estado si es necesario
            },
            error: function (xhr, errmsg, err) {
                console.log("Error: No se pudo cambiar el estado");
                // Manejo de errores si es necesario
            },
        });
    });
});
