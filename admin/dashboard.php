<?php
session_start();
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../helpers.php';

if (empty($_SESSION['admin_logged_in'])) {
    header('Location: login.php');
    exit;
}

$pdo = get_db_connection();
$query = 'SELECT * FROM solicitudes';
$where = [];
$params = [];

if (!empty($_GET['search'])) {
    $where[] = '(nombre LIKE :search OR numero_solicitud LIKE :search)';
    $params[':search'] = '%' . $_GET['search'] . '%';
}

if (!empty($_GET['estado'])) {
    $where[] = 'estado = :estado';
    $params[':estado'] = $_GET['estado'];
}

if (!empty($_GET['desde']) && !empty($_GET['hasta'])) {
    $where[] = 'fecha_creacion BETWEEN :desde AND :hasta';
    $params[':desde'] = $_GET['desde'] . ' 00:00:00';
    $params[':hasta'] = $_GET['hasta'] . ' 23:59:59';
}

if (!empty($where)) {
    $query .= ' WHERE ' . implode(' AND ', $where);
}

$query .= ' ORDER BY fecha_creacion DESC';

$stmt = $pdo->prepare($query);
$stmt->execute($params);
$solicitudes = $stmt->fetchAll();

$estados = ['Pendiente', 'En revisión', 'Aprobado', 'Rechazado', 'Completado'];
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Administrativo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="../css/style.css">
</head>
<body class="bg-light">
    <div class="container py-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1>Panel Administrativo</h1>
            <a href="logout.php" class="btn btn-outline-secondary">Cerrar sesión</a>
        </div>

        <form class="row g-3 mb-4" method="get">
            <div class="col-md-4">
                <input type="text" class="form-control" name="search" placeholder="Buscar solicitudes" value="<?= htmlspecialchars($_GET['search'] ?? '') ?>">
            </div>
            <div class="col-md-3">
                <select name="estado" class="form-select">
                    <option value="">Filtrar por estado</option>
                    <?php foreach ($estados as $estado): ?>
                        <option value="<?= $estado ?>" <?= (($_GET['estado'] ?? '') === $estado) ? 'selected' : '' ?>><?= $estado ?></option>
                    <?php endforeach; ?>
                </select>
            </div>
            <div class="col-md-2">
                <input type="date" name="desde" class="form-control" value="<?= htmlspecialchars($_GET['desde'] ?? '') ?>">
            </div>
            <div class="col-md-2">
                <input type="date" name="hasta" class="form-control" value="<?= htmlspecialchars($_GET['hasta'] ?? '') ?>">
            </div>
            <div class="col-md-1 d-grid">
                <button class="btn btn-primary" type="submit">Filtrar</button>
            </div>
        </form>

        <div class="table-responsive">
            <table class="table table-striped align-middle">
                <thead class="table-dark">
                    <tr>
                        <th>N° Solicitud</th>
                        <th>Nombre</th>
                        <th>Email</th>
                        <th>Estado</th>
                        <th>Fecha</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($solicitudes as $solicitud): ?>
                        <tr>
                            <td><?= htmlspecialchars($solicitud['numero_solicitud']) ?></td>
                            <td><?= htmlspecialchars($solicitud['nombre']) ?></td>
                            <td><?= htmlspecialchars($solicitud['email']) ?></td>
                            <td><?= htmlspecialchars($solicitud['estado']) ?></td>
                            <td><?= htmlspecialchars($solicitud['fecha_creacion']) ?></td>
                            <td>
                                <a href="view_request.php?id=<?= intval($solicitud['id']) ?>" class="btn btn-sm btn-outline-primary">Ver</a>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                    <?php if (empty($solicitudes)): ?>
                        <tr><td colspan="6" class="text-center text-muted">No se encontraron solicitudes.</td></tr>
                    <?php endif; ?>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
