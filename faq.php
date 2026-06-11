<?php define('SITE_TITLE', 'GreenDot Fintech | FAQ'); include 'includes/header.php'; ?>
<main class="py-5">
    <section class="container">
        <div class="text-center mb-5">
            <h1 class="fw-bold">Preguntas frecuentes</h1>
            <p class="text-muted">Resuelva sus dudas con nuestra guía rápida sobre el servicio.</p>
        </div>
        <div class="accordion" id="faqAccordion">
            <div class="accordion-item">
                <h2 class="accordion-header" id="faqOne">
                    <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                        ¿Cómo solicito un reporte?
                    </button>
                </h2>
                <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="faqOne" data-bs-parent="#faqAccordion">
                    <div class="accordion-body text-muted">Visita la página Apply Now y completa el formulario multipasos con tus datos y documento de identidad.</div>
                </div>
            </div>
            <div class="accordion-item">
                <h2 class="accordion-header" id="faqTwo">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                        ¿Está seguro mi documento de identidad?
                    </button>
                </h2>
                <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="faqTwo" data-bs-parent="#faqAccordion">
                    <div class="accordion-body text-muted">Sí. El proceso utiliza un entorno seguro y encriptado para proteger tus archivos e información personal.</div>
                </div>
            </div>
            <div class="accordion-item">
                <h2 class="accordion-header" id="faqThree">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                        ¿Cuánto tarda la revisión?
                    </button>
                </h2>
                <div id="collapseThree" class="accordion-collapse collapse" aria-labelledby="faqThree" data-bs-parent="#faqAccordion">
                    <div class="accordion-body text-muted">Los tiempos suelen variar entre 24 y 48 horas dependiendo del volumen de solicitudes y verificación del documento.</div>
                </div>
            </div>
            <div class="accordion-item">
                <h2 class="accordion-header" id="faqFour">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFour" aria-expanded="false" aria-controls="collapseFour">
                        ¿Puedo cambiar mi solicitud?
                    </button>
                </h2>
                <div id="collapseFour" class="accordion-collapse collapse" aria-labelledby="faqFour" data-bs-parent="#faqAccordion">
                    <div class="accordion-body text-muted">Contáctanos cuanto antes y te indicaremos los pasos para ajustar la información antes de procesar la solicitud.</div>
                </div>
            </div>
        </div>
    </section>
</main>
<?php include 'includes/footer.php'; ?>
