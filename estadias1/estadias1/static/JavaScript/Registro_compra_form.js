document
  .getElementById("btnGuardar")
  .addEventListener("click", function (event) {
    event.preventDefault();
    const formData = new FormData(document.getElementById("compraForm"));
    const productoId = formData.get("id_producto");

    //const proveedorId = formData.get("id_proveedor");
    let proveedorId = formData.get("id_proveedor");
    if (document.getElementById("id_id_proveedor").disabled) {
      proveedorId = document.getElementById("hidden_proveedor").value;
    } else {
        document.getElementById("hidden_proveedor").value = proveedorId;
    }
    //console.log(proveedorId);
    const cantidad = parseFloat(formData.get("cantidad"));
    const costo = parseFloat(formData.get("costo"));

    //modificacion para id
    const productoText = document.querySelector(
      `#id_id_producto option[value="${productoId}"]`
    ).textContent;
    const proveedorText = document.querySelector(
      `#id_id_proveedor option[value="${proveedorId}"]`
    ).textContent;

    // Verifica si cantidad y costo son números válidos
    if (isNaN(cantidad) || isNaN(costo)) {
      alert("Por favor, introduce valores válidos");
      return;
    }

    const precioTotal = cantidad * costo;

    // para actualizar la tabla
    const table = document.getElementById("resumenTabla");
    const newRow = table.insertRow();
    newRow.innerHTML = `
        <td>${cantidad}</td>
        <td data-id="${productoId}">${productoText}</td>
        <td data-id="${proveedorId}">${proveedorText}</td>
        <td>${costo}</td>
        <td>${precioTotal}</td>
    `;

    document.getElementById("id_id_proveedor").disabled = true;

    
    // Actualizar el total
    const totalCompra = document.getElementById("total-compra");
    const nuevoTotal = parseFloat(totalCompra.textContent) + precioTotal;
    totalCompra.textContent = nuevoTotal;

    // Mostrar botón de editar compra
    document.getElementById("editarCompraBtn").style.display = "inline";

    // Añadir botones de edición y eliminación
    const actionsCell = newRow.insertCell(-1); // Insert a new cell at the end for actions
    actionsCell.innerHTML = `
        <button class="editarBtn" style="display: none;">Editar</button>
        <button class="eliminarBtn" style="display: none;">Eliminar</button>
    `;
    newRow.querySelector(".editarBtn").addEventListener("click", function () {
      editarFila(newRow);
      document.getElementById('cambiarProveedorBtn').style.display='inline';
    });
    newRow.querySelector(".eliminarBtn").addEventListener("click", function () {
      eliminarFila(newRow);
    });


    // limpiar el formulario
    document.getElementById("id_id_producto").value = "";
    document.getElementById("id_cantidad").value = "";
    document.getElementById("id_costo").value = "";
    document.getElementById('cambiarProveedorBtn').style.display='none';


  });


//editar compra ###################################################################################
document
  .getElementById("editarCompraBtn")
  .addEventListener("click", function (event) {
    event.preventDefault();
    const rows = document.querySelectorAll("#resumenTabla tr");

    rows.forEach((row, index) => {
      if (index > 0) {
        // Skip header row
        row.querySelector(".editarBtn").style.display = "inline";
        row.querySelector(".eliminarBtn").style.display = "inline";
      }
    });
    document.getElementById("editarCompraBtn").style.display = "none"; 
  });

function editarFila(row) {
  const cantidadCell = row.cells[0];
  const productoCell = row.cells[1];
  const proveedorCell = row.cells[2];
  const costoCell = row.cells[3];

  const cantidad = cantidadCell.textContent;
  const productoid = productoCell.getAttribute("data-id");
  const proveedorid = proveedorCell.getAttribute("data-id");
  const costo = costoCell.textContent;

  // Llenar el formulario con los datos de la fila ###################################################################################
  document.getElementById("id_id_producto").value = productoid;
  document.getElementById("id_id_proveedor").value = proveedorid;
  document.getElementById("id_cantidad").value = cantidad;
  document.getElementById("id_costo").value = costo;

  // Guardar el índice de la fila para referencia ###################################################################################
  document
    .getElementById("compraForm")
    .setAttribute("data-editing-row-index", row.rowIndex);

  // Eliminar la fila original ###################################################################################
  eliminarFilaParaEditar(row);

  // Ocultar todos los botones de editar y eliminar
  const editarButtons = document.querySelectorAll(".editarBtn");
  const eliminarButtons = document.querySelectorAll(".eliminarBtn");
  editarButtons.forEach(button => button.style.display = 'none');
  eliminarButtons.forEach(button => button.style.display = 'none');
}

function eliminarFilaParaEditar(row) {
  const precioTotalCell = row.cells[4];
  const precioTotal = parseFloat(precioTotalCell.textContent);
  const totalCompra = document.getElementById("total-compra");
  totalCompra.textContent = parseFloat(totalCompra.textContent) - precioTotal;
  row.remove(); // Elimina toda la fila
}

function eliminarFila(row) {
  filaParaEliminar = row;
  document.getElementById("eliminarCompra").style.display = "block"; // ###################################################################################
}

document
  .getElementById("aceptarEliminar")
  .addEventListener("click", function (event) {
    event.preventDefault();
    if (filaParaEliminar) {
      const precioTotalCell = filaParaEliminar.cells[4];
      const precioTotal = parseFloat(precioTotalCell.textContent);
      const totalCompra = document.getElementById("total-compra");
      totalCompra.textContent = (
        parseFloat(totalCompra.textContent) - precioTotal
      ).toFixed(2);
      filaParaEliminar.remove(); // Elimina toda la fila
      filaParaEliminar = null;
      document.getElementById("eliminarCompra").style.display = "none";
    }
  });

document
  .getElementById("cancelarEliminar")
  .addEventListener("click", function (event) {
    event.preventDefault();
    filaParaEliminar = null;
    document.getElementById("eliminarCompra").style.display = "none";
  });


//Editar proveedor ###################################################################################


document.getElementById('cambiarProveedorBtn').addEventListener('click',function(event){
  event.preventDefault();
  cambiarProveedor();
})

function cambiarProveedor(){
  document.getElementById('cambiarProveedor').style.display='block';
  document.getElementById("cambiarProveedorBtn").style.display = "none";
}

document.getElementById('aceptarCambiar').addEventListener('click',function(event){
  event.preventDefault();
  document.getElementById('id_id_proveedor').disabled=false;
  document.getElementById('cambiarProveedor').style.display='none';

})

document.getElementById('cancelarCambiar').addEventListener('click',function(event){
  event.preventDefault();
  document.getElementById('cambiarProveedor').style.display='none';
})

//botón registrar  ###################################################################################

document
  .getElementById("registrarCompraBtn")
  .addEventListener("click", function (event) {
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
