<?php

function get_db_connection()
{
    $dsn = 'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8mb4';
    return new PDO($dsn, DB_USER, DB_PASS, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ]);
}

function generate_csrf_token()
{
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

function validate_csrf_token($token)
{
    return hash_equals($_SESSION['csrf_token'] ?? '', $token);
}

function sanitize_text($value)
{
    return filter_var(trim($value), FILTER_UNSAFE_RAW);
}

function validate_request_form($data)
{
    $errors = [];

    if (empty($data['nombre'])) {
        $errors[] = 'El nombre completo es requerido.';
    }
    if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
        $errors[] = 'El correo electrónico no es válido.';
    }
    if (empty($data['telefono'])) {
        $errors[] = 'El teléfono es requerido.';
    }
    if (empty($data['direccion']) || empty($data['ciudad']) || empty($data['estado']) || empty($data['codigo_postal'])) {
        $errors[] = 'Todos los datos de dirección son requeridos.';
    }
    if (empty($data['tipo_documento']) || empty($data['numero_documento']) || empty($data['fecha_emision']) || empty($data['fecha_vencimiento'])) {
        $errors[] = 'Los datos de identificación son requeridos.';
    }
    if (empty($data['tipo_reporte'])) {
        $errors[] = 'Selecciona el tipo de reporte solicitado.';
    }
    if (empty($data['motivo'])) {
        $errors[] = 'Indica el motivo de la solicitud.';
    }
    if ($data['acepta_terminos'] !== '1') {
        $errors[] = 'Debes aceptar los términos y condiciones.';
    }

    return $errors;
}

function handle_file_upload($file)
{
    if (!in_array(mime_content_type($file['tmp_name']), ALLOWED_FILE_TYPES, true)) {
        return false;
    }

    if (!is_dir(UPLOAD_DIR) && !mkdir(UPLOAD_DIR, 0755, true)) {
        return false;
    }

    $ext = pathinfo($file['name'], PATHINFO_EXTENSION);
    $filename = bin2hex(random_bytes(16)) . '.' . $ext;
    $destination = UPLOAD_DIR . '/' . $filename;

    if (move_uploaded_file($file['tmp_name'], $destination)) {
        return 'uploads/' . $filename;
    }

    return false;
}

function generate_request_number()
{
    return 'GD-' . strtoupper(bin2hex(random_bytes(4)));
}

function send_confirmation_email($email, $nombre, $numeroSolicitud)
{
    $subject = 'Confirmación de solicitud de reporte';
    $message = "Hola $nombre,\n\nHemos recibido tu solicitud. Tu número de solicitud es: $numeroSolicitud.\n\nGracias por confiar en nosotros.\n";
    $headers = 'From: ' . SITE_EMAIL . "\r\n" . 'Reply-To: ' . SITE_EMAIL . "\r\n";

    @mail($email, $subject, $message, $headers);
}

function sanitize_input_array($data)
{
    return array_map('sanitize_text', $data);
}
