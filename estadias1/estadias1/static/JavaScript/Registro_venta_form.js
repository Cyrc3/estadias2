// <-JS para gestionar el formulario para compras->

document.getElementById('ventaForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const producto = formData.get('id_producto');
    //const proveedor = formData.get('id_proveedor')
    const cantidad = formData.get('cantidad');
    const costo = formData.get('costo');
    const iva = formData.get('iva');
    const precioTotal = parseFloat(cantidad) * (parseFloat(costo) + parseFloat(iva));

    //para actualizar la tabla
    const table = document.getElementById('resumenTabla');
    const newRow = table.insertRow();
    newRow.innerHTML = `
    <td>${producto}</td>
    <td>${costo}</td>
    <td>${cantidad}</td>
    <td>${precioTotal.toFixed(2)}</td>
    `;

    //Actualizar el total
    const totalVenta = document.getElementById('total-venta');
    const nuevoTotal = parseFloat(totalVenta.textContent) + precioTotal;
    totalVenta.textContent = nuevoTotal.toFixed(2);

    //limpia el formulario
    event.target.reset();
});
