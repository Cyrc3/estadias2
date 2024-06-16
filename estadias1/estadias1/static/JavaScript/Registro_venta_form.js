document
  .getElementById("btnGuardar")
  .addEventListener("click", function (event) {
    event.preventDefault();

    // Obtener datos del formulario
    const formData = new FormData(document.getElementById("ventaForm")); // Asegúrate de que el ID del formulario sea correcto
    const productoId = formData.get("id_producto");
    const cantidad = parseInt(formData.get("cantidad"));
    const precioTotal = parseFloat(formData.get("precio_total"));
    const rfcId = formData.get("rfc");

    // Verificar si cantidad y precio total son números válidos
    if (isNaN(cantidad) || isNaN(precioTotal)) {
      alert("Por favor, introduce valores válidos para cantidad y precio total.");
      return;
    }
    const precioFinal = cantidad * costo;
    // Obtener texto de las opciones seleccionadas (si es necesario)
    const productoText = obtenerTextoOpcionSeleccionada("id_producto", productoId);
    const rfcText = obtenerTextoOpcionSeleccionada("rfc", rfcId);

    // Actualizar la tabla (si es necesario)
    const table = document.getElementById("resumenTabla");
    const newRow = table.insertRow();
    newRow.innerHTML = `
        <td>${cantidad}</td>
        <td data-id="${productoId}">${productoText}</td>
        <td data-id="${rfcId}">${rfcText}</td>
        <td>${precioFinal}</td>
    `;
    document.getElementById("editarVentaBtn").style.display = "inline";
    // Añadir botones de edición y eliminación
    const actionsCell = newRow.insertCell(-1); // Insert a new cell at the end for actions
    actionsCell.innerHTML = `
        <button class="editarBtn" style="display: none;">Editar</button>
        <button class="eliminarBtn" style="display: none;">Eliminar</button>
    `;
    newRow.querySelector(".editarBtn").addEventListener("click", function () {
      editarFila(newRow);
    });
    newRow.querySelector(".eliminarBtn").addEventListener("click", function () {
      eliminarFila(newRow);
    });

    // Limpiar el formulario (si es necesario)
    limpiarFormulario("ventaForm");
  });
  document
  .getElementById("editarVentaBtn").addEventListener("click", function (event) {
    event.preventDefault();
    const rows = document.querySelectorAll("#resumenTabla tr");

    rows.forEach((row, index) => {
      if (index > 0) {
        // Skip header row
        row.querySelector(".editarBtn").style.display = "inline";
        row.querySelector(".eliminarBtn").style.display = "inline";
      }
    });
    document.getElementById("editarVentaBtn").style.display = "none"; // Hide the Edit venta button after it is clicked
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
  
    // Llenar el formulario con los datos de la fila
    document.getElementById("id_id_producto").value = productoid;
    document.getElementById("id_id_proveedor").value = proveedorid;
    document.getElementById("id_cantidad").value = cantidad;
    document.getElementById("id_costo").value = costo;
  
    // Guardar el índice de la fila para referencia
    document
      .getElementById("VentaForm")
      .setAttribute("data-editing-row-index", row.rowIndex);
  
    // Eliminar la fila original
    eliminarFilaParaEditar(row);
  }
  function eliminarFilaParaEditar(row){
    const precioTotalCell = row.cells[4];
    const precioTotal = parseFloat(precioTotalCell.textContent);
    const totalVenta = document.getElementById("total-venta");
    totalVenta.textContent = parseFloat(totalVenta.textContent) - precioTotal;
    row.remove(); // Elimina toda la fila
  }

function eliminarFila(row) {
    filaParaEliminar = row;
    document.getElementById("eliminarVenta").style.display = 'block';
  }
  
  document.getElementById('aceptarEliminar').addEventListener('click',function(event){
    event.preventDefault();
    if(filaParaEliminar){
      const precioTotalCell = filaParaEliminar.cells[4];
          const precioTotal = parseFloat(precioTotalCell.textContent);
          const totalVenta = document.getElementById("total-venta");
          totalVenta.textContent = (parseFloat(totalVenta.textContent) - precioTotal).toFixed(2);
          filaParaEliminar.remove(); // Elimina toda la fila
          filaParaEliminar = null;
          document.getElementById("eliminarVenta").style.display = "none";
    }
  });

document.getElementById('cancelarEliminar').addEventListener('click',function(event){
    event.preventDefault();
    filaParaEliminar = null;
    document.getElementById("eliminarVenta").style.display = "none";
  })
  
  document
  .getElementById("registrarVentaBtn")
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

    const fechaVenta = document.getElementById('fecha').value;
    const totalVenta = document.getElementById('total-venta').textContent;

    const fechaField = document.createElement('input');
    fechaField.type = 'hidden';
    fechaField.name = 'fecha_compra';
    fechaField.value = fechaVenta;
    document.getElementById('compraForm').appendChild(fechaField);

    const totalField = document.createElement('input');
    totalField.type = 'hidden';
    totalField.name = 'total_compra';
    totalField.value = totalVenta;
    document.getElementById('compraForm').appendChild(totalField);

    document.getElementById('compraForm').submit();

  });




/*
// Función para obtener el texto de la opción seleccionada
function obtenerTextoOpcionSeleccionada(selectId, value) {
  return document.querySelector(`#${selectId} option[value="${value}"]`).textContent;
}

// Función para limpiar el formulario después de guardar los datos
function limpiarFormulario(formId) {
  document.getElementById(`${formId}`).reset();
}
*/