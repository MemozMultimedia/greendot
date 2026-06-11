<?php
define('SITE_TITLE', 'GreenDot Fintech | Contact');
include 'includes/header.php';
$message = '';
$errors = [];
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = sanitize($_POST['name'] ?? '');
    $email = sanitize($_POST['email'] ?? '');
    $messageText = sanitize($_POST['message'] ?? '');
    if (!$name || !$email || !$messageText) {
        $errors[] = 'Please complete all fields.';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = 'Please provide a valid email address.';
    } else {
        $message = 'Thank you for contacting us. We will respond shortly.';
    }
}
?>
<main class="py-5">
    <section class="container">
        <div class="row align-items-center gy-4">
            <div class="col-lg-6">
                <h1 class="fw-bold">Contáctanos</h1>
                <p class="text-muted">Estamos listos para ayudarte con tu solicitud y resolver cualquier duda.</p>
                <div class="contact-card rounded-4 shadow-sm p-4 bg-white">
                    <h5 class="mb-3">Soporte</h5>
                    <p class="small text-muted mb-1">support@greendotfintech.com</p>
                    <p class="small text-muted">+1 (555) 123-4567</p>
                </div>
            </div>
            <div class="col-lg-6">
                <?php if ($message): ?>
                    <div class="alert alert-success"><?= $message ?></div>
                <?php endif; ?>
                <?php if ($errors): ?>
                    <div class="alert alert-danger"><ul class="mb-0"><?php foreach ($errors as $error) echo '<li>' . $error . '</li>'; ?></ul></div>
                <?php endif; ?>
                <form method="post" class="contact-form rounded-4 shadow-lg p-4 bg-white">
                    <div class="mb-3"><label class="form-label">Name</label><input type="text" name="name" class="form-control" value="<?= $name ?? '' ?>"></div>
                    <div class="mb-3"><label class="form-label">Email</label><input type="email" name="email" class="form-control" value="<?= $email ?? '' ?>"></div>
                    <div class="mb-3"><label class="form-label">Message</label><textarea name="message" rows="5" class="form-control"><?= $messageText ?? '' ?></textarea></div>
                    <button class="btn btn-success">Send Message</button>
                </form>
            </div>
        </div>
    </section>
</main>
<?php include 'includes/footer.php'; ?>
