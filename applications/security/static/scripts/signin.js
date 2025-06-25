document.getElementById('loginForm').addEventListener('submit', function (e) {
    // Mostrar loading inmediatamente
    document.getElementById('medicalLoading').classList.remove('hidden')

    // Deshabilitar botón para evitar doble click
    document.getElementById('loginButton').disabled = true
    document.getElementById('loginButton').innerHTML = 'Iniciando sesión...'
})
