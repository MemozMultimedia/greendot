const express = require('express');
const path = require('path');
const multer = require('multer');
const bcrypt = require('bcryptjs');
const db = require('../utils/db');
const mailer = require('../utils/mailer');
const { validateRequestForm, generateRequestNumber } = require('../utils/validation');

const router = express.Router();

const upload = multer({
  storage: multer.diskStorage({
    destination: (req, file, cb) => cb(null, path.join(__dirname, '..', 'uploads')),
    filename: (req, file, cb) => cb(null, `${Date.now()}-${file.originalname}`)
  }),
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png'];
    cb(null, allowedTypes.includes(file.mimetype));
  },
  limits: { fileSize: 5 * 1024 * 1024 }
});

router.get('/', (req, res) => {
  res.render('index', { formData: {}, errors: [] });
});

router.post('/submit', upload.single('documento'), async (req, res) => {
  const formData = req.body;
  const errors = validateRequestForm(formData);

  if (!req.file) {
    errors.push('Debe subir un documento válido (PDF/JPG/PNG).');
  }

  if (errors.length > 0) {
    return res.render('index', { formData, errors });
  }

  try {
    const numeroSolicitud = generateRequestNumber();
    await db.execute('INSERT INTO solicitudes (numero_solicitud, nombre, telefono, email, direccion, documento, tipo_reporte, comentarios, estado, fecha_creacion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())', [
      numeroSolicitud,
      formData.nombre,
      formData.telefono,
      formData.email,
      formData.direccion,
      `/uploads/${req.file.filename}`,
      formData.tipo_reporte,
      formData.comentarios,
      'Pendiente'
    ]);

    await mailer.sendConfirmationEmail(formData.email, formData.nombre, numeroSolicitud);
    req.flash('success', `Solicitud enviada con éxito. Tu número es ${numeroSolicitud}`);
    res.redirect('/success');
  } catch (err) {
    console.error(err);
    res.render('index', { formData, errors: ['Ocurrió un error procesando tu solicitud. Por favor intenta más tarde.'] });
  }
});

router.get('/success', (req, res) => {
  const message = req.flash('success');
  res.render('success', { message: message.length ? message[0] : 'Tu solicitud ha sido procesada correctamente.' });
});

router.get('/admin/login', (req, res) => {
  res.render('admin/login', { error: null });
});

router.post('/admin/login', async (req, res) => {
  const { username, password } = req.body;
  const adminUser = process.env.ADMIN_USER || 'admin';
  const adminPasswordHash = process.env.ADMIN_PASSWORD_HASH || '$2a$10$wz8fA7Vq5x3ekKDOMLxIh.5xkFzA3N5YlEoIq9ZsHirWFx3SGbBR6';

  if (username === adminUser && await bcrypt.compare(password, adminPasswordHash)) {
    req.session.admin = true;
    return res.redirect('/admin/dashboard');
  }

  res.render('admin/login', { error: 'Usuario o contraseña inválida.' });
});

router.get('/admin/dashboard', async (req, res) => {
  if (!req.session.admin) return res.redirect('/admin/login');

  const { search, estado, desde, hasta } = req.query;
  let query = 'SELECT * FROM solicitudes';
  const params = [];
  const clauses = [];

  if (search) {
    clauses.push('(nombre LIKE ? OR numero_solicitud LIKE ?)');
    params.push(`%${search}%`, `%${search}%`);
  }
  if (estado) {
    clauses.push('estado = ?');
    params.push(estado);
  }
  if (desde && hasta) {
    clauses.push('fecha_creacion BETWEEN ? AND ?');
    params.push(`${desde} 00:00:00`, `${hasta} 23:59:59`);
  }
  if (clauses.length) query += ` WHERE ${clauses.join(' AND ')}`;
  query += ' ORDER BY fecha_creacion DESC';

  const [solicitudes] = await db.execute(query, params);
  res.render('admin/dashboard', { solicitudes, filters: { search, estado, desde, hasta } });
});

router.get('/admin/view/:id', async (req, res) => {
  if (!req.session.admin) return res.redirect('/admin/login');
  const [rows] = await db.execute('SELECT * FROM solicitudes WHERE id = ?', [req.params.id]);
  if (!rows.length) return res.redirect('/admin/dashboard');
  res.render('admin/view_request', { solicitud: rows[0], estados: ['Pendiente', 'En revisión', 'Aprobado', 'Rechazado', 'Completado'] });
});

router.post('/admin/view/:id', async (req, res) => {
  if (!req.session.admin) return res.redirect('/admin/login');
  const { estado } = req.body;
  await db.execute('UPDATE solicitudes SET estado = ? WHERE id = ?', [estado, req.params.id]);
  res.redirect('/admin/dashboard');
});

router.get('/admin/logout', (req, res) => {
  req.session.destroy(() => res.redirect('/admin/login'));
});

module.exports = router;
