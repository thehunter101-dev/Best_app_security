document.addEventListener('DOMContentLoaded', function () {
    const moduleSelect = document.querySelector('select[name="module"]')
    const permissionsSelect = document.querySelector('select[name="permissions"]')

    if (!moduleSelect || !permissionsSelect) return

    moduleSelect.addEventListener('change', function () {
        const moduleId = this.value
        if (!moduleId) return

        fetch(`/security/module/${moduleId}/permissions/`)
            .then((response) => response.json())
            .then((data) => {
                // Limpiar opciones actuales
                permissionsSelect.innerHTML = ''

                // Agregar nuevas opciones
                data.permissions.forEach(function (permission) {
                    const option = document.createElement('option')
                    option.value = permission.id
                    option.textContent = permission.name
                    permissionsSelect.appendChild(option)
                })
            })
            .catch((error) => {
                console.error('Error cargando permisos:', error)
            })
    })
})

document.addEventListener('DOMContentLoaded', function () {
    // Inicializamos Select2 en el campo de permisos si existe
    const permissionsSelect = $('#id_permissions')

    if (permissionsSelect.length) {
        permissionsSelect.select2({
            placeholder: 'Seleccione permisos',
            allowClear: true,
            // theme: "bootstrap" // Descomenta si estás usando Bootstrap
        })
    }

    // Manejamos el cambio de módulo para actualizar permisos
    const moduleSelect = document.getElementById('id_module')

    if (moduleSelect) {
        moduleSelect.addEventListener('change', function () {
            const moduleId = this.value

            if (moduleId) {
                console.log('Módulo seleccionado: ' + moduleId)

                // Aquí puedes hacer una llamada AJAX si deseas cargar permisos dinámicamente
                // Ejemplo (debes habilitar la URL correspondiente en Django):
                /*
                $.ajax({
                    url: `/security/api/permissions-for-module/${moduleId}/`,
                    method: 'GET',
                    success: function (data) {
                        permissionsSelect.empty();
                        data.permissions.forEach(function (perm) {
                            const newOption = new Option(perm.name, perm.id, false, false);
                            permissionsSelect.append(newOption);
                        });
                        permissionsSelect.trigger('change');
                    },
                    error: function () {
                        alert("Error al cargar los permisos del módulo.");
                    }
                });
                */

                // Por ahora, solo limpieza (si no usas AJAX dinámico)
                // permissionsSelect.empty().trigger('change');
            } else {
                permissionsSelect.empty().trigger('change')
            }
        })
    }
})
