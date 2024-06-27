// Interceptar el evento "Enter" en los campos de entrada
document.querySelectorAll("#id_cantidad, #id_costo", '#iva').forEach(function(input) {
    input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevenir el envío del formulario
        }
    });
});



//BOTÓN DE GUARDAR O AÑADIR COMPRA --SIRVE PARA PASAR DATOS DEL FORM A LA TABLA DE RESUMEN

document.getElementById("btnGuardar").addEventListener("click", function (event) {
    event.preventDefault();
    const formData = new FormData(document.getElementById("compraForm"));
    const productoId = formData.get("id_producto");

    let proveedorId = formData.get("id_proveedor");
    if (document.getElementById("id_id_proveedor").disabled) {
        proveedorId = document.getElementById("hidden_proveedor").value;
    } else {
        document.getElementById("hidden_proveedor").value = proveedorId;
    }

    const cantidad = parseFloat(formData.get("cantidad"));
    const costo = parseFloat(formData.get("costo"));
    const registroConIva = document.getElementById('iva').checked;

    const productoText = document.querySelector(`#id_id_producto option[value="${productoId}"]`).textContent;
    const proveedorText = document.querySelector(`#id_id_proveedor option[value="${proveedorId}"]`).textContent;

    if (isNaN(cantidad) || isNaN(costo)) {
        alert("Por favor, introduce valores válidos");
        return;
    }

    let iva = 0.0;
    let subtotal = cantidad * costo;

    if (registroConIva) {
        iva = subtotal * 0.16;
    }

    const precioTotal = subtotal + iva;

    const table = document.getElementById("resumenTabla");
    const newRow = table.insertRow();
    newRow.innerHTML = `
        <td>${cantidad}</td>
        <td data-id="${productoId}">${productoText}</td>
        <td data-id="${proveedorId}">${proveedorText}</td>
        <td>${costo}</td>
        <td>${subtotal}</td>
        <td style="display:none;">${registroConIva}</td> <!-- Columna oculta para saber si el producto es registrado con IVA -->
    `;

    document.getElementById("id_id_proveedor").disabled = true;

    actualizarTotales(subtotal, iva);

    document.getElementById("editarCompraBtn").style.display = "inline"; //BOTÓN PARA EDITAR COMPRA, APARECE UNA VEZ QUE SE AÑADE UNA PRODUCTO A LA TABLA

    const actionsCell = newRow.insertCell(-1);
    actionsCell.innerHTML = `
        <button class="editarBtn" style="display: none;">Editar</button> 
        <button class="eliminarBtn" style="display: none;">Eliminar</button>
    `; //CREA LOS BOTONE ELIMINAR Y EDITAR DENTRO DE LA TABLA EN LA COMLUMNA ACCIONES

    // SE LE AÑADEN FUNCIONES A LOS BOTONES
    newRow.querySelector(".editarBtn").addEventListener("click", function () {
        editarFila(newRow);
        document.getElementById('cambiarProveedorBtn').style.display = 'inline';
    });
    newRow.querySelector(".eliminarBtn").addEventListener("click", function () {
        eliminarFila(newRow);
    });


    //SE LIMPIA EL FORMULARIO
    //document.getElementById("id_id_producto").value = ""; como ahora es un select2 se usa esto:
    $('#id_id_producto').val(null).trigger('change');
    document.getElementById("id_cantidad").value = "";
    document.getElementById("id_costo").value = "";
    document.getElementById('cambiarProveedorBtn').style.display = 'none';


     // Llamar a la función de actualización de proveedores después de guardar
    actualizarProveedores(proveedorId, proveedorText);
    
});



//SE AÑADE FUNCION AL BOTON DE EDITAR COMPRA
document.getElementById("editarCompraBtn").addEventListener("click", function (event) {
    event.preventDefault();
    const rows = document.querySelectorAll("#resumenTabla tr");

    rows.forEach((row, index) => {
        if (index > 0) {
            row.querySelector(".editarBtn").style.display = "inline";
            row.querySelector(".eliminarBtn").style.display = "inline";
        }
    });
    document.getElementById("editarCompraBtn").style.display = "none";
});


//FUNCION PARA EDITAR LA FILA QUE ESTA LIGADO AL BOTON EDITAR EN LA PARTE DE ARRIBA
function editarFila(row) {  
    const cantidadCell = row.cells[0];
    const productoCell = row.cells[1];
    const proveedorCell = row.cells[2];
    const costoCell = row.cells[3];
    const subtotalCell = row.cells[4];
    const ivaCell = row.cells[5];

    const cantidad = cantidadCell.textContent;
    const productoid = productoCell.getAttribute("data-id");
    const proveedorid = proveedorCell.getAttribute("data-id");
    const costo = parseFloat(costoCell.textContent);
    const subtotal = parseFloat(subtotalCell.textContent);
    const registroConIva = ivaCell.textContent === 'true';
    const iva = registroConIva ? subtotal * 0.16 : 0;

    actualizarTotales(-subtotal, -iva);

    //document.getElementById("id_id_producto").value = productoid;
    $('#id_id_producto').val(productoid).trigger('change');
    document.getElementById("id_id_proveedor").value = proveedorid;
    document.getElementById("id_cantidad").value = cantidad;
    document.getElementById("id_costo").value = costo;
    document.getElementById("iva").checked = registroConIva;


    document.getElementById("compraForm").setAttribute("data-editing-row-index", row.rowIndex);

    eliminarFilaParaEditar(row);

    const editarButtons = document.querySelectorAll(".editarBtn");
    const eliminarButtons = document.querySelectorAll(".eliminarBtn");
    editarButtons.forEach(button => button.style.display = 'none');
    eliminarButtons.forEach(button => button.style.display = 'none');
}


//ELIMINA LA FILA PARA PROCEDER CON LA EDICION DE LA MISMA
function eliminarFilaParaEditar(row) {  
    row.remove();
}

//ELIMINA LA FILA
function eliminarFila(row) {
    filaParaEliminar = row;
    document.getElementById("eliminarCompra").style.display = "block";
}


//VALIDACIÓN PARA ELIMINAR
document.getElementById('aceptarEliminar').addEventListener('click', function (event) {
    event.preventDefault();
    if (filaParaEliminar) {
        
        const subtotalCell = filaParaEliminar.cells[4];
        const ivaCell = filaParaEliminar.cells[5]; // Columna oculta para IVA

        const subtotal = parseFloat(subtotalCell.textContent);
        const registroConIva = ivaCell.textContent === 'true';
        const iva = registroConIva ? subtotal * 0.16 : 0;

        actualizarTotales(-subtotal, -iva);

        filaParaEliminar.remove();
        filaParaEliminar = null;
        document.getElementById("eliminarCompra").style.display = "none";
    }
});

document.getElementById('cancelarEliminar').addEventListener('click', function (event) {
    event.preventDefault();
    filaParaEliminar = null;
    document.getElementById("eliminarCompra").style.display = "none";
});


//FUNCION PARA ACTUALIZAR LOS TOTALES POR LO DEL IVA Y ESAS COSAS
function actualizarTotales(subtotal, iva) {  
    // Actualizar SUBTOTAL
    const subTotalCompra = document.getElementById('subtotal-compra');
    const nuevoSubtotal = parseFloat(subTotalCompra.textContent) + subtotal;
    subTotalCompra.textContent = nuevoSubtotal.toFixed(2);

    // Actualizar el Iva
    const ivaCompra = document.getElementById('iva-compra');
    const nuevaIva = parseFloat(ivaCompra.textContent) + iva;
    ivaCompra.textContent = nuevaIva.toFixed(2);

    // Actualizar el total
    const totalCompra = document.getElementById("total-compra");
    const nuevoTotal = parseFloat(totalCompra.textContent) + subtotal + iva;
    totalCompra.textContent = nuevoTotal.toFixed(2);
}


//FUNCIONES  PARA CAMBIAR DE PROVEEDOR
document.getElementById('cambiarProveedorBtn').addEventListener('click', function(event){
    event.preventDefault();
    cambiarProveedor();
})

function cambiarProveedor(){
    document.getElementById('cambiarProveedor').style.display = 'block';
    document.getElementById("cambiarProveedorBtn").style.display = "none";
}

document.getElementById('aceptarCambiar').addEventListener('click', function(event){
    event.preventDefault();
    document.getElementById('id_id_proveedor').disabled = false;
    document.getElementById('cambiarProveedor').style.display = 'none';
})

// Función para actualizar el proveedor en todas las filas
function actualizarProveedores(nuevoProveedorId, nuevoProveedorText) {
    const rows = document.querySelectorAll("#resumenTabla tr");
    rows.forEach((row, index) => {
        if (index > 0) { // Saltar la fila del encabezado
            const proveedorCell = row.cells[2];
            proveedorCell.setAttribute("data-id", nuevoProveedorId);
            proveedorCell.textContent = nuevoProveedorText;
        }
    });
}


document.getElementById('cancelarCambiar').addEventListener('click', function(event){
    event.preventDefault();
    document.getElementById('cambiarProveedor').style.display = 'none';
})


//FUNCION PARA ALMACENAR DATOS Y DESPUES EXTRAERLOS EN EL VIEWS.PY
document.getElementById("registrarCompraBtn").addEventListener("click", function (event) {
    event.preventDefault();

    const resumenTabla = document.getElementById("resumenTabla");
    const rows = resumenTabla.getElementsByTagName("tr");
    const resumenData = [];

    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName("td");
        const rowData = {
            cantidad: cells[0].innerText,
            producto_id: cells[1].getAttribute("data-id"),
            proveedor_id: cells[2].getAttribute("data-id"),
            costo: cells[3].innerText,
            precio_total: cells[4].innerText,
        };
        resumenData.push(rowData);
    }

    const hiddenField = document.createElement("input");
    hiddenField.type = "hidden";
    hiddenField.name = "resumen_data";
    hiddenField.value = JSON.stringify(resumenData);
    document.getElementById("compraForm").appendChild(hiddenField);

    const fechaCompra = document.getElementById("fecha").value;
    if(fechaCompra === ""){
        alert("INGRESA LA FECHA DE LA COMPRA")
        return;
    }
    const totalCompra = document.getElementById("total-compra").textContent;

    const fechaField = document.createElement("input");
    fechaField.type = "hidden";
    fechaField.name = "fecha_compra";
    fechaField.value = fechaCompra;
    document.getElementById("compraForm").appendChild(fechaField);

    const totalField = document.createElement("input");
    totalField.type = "hidden";
    totalField.name = "total_compra";
    totalField.value = totalCompra;
    document.getElementById("compraForm").appendChild(totalField);

    document.getElementById("compraForm").submit();
});