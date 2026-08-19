/**
 * AURA VOID PRO // MASTER APPLICATION CONTROLLER
 * Handles UI interactions, 360 Spatial stage, Studio EQ, ANC Simulator, Cart logic & Scroll triggers.
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Glowing Smooth Custom Cursor
  initCustomCursor();

  // 2. Interactive Card Spotlight Hover Glows
  initCardSpotlight();

  // 3. Scroll Reveal Animations (Intersection Observer)
  initScrollReveals();

  // 4. Audio Quick Toggle (Navbar & Soundwave)
  initAudioQuickToggle();

  // 5. ANC Simulator (Noise Cancellation Slider & Environment Buttons)
  initANCSimulator();

  // 6. 360 Spatial Audio Soundstage Arena
  initSpatialSoundstage();

  // 7. Studio Equalizer 5-Band Workbench
  initStudioEqualizer();

  // 8. FAQ Accordion
  initFAQ();

  // 9. Pre-Order Slide-in Drawer & Cart Calculation
  initCartDrawer();

  // 10. Mobile Drawer Menu
  initMobileMenu();

  // 11. Newsletter Form
  initNewsletter();
});

/* ================= 1. CUSTOM CURSOR ================= */
function initCustomCursor() {
  const dot = document.getElementById('cursorDot');
  const ring = document.getElementById('cursorRing');
  if (!dot || !ring) return;

  let mouseX = window.innerWidth / 2;
  let mouseY = window.innerHeight / 2;
  let ringX = mouseX;
  let ringY = mouseY;
  let isHovered = false;

  window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    dot.style.transform = `translate3d(${mouseX}px, ${mouseY}px, 0)`;
    
    if (dot.classList.contains('cursor-hidden')) {
      dot.classList.remove('cursor-hidden');
      ring.classList.remove('cursor-hidden');
    }
  });

  document.documentElement.addEventListener('mouseleave', () => {
    dot.classList.add('cursor-hidden');
    ring.classList.add('cursor-hidden');
  });

  document.documentElement.addEventListener('mouseenter', () => {
    dot.classList.remove('cursor-hidden');
    ring.classList.remove('cursor-hidden');
  });

  window.addEventListener('mousedown', () => {
    ring.classList.add('cursor-click');
  });

  window.addEventListener('mouseup', () => {
    ring.classList.remove('cursor-click');
  });

  function renderRing() {
    ringX += (mouseX - ringX) * 0.18;
    ringY += (mouseY - ringY) * 0.18;
    ring.style.transform = `translate3d(${ringX}px, ${ringY}px, 0)`;
    requestAnimationFrame(renderRing);
  }
  renderRing();

  // Interactive element hover detection
  const hoverSelector = 'button, a, input, select, textarea, label, .hotspot-trigger, .color-btn, .eng-card, .edition-card, .review-card, .stat-card, .faq-item, .addon-item, .mode-chip, .env-btn, .spatial-preset-btn, .eq-tab-btn, .v-slider, .custom-slider';

  document.addEventListener('mouseover', (e) => {
    if (e.target.closest(hoverSelector)) {
      ring.classList.add('cursor-hover');
      dot.classList.add('cursor-hover');
    }
  });

  document.addEventListener('mouseout', (e) => {
    if (e.target.closest(hoverSelector)) {
      ring.classList.remove('cursor-hover');
      dot.classList.remove('cursor-hover');
    }
  });
}

/* ================= 2. CARD SPOTLIGHT HOVER EFFECT ================= */
function initCardSpotlight() {
  const cards = document.querySelectorAll('.glass-card, .eng-card, .edition-card, .stat-card, .review-card, .faq-item, .anc-interactive-box, .spatial-interactive-arena, .eq-workbench, .cta-banner');

  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);
    });
  });
}

/* ================= 3. SCROLL REVEALS ================= */
function initScrollReveals() {
  const revealElements = document.querySelectorAll('.reveal-fade, .reveal-scale, .eng-card, .edition-card, .review-card, .stat-card');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  revealElements.forEach(el => {
    el.classList.add('reveal-fade');
    observer.observe(el);
  });
}

/* ================= 4. AUDIO QUICK TOGGLE & TEST TRIGGERS ================= */
function initAudioQuickToggle() {
  const navBtn = document.getElementById('quickAudioToggle');
  const heroBtn = document.getElementById('heroAudioTestBtn');
  const ancBtn = document.getElementById('ancAudioToggleBtn');

  const navLabel = document.getElementById('navAudioLabel');
  const heroText = document.getElementById('heroAudioText');
  const ancText = document.getElementById('ancAudioToggleText');

  function syncAudioUI(isPlaying) {
    if (navBtn) {
      if (isPlaying) navBtn.classList.add('playing');
      else navBtn.classList.remove('playing');
    }

    if (heroBtn) {
      if (isPlaying) heroBtn.classList.add('playing');
      else heroBtn.classList.remove('playing');
    }

    if (ancBtn) {
      if (isPlaying) ancBtn.classList.add('playing');
      else ancBtn.classList.remove('playing');
    }

    if (navLabel) {
      navLabel.textContent = isPlaying ? 'Звук: ❚❚ Пауза' : 'Тест звука ▶';
    }

    if (heroText) {
      heroText.textContent = isPlaying ? 'Звук активен ❚❚ (Пауза)' : 'Включить тест звука ▶';
    }

    if (ancText) {
      ancText.textContent = isPlaying ? 'Тест ANC активен ❚❚' : 'Включить тест шума ANC ▶';
    }
  }

  function handleMusicToggle() {
    if (window.auraAudio) {
      const isPlaying = window.auraAudio.toggleSound('music');
      syncAudioUI(isPlaying);
    }
  }

  function handleANCToggle() {
    if (window.auraAudio) {
      const isPlaying = window.auraAudio.toggleSound('anc');
      syncAudioUI(isPlaying);
    }
  }

  if (navBtn) navBtn.addEventListener('click', handleMusicToggle);
  if (heroBtn) heroBtn.addEventListener('click', handleMusicToggle);
  if (ancBtn) ancBtn.addEventListener('click', handleANCToggle);

  window.syncAudioUI = syncAudioUI;
}

/* ================= 5. ANC SIMULATOR ================= */
function initANCSimulator() {
  const slider = document.getElementById('ancRangeSlider');
  const levelText = document.getElementById('ancLevelText');
  const decibelDisplay = document.getElementById('decibelDisplay');
  const modeChips = document.querySelectorAll('.mode-chip');
  const envBtns = document.querySelectorAll('.env-btn');

  const lowBar = document.getElementById('lowFreqBar');
  const midBar = document.getElementById('midFreqBar');
  const highBar = document.getElementById('highFreqBar');

  const lowPct = document.getElementById('lowFreqPct');
  const midPct = document.getElementById('midFreqPct');
  const highPct = document.getElementById('highFreqPct');

  function updateANC(val) {
    const pct = parseInt(val, 10);
    const normalized = pct / 100;
    const dbReduction = (45.2 * normalized).toFixed(1);

    if (pct === 0) {
      levelText.textContent = 'Прозрачный режим (0 dB)';
    } else if (pct === 100) {
      levelText.textContent = `VoidShield ANC 100% (-45.2 dB)`;
    } else {
      levelText.textContent = `Адаптивный ANC ${pct}% (-${dbReduction} dB)`;
    }

    if (decibelDisplay) {
      decibelDisplay.textContent = `-${dbReduction} dB REDUCTION`;
    }

    // Update status bars
    if (lowBar && midBar && highBar) {
      const lowVal = Math.round(normalized * 98);
      const midVal = Math.round(normalized * 92);
      const highVal = Math.round(normalized * 85);

      lowBar.style.width = `${lowVal}%`;
      midBar.style.width = `${midVal}%`;
      highBar.style.width = `${highVal}%`;

      lowPct.textContent = `-${(45 * normalized).toFixed(0)}dB`;
      midPct.textContent = `-${(39 * normalized).toFixed(0)}dB`;
      highPct.textContent = `-${(32 * normalized).toFixed(0)}dB`;
    }

    // Sync with Visualizer & Audio Engine in ANC mode
    if (window.ancVis) window.ancVis.setANC(normalized);
    if (window.auraAudio) {
      window.auraAudio.ensurePlaying('anc');
      window.auraAudio.setANCLevel(normalized);
      if (window.syncAudioUI) window.syncAudioUI(true);
    }

    // Sync mode chips
    modeChips.forEach(chip => {
      const chipVal = parseInt(chip.dataset.val, 10);
      if (chipVal === pct) chip.classList.add('active');
      else chip.classList.remove('active');
    });
  }

  if (slider) {
    slider.addEventListener('input', (e) => {
      updateANC(e.target.value);
    });
  }

  modeChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const val = chip.dataset.val;
      if (slider) slider.value = val;
      updateANC(val);
    });
  });

  envBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      envBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const env = btn.dataset.env;
      if (window.ancVis) window.ancVis.setEnv(env);
      if (window.auraAudio) {
        window.auraAudio.ensurePlaying('anc');
        window.auraAudio.setEnv(env);
        if (window.syncAudioUI) window.syncAudioUI(true);
      }
    });
  });
}

/* ================= 6. 360 SPATIAL AUDIO SOUNDSTAGE ================= */
function initSpatialSoundstage() {
  const radar = document.getElementById('soundstageRadar');
  const emitter = document.getElementById('soundEmitter');
  const azimuthDisplay = document.getElementById('spatialAzimuth');
  const distanceDisplay = document.getElementById('spatialDistance');
  const autoRotateBtn = document.getElementById('autoRotateSpatialBtn');
  const presetBtns = document.querySelectorAll('.spatial-preset-btn');

  if (!radar || !emitter) return;

  let isDragging = false;
  let autoRotate = false;
  let autoAngle = 45;

  function updatePosition(clientX, clientY) {
    const rect = radar.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    let dx = clientX - centerX;
    let dy = clientY - centerY;
    const maxRadius = rect.width / 2 - 25;

    const distance = Math.min(Math.sqrt(dx * dx + dy * dy), maxRadius);
    const angleRad = Math.atan2(dy, dx);

    const emitterX = rect.width / 2 + Math.cos(angleRad) * distance;
    const emitterY = rect.height / 2 + Math.sin(angleRad) * distance;

    emitter.style.left = `${emitterX}px`;
    emitter.style.top = `${emitterY}px`;

    // Calculate Azimuth Angle in Degrees (0° top / Front)
    let degrees = Math.round((angleRad * (180 / Math.PI)) + 90);
    if (degrees < 0) degrees += 360;

    let dirLabel = 'Спереди';
    if (degrees >= 30 && degrees < 150) dirLabel = 'Справа';
    else if (degrees >= 150 && degrees < 210) dirLabel = 'Сзади';
    else if (degrees >= 210 && degrees < 330) dirLabel = 'Слева';

    if (azimuthDisplay) {
      azimuthDisplay.textContent = `${degrees}° (${dirLabel})`;
    }

    if (distanceDisplay) {
      const meters = ((distance / maxRadius) * 2.5 + 0.5).toFixed(1);
      distanceDisplay.textContent = `${meters} м`;
    }

    // Audio stereo pan sync
    if (window.auraAudio) {
      window.auraAudio.ensurePlaying('music');
      const pan = (dx / maxRadius);
      window.auraAudio.setPanning(pan);
      if (window.syncAudioUI) window.syncAudioUI(true);
    }
  }

  // Mouse Drag Events
  emitter.addEventListener('mousedown', (e) => {
    isDragging = true;
    autoRotate = false;
    if (autoRotateBtn) autoRotateBtn.classList.remove('btn-primary');
    e.preventDefault();
  });

  window.addEventListener('mousemove', (e) => {
    if (isDragging) {
      updatePosition(e.clientX, e.clientY);
    }
  });

  window.addEventListener('mouseup', () => {
    isDragging = false;
  });

  // Touch Drag Events
  emitter.addEventListener('touchstart', () => {
    isDragging = true;
    autoRotate = false;
  }, { passive: true });

  window.addEventListener('touchmove', (e) => {
    if (isDragging && e.touches.length > 0) {
      updatePosition(e.touches[0].clientX, e.touches[0].clientY);
    }
  }, { passive: true });

  window.addEventListener('touchend', () => {
    isDragging = false;
  });

  // Auto-rotate mode
  if (autoRotateBtn) {
    autoRotateBtn.addEventListener('click', () => {
      autoRotate = !autoRotate;
      if (autoRotate) {
        autoRotateBtn.classList.add('btn-primary');
        autoRotateBtn.querySelector('span').textContent = 'Остановить авто-вращение';
        if (window.auraAudio) {
          window.auraAudio.ensurePlaying('music');
          if (window.syncAudioUI) window.syncAudioUI(true);
        }
      } else {
        autoRotateBtn.classList.remove('btn-primary');
        autoRotateBtn.querySelector('span').textContent = 'Запустить авто-вращение звука 360°';
      }
    });
  }

  function loopAutoRotate() {
    if (autoRotate && radar && emitter) {
      autoAngle = (autoAngle + 1.2) % 360;
      const rad = (autoAngle - 90) * (Math.PI / 180);
      const rect = radar.getBoundingClientRect();
      const radius = rect.width * 0.36;

      const emitterX = rect.width / 2 + Math.cos(rad) * radius;
      const emitterY = rect.height / 2 + Math.sin(rad) * radius;

      emitter.style.left = `${emitterX}px`;
      emitter.style.top = `${emitterY}px`;

      if (azimuthDisplay) azimuthDisplay.textContent = `${Math.round(autoAngle)}° (360° Орбита)`;
      if (window.auraAudio) {
        window.auraAudio.setPanning(Math.cos(rad));
      }
    }
    requestAnimationFrame(loopAutoRotate);
  }
  loopAutoRotate();

  // Space Presets
  presetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      presetBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const preset = btn.dataset.preset;
      if (window.auraAudio) {
        window.auraAudio.ensurePlaying('music');
        window.auraAudio.setSpatialPreset(preset);
        if (window.syncAudioUI) window.syncAudioUI(true);
      }
    });
  });
}

/* ================= 7. STUDIO EQUALIZER ================= */
function initStudioEqualizer() {
  const canvas = document.getElementById('eqCurveCanvas');
  const sliders = [
    document.getElementById('eqBand0'),
    document.getElementById('eqBand1'),
    document.getElementById('eqBand2'),
    document.getElementById('eqBand3'),
    document.getElementById('eqBand4')
  ];
  const valDisplays = [
    document.getElementById('gainVal0'),
    document.getElementById('gainVal1'),
    document.getElementById('gainVal2'),
    document.getElementById('gainVal3'),
    document.getElementById('gainVal4')
  ];
  const presetTabs = document.querySelectorAll('.eq-tab-btn');
  const resetBtn = document.getElementById('resetEqBtn');

  const presets = {
    bass: [6, 3.5, -1, 2.5, 5],
    vocal: [-2, 1, 4.5, 3, 1],
    flat: [0, 0, 0, 0, 0],
    synth: [5, 4, 1.5, 4, 6],
    podcast: [-4, 2, 5, 2, -1]
  };

  function drawEQCurve() {
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width = canvas.parentElement.clientWidth;
    const h = canvas.height = canvas.parentElement.clientHeight;

    ctx.clearRect(0, 0, w, h);

    // Draw Grid Lines
    ctx.strokeStyle = 'rgba(168, 85, 247, 0.1)';
    ctx.lineWidth = 1;
    for (let y = 20; y < h; y += 30) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
      ctx.stroke();
    }

    // Zero dB center line
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(0, h / 2);
    ctx.lineTo(w, h / 2);
    ctx.stroke();
    ctx.setLineDash([]);

    // Calculate Points
    const points = [];
    const step = w / 6;

    // Left anchor
    points.push({ x: 0, y: h / 2 });

    sliders.forEach((slider, idx) => {
      if (slider) {
        const val = parseFloat(slider.value);
        const y = h / 2 - (val / 12) * (h * 0.4);
        const x = (idx + 1) * step;
        points.push({ x, y });
      }
    });

    // Right anchor
    points.push({ x: w, y: h / 2 });

    // Draw Smooth Spline / Bezier Curve
    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);

    for (let i = 0; i < points.length - 1; i++) {
      const p0 = points[i];
      const p1 = points[i + 1];
      const cpX = (p0.x + p1.x) / 2;
      ctx.bezierCurveTo(cpX, p0.y, cpX, p1.y, p1.x, p1.y);
    }

    // Fill Gradient under curve
    ctx.lineTo(w, h);
    ctx.lineTo(0, h);
    ctx.closePath();

    const fillGrad = ctx.createLinearGradient(0, 0, 0, h);
    fillGrad.addColorStop(0, 'rgba(168, 85, 247, 0.35)');
    fillGrad.addColorStop(1, 'rgba(14, 9, 28, 0.05)');
    ctx.fillStyle = fillGrad;
    ctx.fill();

    // Draw Stroke Line
    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);
    for (let i = 0; i < points.length - 1; i++) {
      const p0 = points[i];
      const p1 = points[i + 1];
      const cpX = (p0.x + p1.x) / 2;
      ctx.bezierCurveTo(cpX, p0.y, cpX, p1.y, p1.x, p1.y);
    }
    ctx.strokeStyle = '#c084fc';
    ctx.lineWidth = 3;
    ctx.shadowBlur = 12;
    ctx.shadowColor = '#a855f7';
    ctx.stroke();
    ctx.shadowBlur = 0;

    // Draw Point Beads
    points.slice(1, points.length - 1).forEach(pt => {
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#ffffff';
      ctx.shadowBlur = 8;
      ctx.shadowColor = '#c084fc';
      ctx.fill();
      ctx.shadowBlur = 0;
    });
  }

  function applyPreset(presetKey) {
    const vals = presets[presetKey];
    if (!vals) return;
    vals.forEach((v, i) => {
      if (sliders[i]) sliders[i].value = v;
      if (valDisplays[i]) {
        valDisplays[i].textContent = `${v >= 0 ? '+' : ''}${v.toFixed(1)} dB`;
      }
      if (window.auraAudio) {
        window.auraAudio.setEQBand(i, v);
      }
    });
    drawEQCurve();
    if (window.auraAudio) {
      window.auraAudio.ensurePlaying('music');
      window.auraAudio.playUiSound('mode');
      if (window.syncAudioUI) window.syncAudioUI(true);
    }
  }

  sliders.forEach((slider, i) => {
    if (slider) {
      slider.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        if (valDisplays[i]) {
          valDisplays[i].textContent = `${val >= 0 ? '+' : ''}${val.toFixed(1)} dB`;
        }
        drawEQCurve();
        if (window.auraAudio) {
          window.auraAudio.ensurePlaying('music');
          window.auraAudio.setEQBand(i, val);
          if (window.syncAudioUI) window.syncAudioUI(true);
        }
      });
    }
  });

  presetTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      presetTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      applyPreset(tab.dataset.preset);
    });
  });

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      presetTabs.forEach(t => t.classList.remove('active'));
      const flatTab = document.querySelector('[data-preset="flat"]');
      if (flatTab) flatTab.classList.add('active');
      applyPreset('flat');
    });
  }

  window.addEventListener('resize', drawEQCurve);
  drawEQCurve();
}

/* ================= 7. FAQ ACCORDION ================= */
function initFAQ() {
  const items = document.querySelectorAll('.faq-item');
  items.forEach(item => {
    item.addEventListener('click', () => {
      const isActive = item.classList.contains('active');
      items.forEach(i => i.classList.remove('active'));
      if (!isActive) {
        item.classList.add('active');
      }
    });
  });
}

/* ================= 8. CART & PRE-ORDER DRAWER ================= */
function initCartDrawer() {
  const drawer = document.getElementById('cartDrawer');
  const backdrop = document.getElementById('cartBackdrop');
  const openBtns = document.querySelectorAll('.open-cart-btn');
  const closeBtn = document.getElementById('closeCartBtn');
  const submitBtn = document.getElementById('submitOrderBtn');
  const toast = document.getElementById('toastNotif');

  const basePrice = 34990;
  const addonStand = document.getElementById('addonStand');
  const addonCable = document.getElementById('addonCable');
  const subtotalEl = document.getElementById('subtotalPrice');
  const grandTotalEl = document.getElementById('grandTotalPrice');

  function openDrawer() {
    if (drawer && backdrop) {
      drawer.classList.add('open');
      backdrop.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeDrawer() {
    if (drawer && backdrop) {
      drawer.classList.remove('open');
      backdrop.classList.remove('open');
      document.body.style.overflow = '';
    }
  }

  function updatePrice() {
    let total = basePrice;
    if (addonStand && addonStand.checked) total += parseInt(addonStand.dataset.price, 10);
    if (addonCable && addonCable.checked) total += parseInt(addonCable.dataset.price, 10);

    const formatted = `${total.toLocaleString('ru-RU')} ₽`;
    if (subtotalEl) subtotalEl.textContent = formatted;
    if (grandTotalEl) grandTotalEl.textContent = formatted;
  }

  openBtns.forEach(btn => btn.addEventListener('click', openDrawer));
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  if (backdrop) backdrop.addEventListener('click', closeDrawer);

  if (addonStand) addonStand.addEventListener('change', updatePrice);
  if (addonCable) addonCable.addEventListener('change', updatePrice);

  if (submitBtn) {
    submitBtn.addEventListener('click', () => {
      closeDrawer();
      if (toast) {
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 5000);
      }
    });
  }
}

/* ================= 9. MOBILE MENU ================= */
function initMobileMenu() {
  const btn = document.getElementById('mobileMenuBtn');
  const drawer = document.getElementById('mobileDrawer');
  const closeBtn = document.getElementById('closeDrawerBtn');
  const links = document.querySelectorAll('.mobile-nav-link');

  if (btn && drawer) {
    btn.addEventListener('click', () => drawer.classList.add('open'));
  }
  if (closeBtn && drawer) {
    closeBtn.addEventListener('click', () => drawer.classList.remove('open'));
  }
  links.forEach(link => {
    link.addEventListener('click', () => {
      if (drawer) drawer.classList.remove('open');
    });
  });
}

/* ================= 10. NEWSLETTER ================= */
function initNewsletter() {
  const form = document.getElementById('newsletterForm');
  const msg = document.getElementById('newsletterMsg');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (msg) msg.textContent = '✓ Вы успешно подписаны на закрытые релизы AURA!';
      form.reset();
    });
  }
}
