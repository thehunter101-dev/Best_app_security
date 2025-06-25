function openDeleteModal(id, name) {
  const deleteForm = document.getElementById("deleteForm");
  deleteForm.action = `${deleteUrlBase}/${id}/`;
  document.getElementById("Description").textContent = `ID: ${id} - ${name}`;
  document.getElementById("deleteModal").classList.remove("hidden");
}

function closeModal() {
  document.getElementById("deleteModal").classList.add("hidden");
}

// ✅ AGREGAR: Asegurar redirección correcta
document.addEventListener("DOMContentLoaded", function () {
  const deleteForm = document.getElementById("deleteForm");

  if (deleteForm) {
    deleteForm.addEventListener("submit", function (e) {
      // Opcional: Mostrar loading
      const submitBtn = deleteForm.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.innerHTML =
          '<i class="fa-solid fa-spinner fa-spin"></i> Eliminando...';
        submitBtn.disabled = true;
      }

      // Permitir envío normal del formulario
      // Django manejará la redirección automáticamente
    });
  }
});
