/**
 * NEO GAIAM - Booking Form
 * 
 * An interactive booking form for services with
 * support for service levels and astrological information.
 */
class BookingForm {
  constructor(selector, options = {}) {
    this.container = document.querySelector(selector);
    if (!this.container) return;
    
    this.options = {
      serviceId: this.container.dataset.serviceId || '1',
      serviceName: this.container.dataset.serviceName || 'Service',
      hasLevels: this.container.dataset.hasLevels === 'true',
      astrologyFields: this.container.dataset.astrologyFields === 'true',
      formTitle: this.container.dataset.formTitle || 'Book Your Session',
      submitText: this.container.dataset.submitText || 'Confirm Booking',
      ...options
    };
    
    // Language settings
    this.language = document.documentElement.lang || 'en';
    
    // Initialize form
    this.init();
  }
  
  init() {
    // Clear loading message
    this.container.innerHTML = '';
    
    // Create form
    const form = document.createElement('form');
    form.className = 'booking-form';
    form.id = 'booking-form-' + this.options.serviceId;
    
    // Left column (form fields)
    const leftCol = document.createElement('div');
    leftCol.className = 'booking-form-left-column';
    
    // Personal information section
    const personalInfo = this.createPersonalInfoSection();
    leftCol.appendChild(personalInfo);
    
    // Date and time section
    const dateTime = this.createDateTimeSection();
    leftCol.appendChild(dateTime);
    
    // Service level section (if enabled)
    if (this.options.hasLevels) {
      const serviceLevel = this.createServiceLevelSection();
      leftCol.appendChild(serviceLevel);
    }
    
    // Astrology section (if enabled)
    if (this.options.astrologyFields) {
      const astrology = this.createAstrologySection();
      leftCol.appendChild(astrology);
    }
    
    // Right column (summary and submit)
    const rightCol = document.createElement('div');
    rightCol.className = 'booking-form-right-column';
    
    // Summary section
    const summary = this.createSummarySection();
    rightCol.appendChild(summary);
    
    // Submit button
    const submitBtn = document.createElement('button');
    submitBtn.type = 'submit';
    submitBtn.className = 'booking-form-submit';
    submitBtn.textContent = this.options.submitText;
    rightCol.appendChild(submitBtn);
    
    // Assemble the form
    form.appendChild(leftCol);
    form.appendChild(rightCol);
    
    // Form submission handler
    form.addEventListener('submit', (e) => this.handleSubmit(e));
    
    // Add form to container
    this.container.appendChild(form);
  }
  
  createPersonalInfoSection() {
    const section = document.createElement('div');
    section.className = 'booking-form-section personal-info-section';
    
    const heading = document.createElement('h3');
    heading.className = 'booking-form-heading';
    heading.textContent = this.options.formTitle;
    section.appendChild(heading);
    
    const personalFields = [
      { name: 'fullName', label: this.translate('Full Name'), type: 'text', required: true },
      { name: 'email', label: this.translate('Email'), type: 'email', required: true },
      { name: 'phone', label: this.translate('Phone'), type: 'tel', required: true }
    ];
    
    personalFields.forEach(field => {
      const fieldEl = this.createFormField(field);
      section.appendChild(fieldEl);
    });
    
    return section;
  }
  
  createDateTimeSection() {
    const section = document.createElement('div');
    section.className = 'booking-form-section date-time-section';
    
    const heading = document.createElement('h3');
    heading.className = 'booking-form-heading';
    heading.textContent = this.translate('Date & Time');
    section.appendChild(heading);
    
    // Date field
    const dateField = this.createFormField({
      name: 'date',
      label: this.translate('Select Date'),
      type: 'date',
      required: true
    });
    section.appendChild(dateField);
    
    // Time field
    const timeField = this.createFormField({
      name: 'time',
      label: this.translate('Select Time'),
      type: 'select',
      required: true,
      options: this.getTimeSlotOptions()
    });
    section.appendChild(timeField);
    
    return section;
  }
  
  createServiceLevelSection() {
    const section = document.createElement('div');
    section.className = 'booking-form-section service-level-section';
    
    const heading = document.createElement('h3');
    heading.className = 'booking-form-heading';
    heading.textContent = this.translate('Service Level');
    section.appendChild(heading);
    
    const levelField = this.createFormField({
      name: 'serviceLevel',
      label: this.translate('Select Service Level'),
      type: 'select',
      required: true,
      options: [
        { value: 'standard', label: this.translate('Standard') },
        { value: 'argentum', label: 'Argentum' },
        { value: 'aurum', label: 'Aurum' }
      ]
    });
    section.appendChild(levelField);
    
    return section;
  }
  
  createAstrologySection() {
    const section = document.createElement('div');
    section.className = 'booking-form-section astrology-section';
    
    const heading = document.createElement('h3');
    heading.className = 'booking-form-heading';
    heading.textContent = this.translate('Astrological Information');
    section.appendChild(heading);
    
    const astrologyFields = [
      { name: 'birthDate', label: this.translate('Birth Date'), type: 'date', required: false },
      { name: 'birthTime', label: this.translate('Birth Time (if known)'), type: 'time', required: false },
      { name: 'birthPlace', label: this.translate('Birth Place'), type: 'text', required: false },
      { name: 'questionForReading', label: this.translate('Specific Questions for Reading'), type: 'textarea', required: false }
    ];
    
    astrologyFields.forEach(field => {
      const fieldEl = this.createFormField(field);
      section.appendChild(fieldEl);
    });
    
    return section;
  }
  
  createSummarySection() {
    const section = document.createElement('div');
    section.className = 'booking-form-section summary-section';
    
    const heading = document.createElement('h3');
    heading.className = 'booking-form-heading';
    heading.textContent = this.translate('Booking Summary');
    section.appendChild(heading);
    
    // Service summary items
    const summaryItems = [
      { label: this.translate('Service'), value: this.options.serviceName },
      { label: this.translate('Duration'), value: '60 minutes' },
      { label: this.translate('Price'), value: '$120' }
    ];
    
    summaryItems.forEach(item => {
      const itemRow = document.createElement('div');
      itemRow.className = 'summary-item';
      
      const itemLabel = document.createElement('div');
      itemLabel.className = 'summary-item-label';
      itemLabel.textContent = item.label;
      
      const itemValue = document.createElement('div');
      itemValue.className = 'summary-item-value';
      itemValue.textContent = item.value;
      
      itemRow.appendChild(itemLabel);
      itemRow.appendChild(itemValue);
      section.appendChild(itemRow);
    });
    
    // What to expect section
    const expectationTitle = document.createElement('h4');
    expectationTitle.className = 'booking-form-subheading';
    expectationTitle.textContent = this.translate('What to expect');
    section.appendChild(expectationTitle);
    
    const expectationText = document.createElement('p');
    expectationText.className = 'booking-form-text';
    expectationText.textContent = this.translate('After booking, you\'ll receive a confirmation email with details about your session and any preparation required.');
    section.appendChild(expectationText);
    
    return section;
  }
  
  createFormField({ name, label, type, required, options = [] }) {
    const fieldWrapper = document.createElement('div');
    fieldWrapper.className = 'form-field-wrapper';
    
    const fieldLabel = document.createElement('label');
    fieldLabel.htmlFor = name;
    fieldLabel.className = 'form-field-label';
    fieldLabel.textContent = label;
    
    if (required) {
      const requiredMark = document.createElement('span');
      requiredMark.className = 'required-mark';
      requiredMark.textContent = ' *';
      fieldLabel.appendChild(requiredMark);
    }
    
    fieldWrapper.appendChild(fieldLabel);
    
    let input;
    
    switch (type) {
      case 'textarea':
        input = document.createElement('textarea');
        input.rows = 4;
        break;
      case 'select':
        input = document.createElement('select');
        options.forEach(opt => {
          const option = document.createElement('option');
          option.value = opt.value;
          option.textContent = opt.label;
          input.appendChild(option);
        });
        break;
      default:
        input = document.createElement('input');
        input.type = type;
    }
    
    input.id = name;
    input.name = name;
    input.className = 'form-field-input form-field-' + type;
    if (required) input.required = true;
    
    fieldWrapper.appendChild(input);
    
    // Error message container
    const errorMsg = document.createElement('div');
    errorMsg.className = 'form-field-error';
    fieldWrapper.appendChild(errorMsg);
    
    return fieldWrapper;
  }
  
  getTimeSlotOptions() {
    // Sample time slots
    return [
      { value: '09:00', label: '9:00 AM' },
      { value: '10:00', label: '10:00 AM' },
      { value: '11:00', label: '11:00 AM' },
      { value: '13:00', label: '1:00 PM' },
      { value: '14:00', label: '2:00 PM' },
      { value: '15:00', label: '3:00 PM' },
      { value: '16:00', label: '4:00 PM' }
    ];
  }
  
  handleSubmit(e) {
    e.preventDefault();
    
    // Validate form
    if (!this.validateForm()) {
      return;
    }
    
    // Get form data
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    // In a real WordPress implementation, this would submit to a form processing script
    console.log('Submitting booking data:', data);
    
    // Show success message
    this.showMessage(
      this.translate('Booking Submitted'),
      this.translate('Thank you for your booking request. We will contact you shortly to confirm your appointment.'),
      'success'
    );
    
    // Reset form
    e.target.reset();
  }
  
  validateForm() {
    // Reset error messages
    const errorElements = this.container.querySelectorAll('.form-field-error');
    errorElements.forEach(el => el.textContent = '');
    
    // Simple validation example
    let isValid = true;
    
    // Here you would add more validation as needed
    
    return isValid;
  }
  
  showMessage(title, message, type = 'info') {
    // Create message element
    const msgElement = document.createElement('div');
    msgElement.className = `booking-form-message message-${type}`;
    
    const msgTitle = document.createElement('h3');
    msgTitle.className = 'message-title';
    msgTitle.textContent = title;
    
    const msgText = document.createElement('p');
    msgText.className = 'message-text';
    msgText.textContent = message;
    
    const closeBtn = document.createElement('button');
    closeBtn.className = 'message-close';
    closeBtn.textContent = '×';
    closeBtn.addEventListener('click', () => msgElement.remove());
    
    msgElement.appendChild(closeBtn);
    msgElement.appendChild(msgTitle);
    msgElement.appendChild(msgText);
    
    // Add to container
    this.container.appendChild(msgElement);
    
    // Auto-remove after delay for success/info messages
    if (type !== 'error') {
      setTimeout(() => {
        msgElement.remove();
      }, 5000);
    }
  }
  
  translate(text) {
    // Simple translation function
    // In a real implementation, this would use a proper translation system
    const translations = {
      'en': {
        'Full Name': 'Full Name',
        'Email': 'Email',
        'Phone': 'Phone',
        'Date & Time': 'Date & Time',
        'Select Date': 'Select Date',
        'Select Time': 'Select Time',
        'Service Level': 'Service Level',
        'Select Service Level': 'Select Service Level',
        'Standard': 'Standard',
        'Astrological Information': 'Astrological Information',
        'Birth Date': 'Birth Date',
        'Birth Time (if known)': 'Birth Time (if known)',
        'Birth Place': 'Birth Place',
        'Specific Questions for Reading': 'Specific Questions for Reading',
        'Booking Summary': 'Booking Summary',
        'Service': 'Service',
        'Duration': 'Duration',
        'Price': 'Price',
        'What to expect': 'What to expect',
        'After booking, you\'ll receive a confirmation email with details about your session and any preparation required.': 'After booking, you\'ll receive a confirmation email with details about your session and any preparation required.',
        'Booking Submitted': 'Booking Submitted',
        'Thank you for your booking request. We will contact you shortly to confirm your appointment.': 'Thank you for your booking request. We will contact you shortly to confirm your appointment.'
      },
      'es': {
        'Full Name': 'Nombre Completo',
        'Email': 'Correo Electrónico',
        'Phone': 'Teléfono',
        'Date & Time': 'Fecha y Hora',
        'Select Date': 'Seleccionar Fecha',
        'Select Time': 'Seleccionar Hora',
        'Service Level': 'Nivel de Servicio',
        'Select Service Level': 'Seleccionar Nivel de Servicio',
        'Standard': 'Estándar',
        'Astrological Information': 'Información Astrológica',
        'Birth Date': 'Fecha de Nacimiento',
        'Birth Time (if known)': 'Hora de Nacimiento (si la conoces)',
        'Birth Place': 'Lugar de Nacimiento',
        'Specific Questions for Reading': 'Preguntas Específicas para la Lectura',
        'Booking Summary': 'Resumen de la Reserva',
        'Service': 'Servicio',
        'Duration': 'Duración',
        'Price': 'Precio',
        'What to expect': 'Qué esperar',
        'After booking, you\'ll receive a confirmation email with details about your session and any preparation required.': 'Después de la reserva, recibirás un correo electrónico de confirmación con detalles sobre tu sesión y cualquier preparación necesaria.',
        'Booking Submitted': 'Reserva Enviada',
        'Thank you for your booking request. We will contact you shortly to confirm your appointment.': 'Gracias por tu solicitud de reserva. Nos pondremos en contacto contigo pronto para confirmar tu cita.'
      }
    };
    
    return translations[this.language]?.[text] || text;
  }
}

// Initialize on document ready
document.addEventListener('DOMContentLoaded', function() {
  const containers = document.querySelectorAll('.neogaiam-booking-form');
  containers.forEach(container => {
    new BookingForm('#' + container.id);
  });
});
