<?php
require_once __DIR__ . '/config.php';

function db_connect() {
    $dsn = 'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8mb4';
    return new PDO($dsn, DB_USER, DB_PASS, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
}

function sanitize($value) {
    return htmlspecialchars(trim($value), ENT_QUOTES, 'UTF-8');
}

function validate_app_form($data) {
    $errors = [];
    if (empty($data['full_name'])) $errors[] = 'Full name is required.';
    if (empty($data['address'])) $errors[] = 'Address is required.';
    if (empty($data['phone'])) $errors[] = 'Phone is required.';
    if (empty($data['email']) || !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) $errors[] = 'Valid email is required.';
    if (empty($data['dob'])) $errors[] = 'Date of birth is required.';
    if (empty($data['ssn_last4']) || !preg_match('/^[0-9]{4}$/', $data['ssn_last4'])) $errors[] = 'Last 4 digits of SSN are required.';
    return $errors;
}

function handle_upload($file) {
    if ($file['error'] !== UPLOAD_ERR_OK) {
        return false;
    }
    $mime = mime_content_type($file['tmp_name']);
    if (!in_array($mime, ALLOWED_FILE_TYPES, true)) {
        return false;
    }
    $ext = pathinfo($file['name'], PATHINFO_EXTENSION);
    $filename = uniqid('id_', true) . '.' . $ext;
    $target = UPLOAD_DIR . '/' . $filename;
    return move_uploaded_file($file['tmp_name'], $target) ? 'uploads/' . $filename : false;
}

function save_application($data, $document) {
    $db = db_connect();
    $stmt = $db->prepare('INSERT INTO applications (full_name, address, phone, email, dob, ssn_last4, document_path, status, created_at) VALUES (:full_name, :address, :phone, :email, :dob, :ssn_last4, :document_path, :status, NOW())');
    $stmt->execute([
        ':full_name' => $data['full_name'],
        ':address' => $data['address'],
        ':phone' => $data['phone'],
        ':email' => $data['email'],
        ':dob' => $data['dob'],
        ':ssn_last4' => $data['ssn_last4'],
        ':document_path' => $document,
        ':status' => 'Pending'
    ]);
    return $db->lastInsertId();
}

function admin_logged_in() {
    return !empty($_SESSION['admin_logged_in']);
}

function require_admin() {
    if (!admin_logged_in()) {
        header('Location: /admin/login.php');
        exit;
    }
}
