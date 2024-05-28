//<-JS para gestionar el formulario para compras->>

document.getElementById('compraForm').addEventListener('submit',function(event){
    event.preventDefault();
    const formData = new FormData(event.target);
    const producto = formData.get('id_producto');
    const proveedor = formData.get('id_proveedor')
    const cantidad = formData.get('cantidad');
    const costo = formData.get('costo');

    const precioTotal = cantidad * costo;


    //para actualizarr la tableeeeeee
    const table = document.getElementById('resumenTabla');
    const newRow = table.insertRow();
    newRow.innerHTML = `
    <td>${producto}</td>
    <td>${proveedor}</td>
    <td>${costo}</td>
    <td>${cantidad}</td>
    <td>${precioTotal}</td>
    `;

    //Actualizar el toptal
    
    const totalCompra = document.getElementById('total-compra');
    const nuevoTotal = parseFloat(totalCompra.textContent) + precioTotal;
    totalCompra.textContent = nuevoTotal;

    //limpia el formulario
    event.target.reset();

});





