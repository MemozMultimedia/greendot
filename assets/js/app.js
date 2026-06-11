const steps = document.querySelectorAll('.form-step');
const nextBtn = document.getElementById('nextBtn');
const prevBtn = document.getElementById('prevBtn');
const submitBtn = document.getElementById('submitBtn');
const form = document.getElementById('applicationForm');
let currentStep = 0;

function updateForm() {
    steps.forEach((step, index) => step.classList.toggle('active', index === currentStep));
    prevBtn.style.display = currentStep === 0 ? 'none' : 'inline-block';
    if (currentStep === steps.length - 1) {
        nextBtn.classList.add('d-none');
        submitBtn.classList.remove('d-none');
        document.getElementById('summaryName').textContent = form.querySelector('[name=full_name]').value;
        document.getElementById('summaryEmail').textContent = form.querySelector('[name=email]').value;
        document.getElementById('summaryPhone').textContent = form.querySelector('[name=phone]').value;
        document.getElementById('summaryAddress').textContent = form.querySelector('[name=address]').value;
    } else {
        nextBtn.classList.remove('d-none');
        submitBtn.classList.add('d-none');
    }
}
nextBtn?.addEventListener('click', () => { if (currentStep < steps.length - 1) { currentStep += 1; updateForm(); } });
prevBtn?.addEventListener('click', () => { if (currentStep > 0) { currentStep -= 1; updateForm(); } });
form?.addEventListener('submit', () => { if (currentStep < steps.length - 1) { currentStep = steps.length - 1; updateForm(); event.preventDefault(); }});
updateForm();
