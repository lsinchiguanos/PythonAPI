/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
/* global Swal */

function saveCliente() {
    let datos = {
        dni: document.getElementById('cedulaDeIdentidad').value,
        apellido_paterno: document.getElementById('apellidoPaterno').value,
        apellido_materno: document.getElementById('apellidoMaterno').value,
        primer_nombre: document.getElementById('primerNombre').value,
        segundo_nombre: document.getElementById('segundoNombre').value
    };
    console.log(datos);
    $.ajax({
        url: 'http://localhost:5000/api/clientes',
        data: JSON.stringify(datos),
        method: 'POST',
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (response) {
            console.log(response);
            Swal.fire({
                position: 'top-end',
                icon: 'success',
                title: response.message,
                showConfirmButton: false,
                timer: 1500
            });
            limpiar_form();
        },
        error: function (error) {
            console.log(error);
            Swal.fire({
                position: 'top-end',
                icon: 'error',
                title: error,
                showConfirmButton: false,
                timer: 1500
            });
        }
    });
}
;

function limpiar_form() {
    document.getElementById('cedulaDeIdentidad').value = '';
    document.getElementById('apellidoPaterno').value = '';
    document.getElementById('apellidoMaterno').value = '';
    document.getElementById('primerNombre').value = '';
    document.getElementById('segundoNombre').value = '';
}
;