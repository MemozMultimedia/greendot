const nodemailer = require('nodemailer');
const config = require('../config');

const transporter = nodemailer.createTransport({
  host: config.SMTP_HOST,
  port: config.SMTP_PORT,
  secure: config.SMTP_SECURE,
  auth: {
    user: config.SMTP_USER,
    pass: config.SMTP_PASS
  }
});

async function sendConfirmationEmail(email, nombre, numeroSolicitud) {
  const message = {
    from: config.SITE_EMAIL,
    to: email,
    subject: 'Confirmación de solicitud de reporte',
    text: `Hola ${nombre},\n\nHemos recibido tu solicitud. Tu número de solicitud es: ${numeroSolicitud}.\n\nGracias por confiar en nosotros.\n`
  };
  await transporter.sendMail(message);
}

module.exports = { sendConfirmationEmail };
