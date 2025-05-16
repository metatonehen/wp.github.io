/**
 * NEO GAIAM - Star Field
 * 
 * A cosmic background with animated stars
 * for creating an immersive cosmic atmosphere.
 */
class StarField {
  constructor(selector, options = {}) {
    this.container = document.querySelector(selector);
    if (!this.container) return;
    
    this.options = {
      count: parseInt(this.container.dataset.count) || 200,
      color: this.container.dataset.color || '#ffffff',
      size: parseFloat(this.container.dataset.size) || 2,
      speed: parseFloat(this.container.dataset.speed) || 0.5,
      twinkle: true,
      ...options
    };
    
    // Initialize
    this.init();
  }
  
  init() {
    // Make sure container has position relative
    if (window.getComputedStyle(this.container).position === 'static') {
      this.container.style.position = 'relative';
    }
    
    // Create stars
    for (let i = 0; i < this.options.count; i++) {
      this.createStar();
    }
  }
  
  createStar() {
    const star = document.createElement('div');
    star.className = 'star-field-star';
    
    // Random position
    const x = Math.random() * 100;
    const y = Math.random() * 100;
    
    // Random size variation
    const sizeVariation = Math.random() * this.options.size;
    
    // Apply styles
    star.style.left = x + '%';
    star.style.top = y + '%';
    star.style.width = sizeVariation + 'px';
    star.style.height = sizeVariation + 'px';
    star.style.backgroundColor = this.options.color;
    star.style.position = 'absolute';
    star.style.borderRadius = '50%';
    
    // Add animation if twinkle is enabled
    if (this.options.twinkle) {
      const duration = 3 + Math.random() * 4;
      star.style.animation = `star-field-twinkle ${duration}s infinite`;
    }
    
    this.container.appendChild(star);
    return star;
  }
}

// Add keyframe animation to the document
if (!document.getElementById('star-field-style')) {
  const styleSheet = document.createElement('style');
  styleSheet.id = 'star-field-style';
  styleSheet.textContent = `
    @keyframes star-field-twinkle {
      0%, 100% { opacity: 0.3; }
      50% { opacity: 1; }
    }
  `;
  document.head.appendChild(styleSheet);
}

// Initialize on document ready
document.addEventListener('DOMContentLoaded', function() {
  const containers = document.querySelectorAll('.neogaiam-star-field');
  containers.forEach(container => {
    new StarField('#' + container.id);
  });
});
