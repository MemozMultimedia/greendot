<?php
session_start();
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../helpers.php';

if (empty($_SESSION['admin_logged_in'])) {
    header('Location: login.php');
    exit;
}

$pdo = get_db_connection();
$id = intval($_GET['id'] ?? 0);
$stmt = $pdo->prepare('SELECT * FROM solicitudes WHERE id = :id');
$stmt->execute([':id' => $id]);
$solicitud = $stmt->fetch();

if (!$solicitud) {
    header('Location: dashboard.php');
    exit;
}

$estados = ['Pendiente', 'En revisión', 'Aprobado', 'Rechazado', 'Completado'];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nuevoEstado = $_POST['estado'] ?? $solicitud['estado'];
    $update = $pdo->prepare('UPDATE solicitudes SET estado = :estado WHERE id = :id');
    $update->execute([':estado' => $nuevoEstado, ':id' => $id]);
    header('Location: dashboard.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solicitud <?= htmlspecialchars($solicitud['numero_solicitud']) ?></title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="../css/style.css">
</head>
<body class="bg-light">
    <div class="container py-5">
        <a href="dashboard.php" class="btn btn-outline-secondary mb-4">← Volver al panel</a>
        <div class="card shadow rounded-4 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <div>
                    <h2>Solicitud <?= htmlspecialchars($solicitud['numero_solicitud']) ?></h2>
                    <p class="text-muted">Creada el <?= htmlspecialchars($solicitud['fecha_creacion']) ?></p>
                </div>
                <form method="post" class="d-flex gap-2 align-items-center">
                    <select name="estado" class="form-select">
                        <?php foreach ($estados as $estado): ?>
                            <option value="<?= $estado ?>" <?= $solicitud['estado'] === $estado ? 'selected' : '' ?>><?= $estado ?></option>
                        <?php endforeach; ?>
                    </select>
                    <button class="btn btn-success" type="submit">Guardar</button>
                </form>
            </div>
            <div class="row g-4">
                <div class="col-md-6">
                    <h5>Datos personales</h5>
                    <p><strong>Nombre:</strong> <?= htmlspecialchars($solicitud['nombre']) ?></p>
                    <p><strong>Teléfono:</strong> <?= htmlspecialchars($solicitud['telefono']) ?></p>
                    <p><strong>Email:</strong> <?= htmlspecialchars($solicitud['email']) ?></p>
                    <p><strong>Dirección:</strong> <?= htmlspecialchars($solicitud['direccion']) ?></p>
                </div>
                <div class="col-md-6">
                    <h5>Reporte</h5>
                    <p><strong>Tipo:</strong> <?= htmlspecialchars($solicitud['tipo_reporte']) ?></p>
                    <p><strong>Comentarios:</strong> <?= nl2br(htmlspecialchars($solicitud['comentarios'])) ?></p>
                    <p><strong>Documento:</strong> <a href="../<?= htmlspecialchars($solicitud['documento']) ?>" target="_blank" class="link-primary">Ver archivo</a></p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
