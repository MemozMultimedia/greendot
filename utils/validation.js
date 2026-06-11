function validateRequestForm(data) {
  const errors = [];
  if (!data.nombre) errors.push('El nombre completo es requerido.');
  if (!data.email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(data.email)) errors.push('El correo electrónico no es válido.');
  if (!data.telefono) errors.push('El teléfono es requerido.');
  if (!data.direccion || !data.ciudad || !data.estado || !data.codigo_postal) errors.push('Todos los datos de dirección son requeridos.');
  if (!data.tipo_documento || !data.numero_documento || !data.fecha_emision || !data.fecha_vencimiento) errors.push('Los datos de identificación son requeridos.');
  if (!data.tipo_reporte) errors.push('Selecciona el tipo de reporte solicitado.');
  if (!data.motivo) errors.push('Indica el motivo de la solicitud.');
  if (!data.acepta_terminos) errors.push('Debes aceptar los términos y condiciones.');
  return errors;
}

function generateRequestNumber() {
  return `GD-${Math.random().toString(36).substring(2, 10).toUpperCase()}`;
}

module.exports = { validateRequestForm, generateRequestNumber };
