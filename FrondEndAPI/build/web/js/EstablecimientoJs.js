/* global Swal */

var id_actualizar = 0;

window.addEventListener("load", cargaDatos);

function cargaDatos() {
    $('#btnupdate').hide();
    $.ajax({
        method: "GET",
        url: "http://localhost:5000/api/establecimientos",
        dataType: "json",
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        success: function (data) {
            llama(data);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR.statusCode);
            console.log(textStatus);
            console.log(errorThrown);
        }
    });
}
;

function llama(data) {
    $.each(data, function (key, value) {
        document.getElementById("tbody").innerHTML += `<tr>
			<th scope="row">` + value.id + `</th>
			<td>` + value.nombre + `</td>
			<td>` + value.cupo + `</td>
			<td>
			<button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#miModal" 
			data-id="` + value.id + `" onclick="mostrar(` + value.id + `)">Actualizar</button>
			</td>
			<td><button type="button" class="btn btn-danger" data-id="` + value.id + `" onclick="eliminar(` + value.id + `)">Borrar</button>
			</td>
			</tr>`;
    });
}
;

$(document).ready(function () {
    $('#btnsave').click(function (e) {
        e.preventDefault();
        let datos = {
            nombre: document.getElementById('nombre').value,
            cupo: document.getElementById('cupo').value
        };
        $.ajax({
            url: "http://localhost:5000/api/establecimientos",
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
                limpiar();
                $('tbody').html("");
                cargaDatos();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR.status);
                console.log(textStatus);
            }
        });
    });
});

function limpiar() {
    document.getElementById('nombre').value = '';
    document.getElementById('cupo').value = '';
    $("#miModal").modal('toggle');
}
;

function eliminar(id) {
    $.ajax({
        method: "DELETE",
        url: "http://localhost:5000/api/establecimiento/" + id,
        dataType: "json",
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        success: function (data) {
            $('tbody').html("");
            cargaDatos();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR.statusCode);
            console.log(textStatus);
            console.log(errorThrown);
        }
    });
}
;

function mostrar(id) {
    $('#btnupdate').show();
    $('#btnsave').hide();
    id_actualizar = id;
    $("#miModal").modal("show");
}
;

function actualizar(id) {
    let datos = {
        nombre: document.getElementById('nombre').value,
        cupo: document.getElementById('cupo').value
    };
    $.ajax({
        url: "http://localhost:5000/api/establecimiento/" + id,
        data: JSON.stringify(datos),
        method: 'PUT',
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (response) {
            console.log(response);
            $('#btnsave').show();
            $('#btnupdate').hide();
            Swal.fire({
                position: 'top-end',
                icon: 'success',
                title: response.message,
                showConfirmButton: false,
                timer: 1500
            });
            id_actualizar = 0;
            limpiar();
            $('tbody').html("");
            cargaDatos();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR.status);
            console.log(textStatus);
        }
    });
}
;