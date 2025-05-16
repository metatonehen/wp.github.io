/**
 * NEO GAIAM - Flower of Life
 * 
 * A sacred geometry visualization of the Flower of Life pattern
 * with animation and customizable properties.
 */
class FlowerOfLife {
  constructor(selector, options = {}) {
    this.container = document.querySelector(selector);
    if (!this.container) return;
    
    this.options = {
      size: parseInt(this.container.dataset.size) || 300,
      opacity: parseFloat(this.container.dataset.opacity) || 0.7,
      animationDuration: parseInt(this.container.dataset.animationDuration) || 60,
      primaryColor: this.container.dataset.primaryColor || '#6366f1',
      secondaryColor: this.container.dataset.secondaryColor || '#8b5cf6',
      ...options
    };
    
    // Set container dimensions
    this.container.style.height = this.options.size + 'px';
    this.container.style.width = this.options.size + 'px';
    this.container.style.position = 'relative';
    
    // Initialize
    this.init();
  }
  
  init() {
    // Center coordinates
    const centerX = this.options.size / 2;
    const centerY = this.options.size / 2;
    
    // Radius for each circle
    const radius = this.options.size / 6;
    
    // Create center circle
    this.createCircle(centerX, centerY, radius, this.options.primaryColor);
    
    // Create first ring of 6 circles
    for (let i = 0; i < 6; i++) {
      const angle = (Math.PI / 3) * i;
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);
      
      this.createCircle(
        x, 
        y, 
        radius, 
        i % 2 === 0 ? this.options.primaryColor : this.options.secondaryColor
      );
    }
    
    // Create second ring of circles for a more complete pattern
    for (let i = 0; i < 12; i++) {
      const angle = (Math.PI / 6) * i;
      const x = centerX + radius * 2 * Math.cos(angle);
      const y = centerY + radius * 2 * Math.sin(angle);
      
      this.createCircle(
        x, 
        y, 
        radius, 
        i % 2 === 0 ? this.options.secondaryColor : this.options.primaryColor
      );
    }
  }
  
  createCircle(x, y, r, color) {
    const circle = document.createElement('div');
    circle.className = 'flower-of-life-circle';
    
    // Apply styles
    circle.style.width = (r * 2) + 'px';
    circle.style.height = (r * 2) + 'px';
    circle.style.left = (x - r) + 'px';
    circle.style.top = (y - r) + 'px';
    circle.style.borderColor = color;
    circle.style.position = 'absolute';
    circle.style.borderRadius = '50%';
    circle.style.borderWidth = '1px';
    circle.style.borderStyle = 'solid';
    circle.style.opacity = this.options.opacity;
    
    // Add animation with random delay for subtle effect
    const delay = Math.random() * this.options.animationDuration;
    circle.style.animation = `flower-of-life-pulse ${this.options.animationDuration}s infinite ${delay}s`;
    
    this.container.appendChild(circle);
    return circle;
  }
}

// Add keyframe animation to the document
if (!document.getElementById('flower-of-life-style')) {
  const styleSheet = document.createElement('style');
  styleSheet.id = 'flower-of-life-style';
  styleSheet.textContent = `
    @keyframes flower-of-life-pulse {
      0%, 100% { transform: scale(1); opacity: var(--opacity, 0.7); }
      50% { transform: scale(1.05); opacity: calc(var(--opacity, 0.7) + 0.2); }
    }
  `;
  document.head.appendChild(styleSheet);
}

// Initialize on document ready
document.addEventListener('DOMContentLoaded', function() {
  const containers = document.querySelectorAll('.neogaiam-flower-of-life');
  containers.forEach(container => {
    new FlowerOfLife('#' + container.id);
  });
});
