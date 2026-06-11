<?php
session_start();
$successMessage = $_SESSION['success_message'] ?? 'Tu solicitud ha sido procesada correctamente.';
unset($_SESSION['success_message']);
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solicitud Enviada</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="css/style.css">
</head>
<body class="bg-light">
    <div class="container py-5">
        <div class="card shadow rounded-4 p-5 text-center">
            <h1 class="fw-bold mb-3">Gracias</h1>
            <p class="lead text-muted mb-4"><?= htmlspecialchars($successMessage) ?></p>
            <a href="index.php" class="btn btn-primary">Volver al inicio</a>
        </div>
    </div>
</body>
</html>
