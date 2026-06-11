const steps = Array.from(document.querySelectorAll('.form-step'));
const nextButton = document.getElementById('nextStep');
const prevButton = document.getElementById('prevStep');
const submitButton = document.getElementById('submitForm');
const form = document.getElementById('multiStepForm');
const summaryFields = {
    nombre: document.getElementById('summaryNombre'),
    email: document.getElementById('summaryEmail'),
    telefono: document.getElementById('summaryTelefono'),
    tipo_reporte: document.getElementById('summaryReporte'),
    motivo: document.getElementById('summaryMotivo'),
    comentarios: document.getElementById('summaryComentarios'),
};
const signaturePad = document.getElementById('signaturePad');
const signatureInput = document.getElementById('firmaData');
const clearSignatureButton = document.getElementById('clearSignature');

let currentStep = 0;

function updateSteps() {
    steps.forEach((step, index) => {
        step.classList.toggle('active', index === currentStep);
    });
    const stepIndicators = document.querySelectorAll('.step-indicator .step');
    stepIndicators.forEach((indicator, index) => {
        indicator.classList.toggle('active', index === currentStep);
    });
    prevButton.style.display = currentStep === 0 ? 'none' : 'inline-block';
    if (currentStep === steps.length - 1) {
        nextButton.classList.add('d-none');
        submitButton.classList.remove('d-none');
        fillSummary();
    } else {
        nextButton.classList.remove('d-none');
        submitButton.classList.add('d-none');
    }
}

function fillSummary() {
    steps[0].querySelectorAll('input, textarea, select').forEach((input) => {
        if (input.name && summaryFields[input.name]) {
            summaryFields[input.name].textContent = input.value;
        }
    });
}

function validateStep() {
    const inputs = steps[currentStep].querySelectorAll('input, textarea, select');
    let valid = true;
    inputs.forEach((input) => {
        if (!input.checkValidity()) {
            valid = false;
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
        }
    });
    return valid;
}

nextButton.addEventListener('click', () => {
    if (!validateStep()) return;
    currentStep = Math.min(currentStep + 1, steps.length - 1);
    updateSteps();
});

prevButton.addEventListener('click', () => {
    currentStep = Math.max(currentStep - 1, 0);
    updateSteps();
});

form.addEventListener('submit', (event) => {
    const signatureData = signatureInput.value;
    if (!signatureData) {
        alert('Por favor firma digitalmente para continuar.');
        currentStep = 3;
        updateSteps();
        event.preventDefault();
    }
});

function resizeCanvas() {
    const ratio = Math.max(window.devicePixelRatio || 1, 1);
    signaturePad.width = signaturePad.offsetWidth * ratio;
    signaturePad.height = signaturePad.offsetHeight * ratio;
    signaturePad.getContext('2d').scale(ratio, ratio);
}

function clearSignature() {
    const ctx = signaturePad.getContext('2d');
    ctx.clearRect(0, 0, signaturePad.width, signaturePad.height);
    signatureInput.value = '';
}

function setupSignature() {
    const ctx = signaturePad.getContext('2d');
    ctx.strokeStyle = '#0A2540';
    ctx.lineWidth = 2;
    let drawing = false;

    const startDrawing = (event) => {
        drawing = true;
        ctx.beginPath();
        ctx.moveTo(event.offsetX, event.offsetY);
    };

    const draw = (event) => {
        if (!drawing) return;
        ctx.lineTo(event.offsetX, event.offsetY);
        ctx.stroke();
    };

    const stopDrawing = () => {
        if (!drawing) return;
        drawing = false;
        signatureInput.value = signaturePad.toDataURL('image/png');
    };

    signaturePad.addEventListener('mousedown', startDrawing);
    signaturePad.addEventListener('mousemove', draw);
    window.addEventListener('mouseup', stopDrawing);
    signaturePad.addEventListener('touchstart', (event) => {
        event.preventDefault();
        const touch = event.touches[0];
        const rect = signaturePad.getBoundingClientRect();
        ctx.beginPath();
        ctx.moveTo(touch.clientX - rect.left, touch.clientY - rect.top);
        drawing = true;
    });
    signaturePad.addEventListener('touchmove', (event) => {
        event.preventDefault();
        if (!drawing) return;
        const touch = event.touches[0];
        const rect = signaturePad.getBoundingClientRect();
        ctx.lineTo(touch.clientX - rect.left, touch.clientY - rect.top);
        ctx.stroke();
    });
    signaturePad.addEventListener('touchend', () => {
        drawing = false;
        signatureInput.value = signaturePad.toDataURL('image/png');
    });
}

clearSignatureButton.addEventListener('click', clearSignature);
window.addEventListener('resize', resizeCanvas);
resizeCanvas();
setupSignature();
updateSteps();
