/**
 * AURA VOID PRO // 3D INTERACTIVE CONTROLLER & EDITION PICKER
 * Controls dynamic perspective tilting, realistic lighting highlights, and edition cross-fading.
 */

class Headphone3DController {
  constructor() {
    this.stage = document.getElementById('headphoneStage');
    this.model = document.getElementById('headphone3d');
    this.editionButtons = document.querySelectorAll('.color-btn');
    this.cartThumbImg = document.getElementById('cartThumbImg');
    this.cartVariantText = document.getElementById('cartItemVariant');
    this.ambientRing = document.querySelector('.headphone-ambient-ring');

    this.imgObsidian = document.getElementById('headphoneImgObsidian');
    this.imgCyber = document.getElementById('headphoneImgCyber');
    this.imgTitanium = document.getElementById('headphoneImgTitanium');

    this.currentEdition = 'obsidian';
    this.tiltX = 0;
    this.tiltY = 0;
    this.targetTiltX = 0;
    this.targetTiltY = 0;

    this.initEvents();
    this.animate();
  }

  initEvents() {
    if (!this.stage || !this.model) return;

    // Mouse movement parallax & 3D tilt
    this.stage.addEventListener('mousemove', (e) => {
      const rect = this.stage.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;

      this.targetTiltX = -y * 22; // rotateX
      this.targetTiltY = x * 28;  // rotateY
    });

    this.stage.addEventListener('mouseleave', () => {
      this.targetTiltX = 0;
      this.targetTiltY = 0;
    });

    // Touch support for mobile devices
    this.stage.addEventListener('touchmove', (e) => {
      if (e.touches.length > 0) {
        const touch = e.touches[0];
        const rect = this.stage.getBoundingClientRect();
        const x = (touch.clientX - rect.left) / rect.width - 0.5;
        const y = (touch.clientY - rect.top) / rect.height - 0.5;

        this.targetTiltX = -y * 18;
        this.targetTiltY = x * 22;
      }
    }, { passive: true });

    this.stage.addEventListener('touchend', () => {
      this.targetTiltX = 0;
      this.targetTiltY = 0;
    });

    // Edition Switcher Buttons
    this.editionButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const edition = btn.dataset.edition;
        this.setEdition(edition);

        this.editionButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
      });
    });

    // Select Edition Buttons from Gallery Section
    const galleryEditionBtns = document.querySelectorAll('.select-edition-btn');
    galleryEditionBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const edition = btn.dataset.edition;
        this.setEdition(edition);

        this.editionButtons.forEach(b => {
          if (b.dataset.edition === edition) b.classList.add('active');
          else b.classList.remove('active');
        });

        // Scroll smoothly to hero showcase
        const heroSection = document.getElementById('hero');
        if (heroSection) {
          heroSection.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });
  }

  setEdition(edition) {
    this.currentEdition = edition;

    if (window.auraAudio) {
      window.auraAudio.playUiSound('switch');
    }

    // Reset active images
    if (this.imgObsidian) this.imgObsidian.classList.remove('active');
    if (this.imgCyber) this.imgCyber.classList.remove('active');
    if (this.imgTitanium) this.imgTitanium.classList.remove('active');

    if (edition === 'obsidian') {
      if (this.imgObsidian) this.imgObsidian.classList.add('active');
      if (this.cartThumbImg) this.cartThumbImg.src = 'images/headphone_obsidian.jpg';
      if (this.cartVariantText) this.cartVariantText.textContent = 'Цвет: Obsidian Void (Black/Purple)';
      if (this.ambientRing) {
        this.ambientRing.style.borderColor = 'rgba(168, 85, 247, 0.4)';
        this.ambientRing.style.boxShadow = '0 0 35px rgba(168, 85, 247, 0.4), inset 0 0 35px rgba(168, 85, 247, 0.2)';
      }
    } else if (edition === 'cyber') {
      if (this.imgCyber) this.imgCyber.classList.add('active');
      if (this.cartThumbImg) this.cartThumbImg.src = 'images/headphone_cyber.jpg';
      if (this.cartVariantText) this.cartVariantText.textContent = 'Цвет: Cyber Neon (Charcoal/Magenta)';
      if (this.ambientRing) {
        this.ambientRing.style.borderColor = 'rgba(236, 72, 153, 0.5)';
        this.ambientRing.style.boxShadow = '0 0 35px rgba(236, 72, 153, 0.5), inset 0 0 35px rgba(236, 72, 153, 0.25)';
      }
    } else if (edition === 'titanium') {
      if (this.imgTitanium) this.imgTitanium.classList.add('active');
      if (this.cartThumbImg) this.cartThumbImg.src = 'images/headphone_titanium.jpg';
      if (this.cartVariantText) this.cartVariantText.textContent = 'Цвет: Dark Titanium (Brushed/Amethyst)';
      if (this.ambientRing) {
        this.ambientRing.style.borderColor = 'rgba(203, 213, 225, 0.4)';
        this.ambientRing.style.boxShadow = '0 0 35px rgba(168, 85, 247, 0.3), inset 0 0 35px rgba(203, 213, 225, 0.2)';
      }
    }
  }

  animate() {
    requestAnimationFrame(() => this.animate());

    // Smooth Lerp for 3D rotation
    this.tiltX += (this.targetTiltX - this.tiltX) * 0.09;
    this.tiltY += (this.targetTiltY - this.tiltY) * 0.09;

    if (this.model) {
      this.model.style.transform = `perspective(1000px) rotateX(${this.tiltX.toFixed(2)}deg) rotateY(${this.tiltY.toFixed(2)}deg)`;
    }
  }
}

// Global initialization
document.addEventListener('DOMContentLoaded', () => {
  window.headphone3D = new Headphone3DController();
});
