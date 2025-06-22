// Vista previa del ícono
document.addEventListener('DOMContentLoaded', function () {
    const iconInput = document.getElementById('{{ form.icon.id_for_label }}')
    const iconPreview = document.getElementById('iconPreview')

    function updateIconPreview() {
        const iconClass = iconInput.value.trim()
        if (iconClass) {
            iconPreview.className = iconClass + ' text-3xl text-blue-600 dark:text-blue-400'
        } else {
            iconPreview.className = 'bi bi-x-octagon text-3xl text-gray-400'
        }
    }

    // Actualizar vista previa al cargar la página (para edición)
    updateIconPreview()

    // Actualizar vista previa cuando cambie el input
    iconInput.addEventListener('input', updateIconPreview)
    iconInput.addEventListener('keyup', updateIconPreview)
    iconInput.addEventListener('change', updateIconPreview)
})
