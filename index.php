<?php
session_start();
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/helpers.php';

$errors = [];
$formData = [
    'nombre' => '',
    'fecha_nacimiento' => '',
    'telefono' => '',
    'email' => '',
    'direccion' => '',
    'ciudad' => '',
    'estado' => '',
    'codigo_postal' => '',
    'tipo_documento' => '',
    'numero_documento' => '',
    'fecha_emision' => '',
    'fecha_vencimiento' => '',
    'tipo_reporte' => '',
    'motivo' => '',
    'comentarios' => '',
    'acepta_terminos' => '',
];

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['submit_request'])) {
    if (!validate_csrf_token($_POST['csrf_token'] ?? '')) {
        $errors[] = 'Sesión inválida. Vuelve a cargar la página.';
    }

    $formData = array_merge($formData, array_map('trim', $_POST));
    $formData['acepta_terminos'] = isset($_POST['acepta_terminos']) ? '1' : '0';

    $errors = array_merge($errors, validate_request_form($formData));

    if (empty($errors)) {
        $uploadedFile = $_FILES['documento'] ?? null;
        $filePath = '';

        if ($uploadedFile && $uploadedFile['error'] === UPLOAD_ERR_OK) {
            $filePath = handle_file_upload($uploadedFile);
            if (!$filePath) {
                $errors[] = 'Error al subir el documento. Intente de nuevo.';
            }
        } else {
            $errors[] = 'Debe subir un documento válido (PDF/JPG/PNG).';
        }
    }

    if (empty($errors)) {
        try {
            $pdo = get_db_connection();
            $stmt = $pdo->prepare('INSERT INTO solicitudes (numero_solicitud, nombre, telefono, email, direccion, documento, tipo_reporte, comentarios, estado, fecha_creacion) VALUES (:numero_solicitud, :nombre, :telefono, :email, :direccion, :documento, :tipo_reporte, :comentarios, :estado, NOW())');
            $numeroSolicitud = generate_request_number();
            $stmt->execute([
                ':numero_solicitud' => $numeroSolicitud,
                ':nombre' => $formData['nombre'],
                ':telefono' => $formData['telefono'],
                ':email' => $formData['email'],
                ':direccion' => $formData['direccion'],
                ':documento' => $filePath,
                ':tipo_reporte' => $formData['tipo_reporte'],
                ':comentarios' => $formData['comentarios'],
                ':estado' => 'Pendiente',
            ]);

            send_confirmation_email($formData['email'], $formData['nombre'], $numeroSolicitud);
            $_SESSION['success_message'] = 'Solicitud enviada con éxito. Tu número es ' . $numeroSolicitud;
            header('Location: success.php');
            exit;
        } catch (PDOException $e) {
            error_log($e->getMessage());
            $errors[] = 'Ocurrió un error procesando tu solicitud. Por favor intenta más tarde.';
        }
    }
}

$csrfToken = generate_csrf_token();
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solicita tu Reporte en Línea</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-..." crossorigin="anonymous">
    <link rel="stylesheet" href="css/style.css">
</head>
<body class="bg-light text-dark">
    <header class="bg-dark text-white py-4 shadow-sm">
        <div class="container d-flex flex-column flex-md-row justify-content-between align-items-center gap-3">
            <div>
                <a href="#home" class="text-white text-decoration-none fs-4 fw-bold">GreenDot Reportes</a>
                <p class="mb-0 text-muted small">Plataforma segura de solicitudes online</p>
            </div>
            <nav class="d-flex gap-3">
                <a href="#beneficios" class="text-white text-decoration-none">Beneficios</a>
                <a href="#solicitud" class="text-white text-decoration-none">Solicitud</a>
                <a href="admin/login.php" class="btn btn-outline-light btn-sm">Administración</a>
            </nav>
        </div>
    </header>

    <main>
        <section id="home" class="hero-section py-5">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-lg-6">
                        <span class="badge bg-success mb-3">Reporte en Línea</span>
                        <h1 class="display-5 fw-semibold">Solicita tu Reporte en Línea</h1>
                        <p class="lead text-secondary">Completa tu solicitud rápida y segura. Gestionamos tu reporte con seguimiento digital y atención prioritaria.</p>
                        <a href="#solicitud" class="btn btn-primary btn-lg">Iniciar Solicitud</a>
                    </div>
                    <div class="col-lg-6">
                        <div class="hero-card shadow-lg p-4 rounded-4 bg-white border border-1 border-light">
                            <div class="d-flex justify-content-between mb-3">
                                <div>
                                    <span class="text-uppercase text-muted small">Estado</span>
                                    <h4 class="mb-0">Proceso Seguro</h4>
                                </div>
                                <div class="badge bg-success">En línea</div>
                            </div>
                            <p class="text-muted mb-4">Nuestro sistema procesa solicitudes y mantiene tus datos protegidos con cifrado avanzado.</p>
                            <div class="row text-center gy-3">
                                <div class="col-6">
                                    <div class="metric-card p-3 rounded-4 bg-light">
                                        <h5 class="mb-1">24/7</h5>
                                        <p class="mb-0 small text-muted">Soporte</p>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="metric-card p-3 rounded-4 bg-light">
                                        <h5 class="mb-1">5 min</h5>
                                        <p class="mb-0 small text-muted">Registro</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section id="beneficios" class="py-5 bg-white">
            <div class="container">
                <div class="text-center mb-5">
                    <span class="text-uppercase text-success fw-bold">Beneficios</span>
                    <h2 class="mt-3">Ventajas de solicitar tu reporte aquí</h2>
                </div>
                <div class="row g-4">
                    <div class="col-md-3">
                        <div class="feature-card p-4 rounded-4 shadow-sm h-100">
                            <div class="icon-circle bg-primary text-white mb-3"><svg width="24" height="24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg></div>
                            <h5>Proceso rápido</h5>
                            <p class="text-muted small">Formulario sencillo en pasos claros para completar tu solicitud sin complicaciones.</p>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="feature-card p-4 rounded-4 shadow-sm h-100">
                            <div class="icon-circle bg-primary text-white mb-3"><svg width="24" height="24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M5 12l5 5L20 7"/></svg></div>
                            <h5>Seguimiento online</h5>
                            <p class="text-muted small">Consulta el estado de tu solicitud desde cualquier dispositivo y en cualquier momento.</p>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="feature-card p-4 rounded-4 shadow-sm h-100">
                            <div class="icon-circle bg-primary text-white mb-3"><svg width="24" height="24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M12 1C6.48 1 2 5.48 2 11c0 3.87 2.19 7.24 5.35 8.96L12 23l4.65-3.04A9.957 9.957 0 0022 11c0-5.52-4.48-10-10-10zm0 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/></svg></div>
                            <h5>Protección de datos</h5>
                            <p class="text-muted small">Tus datos son tratados con confidencialidad y protegidos con mejores prácticas de seguridad.</p>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="feature-card p-4 rounded-4 shadow-sm h-100">
                            <div class="icon-circle bg-primary text-white mb-3"><svg width="24" height="24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M20 6H4v12h16V6zm-2 10H6V8h12v8zm-2-6h-2V8h2v2zm0 4h-2v-2h2v2z"/></svg></div>
                            <h5>Entrega digital</h5>
                            <p class="text-muted small">Recibe tu reporte en formato digital directamente a tu correo cuando esté listo.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section id="solicitud" class="py-5 bg-gradient">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-xl-10">
                        <div class="card shadow-lg border-0 rounded-5 p-4 p-lg-5">
                            <div class="card-body">
                                <div class="text-center mb-5">
                                    <h2 class="fw-bold">Formulario de Solicitud de Reporte</h2>
                                    <p class="text-muted">Completa los pasos y envía tu solicitud con seguridad y claridad.</p>
                                </div>
                                <?php if (!empty($errors)): ?>
                                    <div class="alert alert-danger">
                                        <ul class="mb-0">
                                            <?php foreach ($errors as $error): ?>
                                                <li><?= htmlspecialchars($error) ?></li>
                                            <?php endforeach; ?>
                                        </ul>
                                    </div>
                                <?php endif; ?>
                                <form id="multiStepForm" action="" method="post" enctype="multipart/form-data" novalidate>
                                    <input type="hidden" name="csrf_token" value="<?= htmlspecialchars($csrfToken) ?>">
                                    <div class="step-indicator d-flex justify-content-between mb-4">
                                        <div class="step active"><span>1</span> Personal</div>
                                        <div class="step"><span>2</span> Identificación</div>
                                        <div class="step"><span>3</span> Reporte</div>
                                        <div class="step"><span>4</span> Verificación</div>
                                        <div class="step"><span>5</span> Confirmación</div>
                                    </div>

                                    <div class="form-step active">
                                        <div class="row g-3">
                                            <div class="col-md-6">
                                                <label class="form-label">Nombre completo</label>
                                                <input type="text" class="form-control" name="nombre" value="<?= htmlspecialchars($formData['nombre']) ?>" required>
                                            </div>
                                            <div class="col-md-6">
                                                <label class="form-label">Fecha de nacimiento</label>
                                                <input type="date" class="form-control" name="fecha_nacimiento" value="<?= htmlspecialchars($formData['fecha_nacimiento']) ?>" required>
                                            </div>
                                            <div class="col-md-6">
                                                <label class="form-label">Teléfono</label>
                                                <input type="tel" class="form-control" name="telefono" value="<?= htmlspecialchars($formData['telefono']) ?>" required>
                                            </div>
                                            <div class="col-md-6">
                                                <label class="form-label">Correo electrónico</label>
                                                <input type="email" class="form-control" name="email" value="<?= htmlspecialchars($formData['email']) ?>" required>
                                            </div>
                                            <div class="col-md-6">
                                                <label class="form-label">Dirección</label>
                                                <input type="text" class="form-control" name="direccion" value="<?= htmlspecialchars($formData['direccion']) ?>" required>
                                            </div>
                                            <div class="col-md-3">
                                                <label class="form-label">Ciudad</label>
                                                <input type="text" class="form-control" name="ciudad" value="<?= htmlspecialchars($formData['ciudad']) ?>" required>
                                            </div>
                                            <div class="col-md-3">
                                                <label class="form-label">Estado</label>
                                                <input type="text" class="form-control" name="estado" value="<?= htmlspecialchars($formData['estado']) ?>" required>
                                            </div>
                                            <div class="col-md-4">
                                                <label class="form-label">Código postal</label>
                                                <input type="text" class="form-control" name="codigo_postal" value="<?= htmlspecialchars($formData['codigo_postal']) ?>" required>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="form-step">
                                        <div class="row g-3">
                                            <div class="col-md-6">
                                                <label class="form-label">Tipo de documento</label>
                                                <select class="form-select" name="tipo_documento" required>
                                                    <option value="">Selecciona</option>
                                                    <option value="DNI" <?= $formData['tipo_documento'] === 'DNI' ? 'selected' : '' ?>>DNI</option>
                                                    <option value="Pasaporte" <?= $formData['tipo_documento'] === 'Pasaporte' ? 'selected' : '' ?>>Pasaporte</option>
                                                    <option value="Otro" <?= $formData['tipo_documento'] === 'Otro' ? 'selected' : '' ?>>Otro</option>
                                                </select>
                                            </div>
                                            <div class="col-md-6">
                                                <label class="form-label">Número de documento</label>
                                                <input type="text" class="form-control" name="numero_documento" value="<?= htmlspecialchars($formData['numero_documento']) ?>" required>
                                            </div>
                                            <div class="col-md-6">
                                                <label class="form-label">Fecha de emisión</label>
                                                <input type="date" class="form-control" name="fecha_emision" value="<?= htmlspecialchars($formData['fecha_emision']) ?>" required>
                                            </div>
                                            <div class="col-md-6">
                                                <label class="form-label">Fecha de vencimiento</label>
                                                <input type="date" class="form-control" name="fecha_vencimiento" value="<?= htmlspecialchars($formData['fecha_vencimiento']) ?>" required>
                                            </div>
                                            <div class="col-12">
                                                <label class="form-label">Subida de documento</label>
                                                <input type="file" class="form-control" name="documento" accept="application/pdf,image/jpeg,image/png" required>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="form-step">
                                        <div class="row g-3">
                                            <div class="col-md-6">
                                                <label class="form-label">Tipo de reporte solicitado</label>
                                                <select class="form-select" name="tipo_reporte" required>
                                                    <option value="">Selecciona</option>
                                                    <option value="Financiero" <?= $formData['tipo_reporte'] === 'Financiero' ? 'selected' : '' ?>>Financiero</option>
                                                    <option value="Laboral" <?= $formData['tipo_reporte'] === 'Laboral' ? 'selected' : '' ?>>Laboral</option>
                                                    <option value="Legal" <?= $formData['tipo_reporte'] === 'Legal' ? 'selected' : '' ?>>Legal</option>
                                                </select>
                                            </div>
                                            <div class="col-12">
                                                <label class="form-label">Motivo de la solicitud</label>
                                                <textarea class="form-control" name="motivo" rows="3" required><?= htmlspecialchars($formData['motivo']) ?></textarea>
                                            </div>
                                            <div class="col-12">
                                                <label class="form-label">Comentarios adicionales</label>
                                                <textarea class="form-control" name="comentarios" rows="3"><?= htmlspecialchars($formData['comentarios']) ?></textarea>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="form-step">
                                        <div class="row g-4">
                                            <div class="col-12">
                                                <div class="form-check form-switch p-3 rounded-4 border bg-light">
                                                    <input class="form-check-input" type="checkbox" id="acceptTerms" name="acepta_terminos" value="1" <?= $formData['acepta_terminos'] === '1' ? 'checked' : '' ?> required>
                                                    <label class="form-check-label" for="acceptTerms">Acepto los términos y condiciones</label>
                                                </div>
                                            </div>
                                            <div class="col-12">
                                                <label class="form-label">Firma digital</label>
                                                <canvas id="signaturePad" class="signature-pad rounded-4 border bg-white" width="100%" height="180"></canvas>
                                                <input type="hidden" name="firma" id="firmaData">
                                                <button type="button" id="clearSignature" class="btn btn-sm btn-outline-secondary mt-2">Limpiar firma</button>
                                            </div>
                                            <div class="col-12">
                                                <div class="form-check p-3 rounded-4 border bg-light">
                                                    <input class="form-check-input" type="checkbox" id="captchaCheck" required>
                                                    <label class="form-check-label" for="captchaCheck">No soy un robot</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="form-step">
                                        <div class="summary-box p-4 rounded-4 bg-light border">
                                            <h4 class="mb-3">Resumen de solicitud</h4>
                                            <div class="row">
                                                <div class="col-md-6 mb-3"><strong>Nombre:</strong> <span id="summaryNombre"></span></div>
                                                <div class="col-md-6 mb-3"><strong>Email:</strong> <span id="summaryEmail"></span></div>
                                                <div class="col-md-6 mb-3"><strong>Teléfono:</strong> <span id="summaryTelefono"></span></div>
                                                <div class="col-md-6 mb-3"><strong>Tipo de reporte:</strong> <span id="summaryReporte"></span></div>
                                                <div class="col-12 mb-3"><strong>Motivo:</strong> <span id="summaryMotivo"></span></div>
                                                <div class="col-12 mb-3"><strong>Comentarios:</strong> <span id="summaryComentarios"></span></div>
                                            </div>
                                            <div class="alert alert-info mt-3">Tu número de solicitud se generará automáticamente cuando envíes el formulario.</div>
                                        </div>
                                    </div>

                                    <div class="d-flex justify-content-between align-items-center mt-4">
                                        <button type="button" class="btn btn-outline-secondary" id="prevStep">Anterior</button>
                                        <button type="button" class="btn btn-secondary" id="nextStep">Siguiente</button>
                                        <button type="submit" class="btn btn-primary d-none" id="submitForm" name="submit_request">Enviar Solicitud</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer class="py-4 bg-dark text-white text-center">
        <div class="container">
            <p class="mb-1">© 2026 GreenDot Reportes. Todos los derechos reservados.</p>
            <p class="small mb-0">Diseño premium para solicitudes en línea con seguridad y experiencia moderna.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-..." crossorigin="anonymous"></script>
    <script src="js/scripts.js"></script>
</body>
</html>
