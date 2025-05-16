/**
 * NEO GAIAM - Metatron Cube
 * 
 * A 3D visualization of the sacred geometry Metatron's Cube
 * with interactive vertices for website navigation.
 */
class MetatronCube {
  constructor(selector, options = {}) {
    this.container = document.querySelector(selector);
    if (!this.container) return;
    
    this.options = {
      size: parseInt(this.container.dataset.size) || 500,
      rotationSpeed: parseFloat(this.container.dataset.rotationSpeed) || 0.005,
      lineColor: this.container.dataset.lineColor || '#6366f1',
      lineOpacity: parseFloat(this.container.dataset.lineOpacity) || 0.6,
      outerCircle: this.container.dataset.outerCircle === 'true',
      woodenStyle: this.container.dataset.woodenStyle === 'true',
      pulseEffect: this.container.dataset.pulseEffect === 'true',
      ...options
    };
    
    // Add classes based on options
    if (this.options.woodenStyle) this.container.classList.add('wooden-metatron-cube');
    if (this.options.pulseEffect) this.container.classList.add('pulse-effect');
    
    // Set container dimensions
    this.container.style.height = this.options.size + 'px';
    this.container.style.width = '100%';
    this.container.style.position = 'relative';
    
    // Initialize
    this.init();
  }
  
  init() {
    // For WordPress, we'll create a simplified 2D version
    // In a production environment, this would use Three.js for a real 3D cube
    
    // Create vertices (in a circle for 2D representation)
    const vertices = [
      { id: 'courses', label: 'Cursos', icon: '📚', color: '#f43f5e', angle: 0 },
      { id: 'services', label: 'Servicios', icon: '🔮', color: '#3b82f6', angle: 45 },
      { id: 'events', label: 'Eventos', icon: '📅', color: '#10b981', angle: 90 },
      { id: 'blog', label: 'Blog', icon: '✍️', color: '#f59e0b', angle: 135 },
      { id: 'about', label: 'Nosotros', icon: '👥', color: '#8b5cf6', angle: 180 },
      { id: 'contact', label: 'Contacto', icon: '📞', color: '#6366f1', angle: 225 },
      { id: 'membership', label: 'Membresía', icon: '⭐', color: '#ec4899', angle: 270 },
      { id: 'home', label: 'Inicio', icon: '🏠', color: '#14b8a6', angle: 315 }
    ];
    
    // Create a circle for the container
    if (this.options.outerCircle) {
      const outerCircle = document.createElement('div');
      outerCircle.className = 'metatron-outer-circle';
      outerCircle.style.width = this.options.size + 'px';
      outerCircle.style.height = this.options.size + 'px';
      outerCircle.style.border = `2px solid ${this.options.lineColor}`;
      outerCircle.style.borderRadius = '50%';
      outerCircle.style.position = 'absolute';
      outerCircle.style.top = '0';
      outerCircle.style.left = '0';
      outerCircle.style.opacity = this.options.lineOpacity;
      this.container.appendChild(outerCircle);
    }
    
    // Create vertices
    vertices.forEach(vertex => {
      const angle = vertex.angle * (Math.PI / 180);
      const radius = this.options.size / 2.5;
      const x = Math.cos(angle) * radius + this.options.size / 2;
      const y = Math.sin(angle) * radius + this.options.size / 2;
      
      const element = document.createElement('div');
      element.className = 'metatron-cube-vertex';
      element.dataset.id = vertex.id;
      element.style.left = (x - 25) + 'px';
      element.style.top = (y - 25) + 'px';
      element.style.backgroundColor = vertex.color;
      element.style.width = '50px';
      element.style.height = '50px';
      element.style.borderRadius = '50%';
      element.style.display = 'flex';
      element.style.alignItems = 'center';
      element.style.justifyContent = 'center';
      element.style.cursor = 'pointer';
      element.style.position = 'absolute';
      element.style.boxShadow = '0 0 15px rgba(255, 255, 255, 0.5)';
      element.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
      
      // Icon and label
      element.innerHTML = `
        <div style="display: flex; flex-direction: column; align-items: center;">
          <div style="font-size: 18px;">${vertex.icon}</div>
          <div style="font-size: 10px; margin-top: 2px;">${vertex.label}</div>
        </div>
      `;
      
      // Hover effects
      element.addEventListener('mouseenter', () => {
        element.style.transform = 'scale(1.2)';
        element.style.boxShadow = '0 0 20px rgba(255, 255, 255, 0.8)';
      });
      
      element.addEventListener('mouseleave', () => {
        element.style.transform = 'scale(1)';
        element.style.boxShadow = '0 0 15px rgba(255, 255, 255, 0.5)';
      });
      
      // Click handler
      element.addEventListener('click', () => {
        console.log('Clicked:', vertex.id);
        // In WordPress, this would navigate to the corresponding page
        // window.location.href = '/' + vertex.id;
      });
      
      this.container.appendChild(element);
    });
    
    // In a real implementation, we would add connecting lines between vertices
    // For simplicity in this WordPress preview version, we're skipping that
  }
  
  // Methods to handle rotation, animation, etc.
  // These would be fully implemented in the Three.js version
}

// Initialize on document ready
document.addEventListener('DOMContentLoaded', function() {
  const containers = document.querySelectorAll('.neogaiam-metatron-cube');
  containers.forEach(container => {
    new MetatronCube('#' + container.id);
  });
});
