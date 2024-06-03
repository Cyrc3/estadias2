document.getElementById('compraForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const producto = formData.get('id_producto');
    const proveedor = formData.get('id_proveedor');
    const cantidad = formData.get('cantidad');
    const costo = formData.get('costo');

    const precioTotal = cantidad * costo;

    // para actualizar la tabla
    const table = document.getElementById('resumenTabla');
    const newRow = table.insertRow();
    newRow.innerHTML = `
        <td>${producto}</td>
        <td>${proveedor}</td>
        <td>${costo}</td>
        <td>${cantidad}</td>
        <td>${precioTotal}</td>
    `;

    // Actualizar el total
    const totalCompra = document.getElementById('total-compra');
    const nuevoTotal = parseFloat(totalCompra.textContent) + precioTotal;
    totalCompra.textContent = nuevoTotal;


    console.log()
    // limpia el formulario
    event.target.reset();

});

function disableProveedorField() {
    const proveedorInput = document.getElementById('id_proveedor');
    const cambiarProveedorBtn = document.getElementById('cambiarProveedorBtn');
    proveedorInput.disabled = true;
    cambiarProveedorBtn.style.display = 'inline';

    cambiarProveedorBtn.addEventListener('click', function(event) {
        event.preventDefault();
        const cambiarProveedorModal = document.getElementById('cambiarProveedorModal');
        cambiarProveedorModal.style.display = 'block';
    });

    document.getElementById('aceptarCambioProveedor').addEventListener('click', function() {
        const proveedorInput = document.getElementById('id_proveedor');
        proveedorInput.disabled = false;
        document.getElementById('cambiarProveedorModal').style.display = 'none';
    });

    document.getElementById('cancelarCambioProveedor').addEventListener('click', function() {
        document.getElementById('cambiarProveedorModal').style.display = 'none';
    });
}
