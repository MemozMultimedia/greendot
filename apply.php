<?php
require_once 'helpers.php';
define('SITE_TITLE', 'GreenDot Fintech | Apply Now');

$errors = [];
$success = false;
$formData = [
    'full_name' => '',
    'address' => '',
    'phone' => '',
    'email' => '',
    'dob' => '',
    'ssn_last4' => ''
];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $formData = array_map('sanitize', $_POST);
    $errors = validate_app_form($formData);
    $documentPath = handle_upload($_FILES['id_document'] ?? []);
    if (!$documentPath) {
        $errors[] = 'Please upload a valid ID document (PDF, JPG, PNG).';
    }
    if (empty($errors)) {
        save_application($formData, $documentPath);
        header('Location: success.php');
        exit;
    }
}
include 'includes/header.php';
?>
<main class="py-5">
    <section class="container">
        <div class="row align-items-center gy-4">
            <div class="col-lg-6">
                <h1 class="fw-bold">Apply Now</h1>
                <p class="text-muted">Completa nuestro formulario multipasos y envía tu solicitud con seguridad.</p>
                <div class="apply-info rounded-4 shadow-sm p-4 bg-white">
                    <h5>What you need</h5>
                    <ul class="text-muted small mb-0">
                        <li>Personal details</li>
                        <li>Valid ID upload</li>
                        <li>Last 4 digits of SSN</li>
                    </ul>
                </div>
            </div>
            <div class="col-lg-6">
                <?php if ($errors): ?>
                    <div class="alert alert-danger"><ul class="mb-0"><?php foreach ($errors as $error) echo '<li>' . $error . '</li>'; ?></ul></div>
                <?php endif; ?>
                <form id="applicationForm" method="post" enctype="multipart/form-data" class="rounded-4 shadow-lg p-4 bg-white">
                    <div class="form-step active">
                        <h5 class="mb-4">Step 1 — Personal Info</h5>
                        <div class="mb-3"><label class="form-label">Full Name</label><input type="text" name="full_name" class="form-control" value="<?= $formData['full_name'] ?>" required></div>
                        <div class="mb-3"><label class="form-label">Address</label><input type="text" name="address" class="form-control" value="<?= $formData['address'] ?>" required></div>
                    </div>
                    <div class="form-step">
                        <h5 class="mb-4">Step 2 — Contact</h5>
                        <div class="mb-3"><label class="form-label">Phone</label><input type="tel" name="phone" class="form-control" value="<?= $formData['phone'] ?>" required></div>
                        <div class="mb-3"><label class="form-label">Email</label><input type="email" name="email" class="form-control" value="<?= $formData['email'] ?>" required></div>
                    </div>
                    <div class="form-step">
                        <h5 class="mb-4">Step 3 — Identity</h5>
                        <div class="mb-3"><label class="form-label">Date of Birth</label><input type="date" name="dob" class="form-control" value="<?= $formData['dob'] ?>" required></div>
                        <div class="mb-3"><label class="form-label">SSN Last 4</label><input type="text" name="ssn_last4" class="form-control" maxlength="4" value="<?= $formData['ssn_last4'] ?>" required></div>
                    </div>
                    <div class="form-step">
                        <h5 class="mb-4">Step 4 — Upload</h5>
                        <div class="mb-3"><label class="form-label">Upload ID</label><input type="file" name="id_document" class="form-control" accept="application/pdf,image/jpeg,image/png" required></div>
                    </div>
                    <div class="form-step">
                        <h5 class="mb-4">Step 5 — Confirm</h5>
                        <p class="text-muted">Revisa tus datos y envía tu solicitud. Te contactaremos si necesitamos más información.</p>
                        <ul class="text-muted small">
                            <li>Full Name: <span id="summaryName"></span></li>
                            <li>Email: <span id="summaryEmail"></span></li>
                            <li>Phone: <span id="summaryPhone"></span></li>
                            <li>Address: <span id="summaryAddress"></span></li>
                        </ul>
                    </div>
                    <div class="d-flex justify-content-between align-items-center mt-4">
                        <button type="button" id="prevBtn" class="btn btn-outline-secondary">Back</button>
                        <button type="button" id="nextBtn" class="btn btn-success">Next</button>
                        <button type="submit" id="submitBtn" class="btn btn-success d-none">Submit Application</button>
                    </div>
                </form>
            </div>
        </div>
    </section>
</main>
<?php include 'includes/footer.php'; ?>
