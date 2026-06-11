# GreenDot Reportes

Sitio web profesional para solicitar reportes online mediante formulario multipaso.

## Estructura del proyecto

- `index.php` - Página principal con formulario multipaso.
- `success.php` - Página de confirmación.
- `admin/` - Panel administrativo con login, dashboard y vista de solicitudes.
- `config.php` - Configuración de conexión a base de datos y constantes.
- `helpers.php` - Funciones reutilizables para DB, validación, carga de archivos y correo.
- `css/style.css` - Estilos personalizados.
- `js/scripts.js` - Lógica del formulario multipaso y firma digital.
- `uploads/` - Carpeta para documentos cargados.
- `database.sql` - Script para crear base de datos y tablas.

## Requisitos

- PHP 8.x
- MySQL / MariaDB
- Servidor web compatible (Apache, Nginx, cPanel, Hostinger)

## Configuración local

1. Copia el proyecto al directorio público de tu servidor.
2. Crea la base de datos con `database.sql`.
3. Ajusta `config.php` con los datos de conexión:
   - `DB_HOST`
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASS`
4. Asegúrate de que el directorio `uploads/` tenga permisos de escritura.

## Importar la base de datos

Usa el siguiente comando o tu herramienta de administración favorita:

```bash
mysql -u tu_usuario -p < database.sql
```

## Uso

- Accede a `index.php` para completar la solicitud.
- El formulario cumple los pasos:
  1. Información personal
  2. Identificación
  3. Datos del reporte
  4. Verificación
  5. Confirmación
- El admin puede entrar en `admin/login.php`.

## Panel administrativo

- `admin/login.php` - Login de administrador.
- `admin/dashboard.php` - Lista y filtros de solicitudes.
- `admin/view_request.php` - Ver solicitud y cambiar estado.
- `admin/logout.php` - Cerrar sesión.

## Notas de seguridad

- Se usa token CSRF básico en el formulario.
- La subida de archivos permite PDF, JPG, PNG.
- Las consultas usan PDO con parámetros preparados.
- Sanitiza datos de entrada en backend.

## Despliegue en Hostinger / cPanel / VPS

1. Copia todos los archivos al hosting.
2. Crea la base de datos MySQL y el usuario.
3. Importa `database.sql`.
4. Configura `config.php` con credenciales.
5. Asegura permisos de escritura en `uploads/`.
6. Entra en `admin/login.php` para administrar.

## Streamlit Viewer

También puedes ejecutar una vista rápida del repositorio usando Streamlit:

1. Instala dependencias de Python:
   ```bash
   pip install -r requirements.txt
   ```
2. Exporta variables de entorno:
   ```bash
   export GITHUB_REPO=MemozMultimedia/greendot
   export GITHUB_TOKEN=tu_token_de_github
   ```
3. Ejecuta:
   ```bash
   streamlit run greendot.py
   ```

## Personalización

- Cambia el texto de la página en `index.php`.
- Ajusta la paleta en `css/style.css`.
- Puedes mejorar la firma digital y CAPTCHA con reCAPTCHA para producción.
