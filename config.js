module.exports = {
  DB_HOST: process.env.DB_HOST || '127.0.0.1',
  DB_NAME: process.env.DB_NAME || 'greendot',
  DB_USER: process.env.DB_USER || 'greendot_user',
  DB_PASS: process.env.DB_PASS || 'changeme',
  ADMIN_USER: process.env.ADMIN_USER || 'admin',
  ADMIN_PASSWORD_HASH: process.env.ADMIN_PASSWORD_HASH || '$2b$10$eip4ZIvr9pH6n7h0IrDXuOAl2sgDMSzlfIbxszgiX7vjXw3lNEmX.',
  SITE_EMAIL: process.env.SITE_EMAIL || 'noreply@greendot.local',
  SMTP_HOST: process.env.SMTP_HOST || 'smtp.example.com',
  SMTP_PORT: process.env.SMTP_PORT || 587,
  SMTP_SECURE: process.env.SMTP_SECURE === 'true',
  SMTP_USER: process.env.SMTP_USER || 'user@example.com',
  SMTP_PASS: process.env.SMTP_PASS || 'password',
};
