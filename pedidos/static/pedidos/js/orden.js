document.addEventListener("DOMContentLoaded", function () {

    let detalles = [];

    const repuestoSelect = document.getElementById("repuestoSelect");
    const cantidadInput = document.getElementById("cantidadInput");
    const precioInput = document.getElementById("precioInput");
    const tabla = document.querySelector("#tablaDetalles tbody");
    const detallesJson = document.getElementById("detallesJson");

    // Cuando selecciona repuesto → llenar precio
    repuestoSelect.addEventListener("change", function () {
        const repuestoId = this.value;
        if (!repuestoId) return;

        fetch(`/pedidos/precio-repuesto/${repuestoId}/`)
            .then(res => res.json())
            .then(data => {
                precioInput.value = data.precio;
            });
    });

    // Agregar repuesto a la tabla
    document.getElementById("btnAgregar").addEventListener("click", function () {

        const repuestoId = repuestoSelect.value;
        const repuestoText = repuestoSelect.options[repuestoSelect.selectedIndex].text;
        const cantidad = parseInt(cantidadInput.value);
        const precio = parseInt(precioInput.value);
        const subtotal = cantidad * precio;

        if (!repuestoId || !cantidad || !precio) {
            alert("Complete todos los campos antes de agregar.");
            return;
        }

        const detalle = {
            repuesto_id: repuestoId,
            repuesto: repuestoText,
            cantidad,
            precio_unitario: precio,
            subtotal
        };

        detalles.push(detalle);
        actualizarTabla();
    });

    function actualizarTabla() {
        tabla.innerHTML = "";

        detalles.forEach((d, index) => {
            tabla.innerHTML += `
                <tr>
                    <td>${d.repuesto}</td>
                    <td>${d.cantidad}</td>
                    <td>${d.precio_unitario}</td>
                    <td>${d.subtotal}</td>
                    <td>
                        <button class="btn btn-danger btn-sm" onclick="eliminar(${index})">X</button>
                    </td>
                </tr>
            `;
        });

        detallesJson.value = JSON.stringify(detalles);
    }

    // Eliminar un reglon
    window.eliminar = function(index) {
        detalles.splice(index, 1);
        actualizarTabla();
    }

});
