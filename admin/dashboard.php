<?php
require_once __DIR__ . '/../helpers.php';
require_admin();
$db = db_connect();
$query = 'SELECT * FROM applications';
$where = [];
$params = [];
if (!empty($_GET['status'])) {
    $where[] = 'status = :status';
    $params[':status'] = $_GET['status'];
}
if (!empty($_GET['search'])) {
    $where[] = '(full_name LIKE :search OR email LIKE :search)';
    $params[':search'] = '%' . $_GET['search'] . '%';
}
if ($where) {
    $query .= ' WHERE ' . implode(' AND ', $where);
}
$query .= ' ORDER BY created_at DESC';
$stmt = $db->prepare($query);
$stmt->execute($params);
$applications = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Applications Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body class="bg-light">
    <div class="container py-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="h3">Admin Dashboard</h1>
            <a href="logout.php" class="btn btn-outline-secondary">Logout</a>
        </div>
        <form class="row g-3 mb-4">
            <div class="col-md-4"><input type="text" name="search" class="form-control" placeholder="Search name or email" value="<?= sanitize($_GET['search'] ?? '') ?>"></div>
            <div class="col-md-3">
                <select name="status" class="form-select">
                    <option value="">All statuses</option>
                    <?php foreach (['Pending','Approved','Rejected'] as $status): ?>
                        <option value="<?= $status ?>" <?= ($_GET['status'] ?? '') === $status ? 'selected' : '' ?>><?= $status ?></option>
                    <?php endforeach; ?>
                </select>
            </div>
            <div class="col-md-2"><button class="btn btn-success w-100">Filter</button></div>
        </form>
        <div class="table-responsive rounded-4 shadow-sm bg-white">
            <table class="table mb-0">
                <thead class="table-light"><tr><th>Application</th><th>Email</th><th>Status</th><th>Submitted</th><th>Action</th></tr></thead>
                <tbody>
                <?php foreach ($applications as $app): ?>
                    <tr>
                        <td><?= sanitize($app['full_name']) ?></td>
                        <td><?= sanitize($app['email']) ?></td>
                        <td><?= sanitize($app['status']) ?></td>
                        <td><?= sanitize($app['created_at']) ?></td>
                        <td><a href="view.php?id=<?= $app['id'] ?>" class="btn btn-sm btn-outline-primary">View</a></td>
                    </tr>
                <?php endforeach; ?>
                <?php if (empty($applications)): ?><tr><td colspan="5" class="text-center text-muted">No applications found.</td></tr><?php endif; ?>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
