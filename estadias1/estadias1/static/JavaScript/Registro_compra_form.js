document
  .getElementById("btnGuardar")
  .addEventListener("click", function (event) {
    event.preventDefault();
    const formData = new FormData(document.getElementById('compraForm'));
    const producto = formData.get("id_producto");
    const proveedor = formData.get("id_proveedor");
    const cantidad = parseFloat(formData.get("cantidad"));
    const costo = parseFloat(formData.get("costo"));

    // Verifica si cantidad y costo son números válidos
    if (isNaN(cantidad) || isNaN(costo) ) {
      alert("Por favor, introduce valores válidos");
      return;
    }

    const precioTotal = cantidad * costo;

    // para actualizar la tabla
    const table = document.getElementById("resumenTabla");
    const newRow = table.insertRow();
    newRow.innerHTML = `
        <td>${cantidad}</td>
        <td>${producto}</td>
        <td>${proveedor}</td>
        <td>${costo}</td>
        <td>${precioTotal}</td>
    `;

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
    });
    newRow.querySelector(".eliminarBtn").addEventListener("click", function () {
      eliminarFila(newRow);
    });

    console.log(proveedor);

    // limpiar el formulario
    document.getElementById("id_id_producto").value = "";
    document.getElementById("id_id_proveedor").value = "";
    document.getElementById("id_cantidad").value = "";
    document.getElementById("id_costo").value = "";
  });

document
  .getElementById("editarCompraBtn")
  .addEventListener("click", function () {
    const rows = document.querySelectorAll("#resumenTabla tr");

    rows.forEach((row, index) => {
      if (index > 0) {
        // Skip header row
        row.querySelector(".editarBtn").style.display = "inline";
        row.querySelector(".eliminarBtn").style.display = "inline";
      }
    });
    document.getElementById("editarCompraBtn").style.display = "none"; // Hide the Edit Compra button after it is clicked
  });

function editarFila(row) {
  const cantidadCell = row.cells[0];
  const productoCell = row.cells[1];
  const proveedorCell = row.cells[2];
  const costoCell = row.cells[3];

  const cantidad = cantidadCell.textContent;
  const producto = productoCell.textContent;
  const proveedor = proveedorCell.textContent;
  const costo = costoCell.textContent;

  // Llenar el formulario con los datos de la fila
  document.getElementById("id_id_producto").value = producto;
  document.getElementById("id_id_proveedor").value = proveedor;
  document.getElementById("id_cantidad").value = cantidad;
  document.getElementById("id_costo").value = costo;

  // Guardar el índice de la fila para referencia
  document
    .getElementById("compraForm")
    .setAttribute("data-editing-row-index", row.rowIndex);

  // Eliminar la fila original
  eliminarFila(row);
}



function eliminarFila(row) {
  const precioTotalCell = row.cells[4];
  const precioTotal = parseFloat(precioTotalCell.textContent);
  const totalCompra = document.getElementById("total-compra");
  totalCompra.textContent = parseFloat(totalCompra.textContent) - precioTotal;
    row.remove(); // Elimina toda la fila
}


function disableProveedorField() {
  const proveedorInput = document.getElementById("id_proveedor");
  const cambiarProveedorBtn = document.getElementById("cambiarProveedorBtn");
  proveedorInput.disabled = true;
  cambiarProveedorBtn.style.display = "inline";

  cambiarProveedorBtn.addEventListener("click", function (event) {
    event.preventDefault();
    const cambiarProveedorModal = document.getElementById(
      "cambiarProveedorModal"
    );
    cambiarProveedorModal.style.display = "block";
  });

  document
    .getElementById("aceptarCambioProveedor")
    .addEventListener("click", function () {
      const proveedorInput = document.getElementById("id_proveedor");
      proveedorInput.disabled = false;
      document.getElementById("cambiarProveedorModal").style.display = "none";
    });

  document
    .getElementById("cancelarCambioProveedor")
    .addEventListener("click", function () {
      document.getElementById("cambiarProveedorModal").style.display = "none";
    });
}
