document.getElementById('ventaForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const producto = formData.get('id_producto');
    const cantidad = formData.get('cantidad');
    const precio = formData.get('precio_total');
    //let iva = 7;
    const precioTotal = parseInt(cantidad) * parseFloat(precio);

    // para actualizar la tabla
    const table = document.getElementById('resumenTabla');
    const newRow = table.insertRow();
    newRow.innerHTML = `
        <td>${cantidad}</td>
        <td>${producto}</td>
        <td>${precio}</td>
        <td>${precioTotal.toFixed(2)}</td>
    `;

    // Actualizar el total
    const totalVenta = document.getElementById('total-venta');
    const nuevoTotal = parseFloat(totalVenta.textContent) + precioTotal;
    totalVenta.textContent = nuevoTotal.toFixed(2);
    // actualiz el iba uwu
    const parcialIva = document.getElementById('total-iva');
    const totalIva = nuevoTotal * 0.16; // Corrección aquí
    parcialIva.textContent = totalIva.toFixed(2);


    // limpia el formulario
    event.target.reset();
});
