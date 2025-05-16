/**
 * NEO GAIAM - Language Switcher
 * 
 * A language switcher component for multilingual support
 * that works with WordPress multilingual plugins.
 */
class LanguageSwitcher {
  constructor(selector, options = {}) {
    this.container = document.querySelector(selector);
    if (!this.container) return;
    
    this.options = {
      showFlags: this.container.dataset.showFlags === 'true',
      ...options
    };
    
    // Get available languages from buttons
    this.languages = Array.from(this.container.querySelectorAll('.language-option'))
      .map(btn => btn.dataset.lang);
    
    // Get current language from HTML lang attribute or default to first language
    this.currentLang = document.documentElement.lang.split('-')[0] || this.languages[0] || 'en';
    
    // Initialize
    this.init();
  }
  
  init() {
    const buttons = this.container.querySelectorAll('.language-option');
    
    // Set initial active state
    buttons.forEach(btn => {
      if (btn.dataset.lang === this.currentLang) {
        btn.classList.add('active');
      }
      
      // Add click handler
      btn.addEventListener('click', () => this.switchLanguage(btn.dataset.lang));
    });
  }
  
  switchLanguage(lang) {
    if (!this.languages.includes(lang)) return;
    
    console.log('Switching language to:', lang);
    
    // Update active button
    const buttons = this.container.querySelectorAll('.language-option');
    buttons.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.lang === lang);
    });
    
    // In a real WordPress implementation, this would redirect to the translated page
    // This would integrate with WPML or Polylang
    
    // For now, we'll just change the HTML lang attribute for demonstration
    document.documentElement.lang = lang;
    
    // Dispatch a custom event that other components can listen for
    const event = new CustomEvent('languageChanged', { detail: { language: lang } });
    document.dispatchEvent(event);
  }
}

// Initialize on document ready
document.addEventListener('DOMContentLoaded', function() {
  const containers = document.querySelectorAll('.neogaiam-language-switcher');
  containers.forEach(container => {
    new LanguageSwitcher('#' + container.id);
  });
});
