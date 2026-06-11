<?php
require_once __DIR__ . '/../helpers.php';
require_admin();
$id = intval($_GET['id'] ?? 0);
$db = db_connect();
$stmt = $db->prepare('SELECT * FROM applications WHERE id = :id');
$stmt->execute([':id' => $id]);
$app = $stmt->fetch(PDO::FETCH_ASSOC);
if (!$app) {
    header('Location: dashboard.php');
    exit;
}
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $status = sanitize($_POST['status'] ?? $app['status']);
    $update = $db->prepare('UPDATE applications SET status = :status WHERE id = :id');
    $update->execute([':status' => $status, ':id' => $id]);
    header('Location: dashboard.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Application Details</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body class="bg-light">
    <div class="container py-5">
        <a href="dashboard.php" class="btn btn-link mb-4">← Back to dashboard</a>
        <div class="card rounded-4 shadow-sm p-4">
            <h3 class="mb-3">Application details</h3>
            <div class="row gy-3">
                <div class="col-md-6"><strong>Name</strong><div class="text-muted"><?= sanitize($app['full_name']) ?></div></div>
                <div class="col-md-6"><strong>Email</strong><div class="text-muted"><?= sanitize($app['email']) ?></div></div>
                <div class="col-md-6"><strong>Phone</strong><div class="text-muted"><?= sanitize($app['phone']) ?></div></div>
                <div class="col-md-6"><strong>Status</strong><div class="text-muted"><?= sanitize($app['status']) ?></div></div>
                <div class="col-12"><strong>Address</strong><div class="text-muted"><?= sanitize($app['address']) ?></div></div>
                <div class="col-md-4"><strong>DOB</strong><div class="text-muted"><?= sanitize($app['dob']) ?></div></div>
                <div class="col-md-4"><strong>SSN Last 4</strong><div class="text-muted">****<?= sanitize($app['ssn_last4']) ?></div></div>
                <div class="col-md-4"><strong>ID document</strong><div><a href="/<?= sanitize($app['document_path']) ?>" target="_blank">View file</a></div></div>
            </div>
            <form method="post" class="mt-4 row g-3 align-items-end">
                <div class="col-md-4">
                    <label class="form-label">Change status</label>
                    <select name="status" class="form-select">
                        <?php foreach (['Pending','Approved','Rejected'] as $status): ?>
                            <option value="<?= $status ?>" <?= $app['status'] === $status ? 'selected' : '' ?>><?= $status ?></option>
                        <?php endforeach; ?>
                    </select>
                </div>
                <div class="col-md-2"><button class="btn btn-success w-100">Update</button></div>
            </form>
        </div>
    </div>
</body>
</html>
