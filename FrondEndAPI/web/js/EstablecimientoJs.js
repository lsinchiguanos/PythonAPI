window.addEventListener("load", cargaDatos);
function cargaDatos() {
    $.ajax({
        type: "GET",
        url: "http://localhost:3000/books",
        dataType: "json",
        beforeSend: function () { },
        success: function (data) {
            llama(data);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR.statusCode);
            console.log(textStatus);
        }
    });
}
function llama(data) {
    $.each(data, function (key, value) {
        document.getElementById("tbody").innerHTML += `<tr>
			<th scope="row">` + value.book_id + `</th>
			<td>` + value.id + `</td>
			<td>` + value.nombre + `</td>
			<td>` + value.cupo + `</td>
			<td>
			<button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#miModal" 
			data-id="` + value.id + `">Actualizar</button>
			</td>
			<td><button type="button" class="btn btn-danger" data-id="` + value.id + `">Borrar</button>
			</td>
			</tr>`;
    });
}
$(document).ready(function () {
    $('#btnsave').click(function (e) {
        e.preventDefault();
        var jsondata = {
            "id": $('#id').val(),
            "nombre": $('#nombre').val(),
            "cupo": $('#cupo').val()
        };
        $.ajax({
            type: "POST",
            url: "http://localhost:3000/book",
            data: JSON.stringify(jsondata),
            contentType: 'application/json',
            dataType: "json",
            beforeSend: function () { },
            success: function (data) {
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
