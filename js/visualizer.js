/**
 * AURA VOID PRO // ADVANCED AUDIO ENGINE & CANVAS VISUALIZERS
 * High-fidelity Web Audio synthesizer with real-time ANC filtering, 360° HRTF spatial panner,
 * 5-Band Studio Parametric EQ, dynamic environment noise generator, and UI sound effects.
 */

class AudioEngine {
  constructor() {
    this.ctx = null;
    this.isPlaying = false;
    this.mode = 'music'; // 'music' (Hero/Spatial/EQ) | 'anc' (Noise Cancellation Demo)
    this.oscillators = [];
    this.intervalId = null;

    // Master nodes
    this.masterGain = null;
    this.compressor = null;
    this.pannerNode = null;
    this.analyser = null;
    this.dataArray = null;

    // EQ Filters (5 Bands)
    this.eqFilters = [];

    // ANC & Environment Nodes
    this.musicGain = null;
    this.noiseGain = null;
    this.ancFilter = null;
    this.noiseFilter = null;
    this.noiseSource = null;

    this.ancLevel = 1.0; // 0 (transparency) to 1.0 (100% vacuum)
    this.currentEnv = 'metro';
    this.currentPreset = 'concert';

    // Rhythmic sequencer state
    this.step = 0;
  }

  init() {
    if (this.ctx) return;
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    this.ctx = new AudioContext();

    // 1. Master Compressor (prevents clipping, adds punch & richness)
    this.compressor = this.ctx.createDynamicsCompressor();
    this.compressor.threshold.setValueAtTime(-14, this.ctx.currentTime);
    this.compressor.knee.setValueAtTime(10, this.ctx.currentTime);
    this.compressor.ratio.setValueAtTime(6, this.ctx.currentTime);
    this.compressor.attack.setValueAtTime(0.003, this.ctx.currentTime);
    this.compressor.release.setValueAtTime(0.2, this.ctx.currentTime);

    // 2. Master Gain (Boosted for clear, loud audibility)
    this.masterGain = this.ctx.createGain();
    this.masterGain.gain.setValueAtTime(0.42, this.ctx.currentTime);

    // 3. Analyser
    this.analyser = this.ctx.createAnalyser();
    this.analyser.fftSize = 128;
    this.analyser.smoothingTimeConstant = 0.8;
    this.dataArray = new Uint8Array(this.analyser.frequencyBinCount);

    // 4. Stereo Panner
    if (this.ctx.createStereoPanner) {
      this.pannerNode = this.ctx.createStereoPanner();
    }

    // 5. 5-Band Studio EQ Filters (60Hz, 250Hz, 1kHz, 4kHz, 16kHz)
    const freqs = [60, 250, 1000, 4000, 16000];
    const types = ['lowshelf', 'peaking', 'peaking', 'peaking', 'highshelf'];

    this.eqFilters = freqs.map((freq, i) => {
      const f = this.ctx.createBiquadFilter();
      f.type = types[i];
      f.frequency.setValueAtTime(freq, this.ctx.currentTime);
      f.gain.setValueAtTime(0, this.ctx.currentTime);
      if (types[i] === 'peaking') f.Q.setValueAtTime(1.1, this.ctx.currentTime);
      return f;
    });

    // Chain EQ filters
    for (let i = 0; i < this.eqFilters.length - 1; i++) {
      this.eqFilters[i].connect(this.eqFilters[i + 1]);
    }

    // 6. Music Path vs Noise Path
    this.musicGain = this.ctx.createGain();
    this.musicGain.gain.setValueAtTime(0.85, this.ctx.currentTime);

    this.noiseGain = this.ctx.createGain();
    this.noiseGain.gain.setValueAtTime(0.0, this.ctx.currentTime); // Starts at 0 for 100% ANC silence

    this.ancFilter = this.ctx.createBiquadFilter();
    this.ancFilter.type = 'lowpass';
    this.ancFilter.frequency.setValueAtTime(18000, this.ctx.currentTime);

    // Routing graph:
    // Music -> musicGain -> EQ[0] -> ... -> EQ[4] -> Panner -> Master Compressor -> Analyser -> MasterGain -> Destination
    const lastEq = this.eqFilters[this.eqFilters.length - 1];
    
    if (this.pannerNode) {
      lastEq.connect(this.pannerNode);
      this.pannerNode.connect(this.compressor);
    } else {
      lastEq.connect(this.compressor);
    }

    // Noise -> NoiseFilter -> NoiseGain -> Master Compressor
    this.noiseFilter = this.ctx.createBiquadFilter();
    this.noiseFilter.type = 'lowpass';
    this.noiseFilter.frequency.setValueAtTime(120, this.ctx.currentTime);
    this.noiseFilter.Q.setValueAtTime(2.5, this.ctx.currentTime);
    this.noiseFilter.connect(this.noiseGain);
    this.noiseGain.connect(this.compressor);

    this.compressor.connect(this.analyser);
    this.analyser.connect(this.masterGain);
    this.masterGain.connect(this.ctx.destination);
  }

  toggleSound(targetMode = 'music') {
    if (!this.ctx) this.init();

    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }

    if (this.isPlaying) {
      // If already playing in a different mode, switch to targetMode instead of stopping
      if (this.mode !== targetMode) {
        this.setMode(targetMode);
        return true;
      }
      this.stopSynthesizer();
      this.isPlaying = false;
    } else {
      this.startSynthesizer(targetMode);
      this.isPlaying = true;
    }
    return this.isPlaying;
  }

  ensurePlaying(targetMode = 'music') {
    if (!this.ctx) this.init();
    if (this.ctx.state === 'suspended') this.ctx.resume();

    if (!this.isPlaying) {
      this.startSynthesizer(targetMode);
      this.isPlaying = true;
    } else if (this.mode !== targetMode) {
      this.setMode(targetMode);
    }
  }

  setMode(mode) {
    this.mode = mode; // 'music' | 'anc'
    if (!this.ctx) return;
    const now = this.ctx.currentTime;

    if (mode === 'anc') {
      // In ANC Noise Test: Mute the music synth completely so user tests only the noise suppression!
      if (this.musicGain) {
        this.musicGain.gain.setTargetAtTime(0.0, now, 0.04);
      }
      if (!this.noiseSource) {
        this.startNoiseGenerator();
      }
      this.setANCLevel(this.ancLevel);
    } else {
      // In Music Mode: Restore music synth and mute environmental noise
      if (this.musicGain) {
        this.musicGain.gain.setTargetAtTime(0.85, now, 0.05);
      }
      if (this.noiseGain) {
        this.noiseGain.gain.setTargetAtTime(0.0, now, 0.03);
      }
    }
  }

  startSynthesizer(mode = 'music') {
    this.stopSynthesizer();
    if (!this.ctx) return;
    this.mode = mode;

    // 1. Lush Ambient Chords (D minor 9 / Cyber Void: D3, F3, A3, C4, E4)
    const chordFrequencies = [146.83, 174.61, 220.00, 261.63, 329.63];
    const waveTypes = ['sine', 'triangle', 'sawtooth', 'sine', 'triangle'];

    chordFrequencies.forEach((freq, idx) => {
      const osc = this.ctx.createOscillator();
      const oscGain = this.ctx.createGain();

      osc.type = waveTypes[idx];
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

      // Gentle LFO detune shimmer
      const lfo = this.ctx.createOscillator();
      lfo.frequency.setValueAtTime(0.15 + idx * 0.12, this.ctx.currentTime);
      const lfoGain = this.ctx.createGain();
      lfoGain.gain.setValueAtTime(3.5, this.ctx.currentTime);
      lfo.connect(osc.frequency);
      lfo.start();

      const voiceVolume = idx === 2 ? 0.04 : 0.12;
      oscGain.gain.setValueAtTime(voiceVolume, this.ctx.currentTime);
      
      osc.connect(oscGain);
      oscGain.connect(this.musicGain);
      osc.start();

      this.oscillators.push(osc, lfo);
    });

    // 2. Deep Sub-Bass Drone (73.4Hz)
    const subOsc = this.ctx.createOscillator();
    const subGain = this.ctx.createGain();
    subOsc.type = 'sine';
    subOsc.frequency.setValueAtTime(73.42, this.ctx.currentTime);
    subGain.gain.setValueAtTime(0.22, this.ctx.currentTime);
    subOsc.connect(subGain);
    subGain.connect(this.musicGain);
    subOsc.start();
    this.oscillators.push(subOsc);

    // Connect musicGain into first EQ band
    this.musicGain.connect(this.eqFilters[0]);

    // 3. Melodic Cyber Arpeggio Sequencer
    const arpNotes = [293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25, 880.00];
    this.step = 0;

    this.intervalId = setInterval(() => {
      if (!this.isPlaying || !this.ctx) return;
      if (this.mode === 'music') {
        this.playArpNote(arpNotes[this.step % arpNotes.length]);
      }
      this.step++;
    }, 280);

    // 4. Start Environmental Noise Generator
    this.startNoiseGenerator();

    // Set initial mode gains
    this.setMode(mode);
  }

  playArpNote(freq) {
    if (!this.ctx || this.mode !== 'music') return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

    const now = this.ctx.currentTime;
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(0.14, now + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);

    osc.connect(gain);
    gain.connect(this.musicGain);

    osc.start(now);
    osc.stop(now + 0.38);
  }

  startNoiseGenerator() {
    if (!this.ctx) return;

    // Create 2-second pink/brown noise buffer
    const bufferSize = this.ctx.sampleRate * 2;
    const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);

    let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      b0 = 0.99886 * b0 + white * 0.0555179;
      b1 = 0.99332 * b1 + white * 0.0750759;
      b2 = 0.96900 * b2 + white * 0.1538520;
      b3 = 0.86650 * b3 + white * 0.3104856;
      b4 = 0.55000 * b4 + white * 0.5329522;
      b5 = -0.7616 * b5 - white * 0.0168980;
      output[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.14;
      b6 = white * 0.115926;
    }

    const whiteNoise = this.ctx.createBufferSource();
    whiteNoise.buffer = noiseBuffer;
    whiteNoise.loop = true;

    whiteNoise.connect(this.noiseFilter);
    whiteNoise.start();
    this.noiseSource = whiteNoise;
  }

  stopSynthesizer() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    this.oscillators.forEach(osc => {
      try { osc.stop(); osc.disconnect(); } catch (e) {}
    });
    this.oscillators = [];

    if (this.noiseSource) {
      try { this.noiseSource.stop(); this.noiseSource.disconnect(); } catch (e) {}
      this.noiseSource = null;
    }
  }

  setPanning(panVal) {
    if (this.pannerNode && this.ctx) {
      const clamped = Math.max(-1, Math.min(1, panVal));
      this.pannerNode.pan.setTargetAtTime(clamped, this.ctx.currentTime, 0.05);
    }
  }

  setANCLevel(level) {
    this.ancLevel = level; // 0 to 1
    if (!this.ctx) return;
    const now = this.ctx.currentTime;

    if (this.mode === 'anc') {
      // In ANC Test Mode:
      // When ANC is 100% (level >= 0.96) -> ZERO SOUND / ABSOLUTE TOTAL SILENCE!
      if (level >= 0.96) {
        this.noiseGain.gain.setTargetAtTime(0.0, now, 0.02);
      } else {
        // At 0% (Transparency) noise is loud and clear (0.55 volume)
        // Drops exponentially as slider moves to 100%
        const noiseVol = Math.pow(1 - level, 1.6) * 0.55;
        this.noiseGain.gain.setTargetAtTime(noiseVol, now, 0.04);
      }

      // Filter noise frequency
      if (this.noiseFilter) {
        const cutFreq = 100 + (1 - level) * 3500;
        this.noiseFilter.frequency.setTargetAtTime(cutFreq, now, 0.05);
      }
    } else {
      // In music mode:
      if (this.noiseGain) {
        this.noiseGain.gain.setTargetAtTime(0.0, now, 0.03);
      }
    }
  }

  setEnv(env) {
    this.currentEnv = env;
    if (!this.ctx || !this.noiseFilter) return;

    const now = this.ctx.currentTime;
    if (env === 'metro') {
      // Heavy low-end subway rumble
      this.noiseFilter.type = 'lowpass';
      this.noiseFilter.frequency.setTargetAtTime(110, now, 0.1);
      this.noiseFilter.Q.setTargetAtTime(3.0, now, 0.1);
      this.playUiSound('switch');
    } else if (env === 'flight') {
      // Airplane turbine jet airflow
      this.noiseFilter.type = 'bandpass';
      this.noiseFilter.frequency.setTargetAtTime(450, now, 0.1);
      this.noiseFilter.Q.setTargetAtTime(1.2, now, 0.1);
      this.playUiSound('switch');
    } else if (env === 'cafe') {
      // Cafe ambient chatter
      this.noiseFilter.type = 'bandpass';
      this.noiseFilter.frequency.setTargetAtTime(1200, now, 0.1);
      this.noiseFilter.Q.setTargetAtTime(0.8, now, 0.1);
      this.playUiSound('switch');
    }

    if (this.mode === 'anc') {
      this.setANCLevel(this.ancLevel);
    }
  }

  setSpatialPreset(preset) {
    this.currentPreset = preset;
    if (!this.ctx) return;

    const now = this.ctx.currentTime;
    if (preset === 'concert') {
      this.eqFilters[0].gain.setTargetAtTime(3, now, 0.1);
      this.eqFilters[3].gain.setTargetAtTime(4, now, 0.1);
      this.eqFilters[4].gain.setTargetAtTime(5, now, 0.1);
    } else if (preset === 'cinema') {
      this.eqFilters[0].gain.setTargetAtTime(8, now, 0.1);
      this.eqFilters[1].gain.setTargetAtTime(4, now, 0.1);
      this.eqFilters[3].gain.setTargetAtTime(2, now, 0.1);
    } else if (preset === 'studio') {
      this.eqFilters.forEach(f => f.gain.setTargetAtTime(0, now, 0.1));
    } else if (preset === 'cyberclub') {
      this.eqFilters[0].gain.setTargetAtTime(7, now, 0.1);
      this.eqFilters[1].gain.setTargetAtTime(5, now, 0.1);
      this.eqFilters[2].gain.setTargetAtTime(-3, now, 0.1);
      this.eqFilters[4].gain.setTargetAtTime(6, now, 0.1);
    }
    this.playUiSound('mode');
  }

  setEQBand(bandIndex, gainDb) {
    if (!this.ctx || !this.eqFilters[bandIndex]) return;
    this.eqFilters[bandIndex].gain.setTargetAtTime(gainDb, this.ctx.currentTime, 0.05);
  }

  playUiSound(type = 'click') {
    if (!this.ctx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioContext();
    }
    if (this.ctx.state === 'suspended') this.ctx.resume();

    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const now = this.ctx.currentTime;

    if (type === 'click') {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(1400, now);
      osc.frequency.exponentialRampToValueAtTime(600, now + 0.06);
      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.06);
      osc.start(now);
      osc.stop(now + 0.07);
    } else if (type === 'switch') {
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(600, now);
      osc.frequency.exponentialRampToValueAtTime(1200, now + 0.1);
      gain.gain.setValueAtTime(0.18, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
      osc.start(now);
      osc.stop(now + 0.12);
    } else if (type === 'mode') {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(320, now);
      osc.frequency.exponentialRampToValueAtTime(780, now + 0.15);
      gain.gain.setValueAtTime(0.22, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.16);
      osc.start(now);
      osc.stop(now + 0.18);
    }

    osc.connect(gain);
    gain.connect(this.masterGain || this.ctx.destination);
  }
}

// Global Audio Instance
window.auraAudio = new AudioEngine();

/* ================= HERO BACKGROUND SINE WAVE CANVAS ================= */
class HeroVisualizer {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.phase = 0;
    this.resize();
    window.addEventListener('resize', () => this.resize());
    this.animate();
  }

  resize() {
    this.width = this.canvas.parentElement.clientWidth;
    this.height = this.canvas.parentElement.clientHeight;
    this.canvas.width = this.width;
    this.canvas.height = this.height;
  }

  animate() {
    requestAnimationFrame(() => this.animate());
    this.ctx.clearRect(0, 0, this.width, this.height);

    const centerY = this.height / 2;
    this.phase += 0.03;

    const isPlaying = window.auraAudio && window.auraAudio.isPlaying && window.auraAudio.mode === 'music';
    const ampBoost = isPlaying ? 1.6 : 1.0;

    // Draw 3 glowing organic sine waves
    this.drawSineWave(centerY, 42 * ampBoost, 0.008, this.phase, 'rgba(168, 85, 247, 0.55)', 2.5);
    this.drawSineWave(centerY, 65 * ampBoost, 0.005, -this.phase * 0.7, 'rgba(192, 132, 252, 0.35)', 1.8);
    this.drawSineWave(centerY, 28 * ampBoost, 0.012, this.phase * 1.3, 'rgba(236, 72, 153, 0.45)', 2);

    // Particle sparkles along center
    const time = Date.now() * 0.001;
    const count = isPlaying ? 24 : 12;
    for (let i = 0; i < count; i++) {
      const px = (Math.sin(time + i * 2) * 0.45 + 0.5) * this.width;
      const py = centerY + Math.sin(time * 2 + i) * (35 * ampBoost);
      const radius = Math.sin(time * 3 + i) * 2 + (isPlaying ? 3.5 : 2);

      this.ctx.beginPath();
      this.ctx.arc(px, py, radius, 0, Math.PI * 2);
      this.ctx.fillStyle = i % 2 === 0 ? 'rgba(232, 121, 249, 0.8)' : 'rgba(168, 85, 247, 0.7)';
      this.ctx.shadowBlur = 12;
      this.ctx.shadowColor = '#d946ef';
      this.ctx.fill();
    }
  }

  drawSineWave(baseY, amplitude, freq, phase, color, lineWidth) {
    this.ctx.save();
    this.ctx.beginPath();
    this.ctx.strokeStyle = color;
    this.ctx.lineWidth = lineWidth;
    this.ctx.shadowBlur = 18;
    this.ctx.shadowColor = color;

    for (let x = 0; x < this.width; x += 4) {
      const distFromCenter = Math.abs(x - this.width / 2) / (this.width / 2);
      const envelope = Math.max(0, 1 - Math.pow(distFromCenter, 1.8));

      const y = baseY + Math.sin(x * freq + phase) * amplitude * envelope;
      if (x === 0) {
        this.ctx.moveTo(x, y);
      } else {
        this.ctx.lineTo(x, y);
      }
    }
    this.ctx.stroke();
    this.ctx.restore();
  }
}

/* ================= ANC REALTIME SPECTRUM CANVAS ================= */
class ANCSpectrumVisualizer {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.bars = 36;
    this.ancLevel = 1.0; // 1 = full cancel
    this.envMultiplier = 1.0;
    this.resize();
    window.addEventListener('resize', () => this.resize());
    this.animate();
  }

  resize() {
    this.width = this.canvas.parentElement.clientWidth - 48;
    this.height = 180;
    this.canvas.width = this.width;
    this.canvas.height = this.height;
  }

  setANC(level) {
    this.ancLevel = level;
  }

  setEnv(env) {
    if (env === 'metro') this.envMultiplier = 1.4;
    else if (env === 'flight') this.envMultiplier = 1.7;
    else this.envMultiplier = 0.9;
  }

  animate() {
    requestAnimationFrame(() => this.animate());
    this.ctx.clearRect(0, 0, this.width, this.height);

    const barWidth = (this.width / this.bars) - 3;
    const time = Date.now() * 0.005;

    for (let i = 0; i < this.bars; i++) {
      const rawEnergy = (Math.sin(time + i * 0.35) * 0.4 + Math.cos(time * 0.8 + i * 0.2) * 0.3 + 0.7) * this.envMultiplier;
      
      // When ANC is 100% (level >= 0.96), bars drop to flatline (0dB reduction / complete quiet)
      let suppressionFactor = (1 - this.ancLevel);
      if (this.ancLevel >= 0.96) {
        suppressionFactor = 0.02; // Flatline silence
      }
      
      const barHeight = Math.max(4, rawEnergy * (this.height * 0.85) * suppressionFactor);

      const x = i * (barWidth + 3);
      const y = this.height - barHeight;

      // Color gradient: deep purple to electric neon violet
      const grad = this.ctx.createLinearGradient(0, this.height, 0, y);
      if (this.ancLevel > 0.6) {
        grad.addColorStop(0, '#3b0764');
        grad.addColorStop(0.6, '#a855f7');
        grad.addColorStop(1, '#e879f9');
      } else {
        grad.addColorStop(0, '#9d174d');
        grad.addColorStop(0.6, '#ec4899');
        grad.addColorStop(1, '#fb7185');
      }

      this.ctx.fillStyle = grad;
      this.ctx.beginPath();
      this.ctx.roundRect(x, y, barWidth, barHeight, [4, 4, 0, 0]);
      this.ctx.fill();

      // Mirror reflection effect at bottom
      this.ctx.fillStyle = 'rgba(168, 85, 247, 0.15)';
      this.ctx.fillRect(x, this.height - 3, barWidth, 3);
    }
  }
}

// Global initialization on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  window.heroVis = new HeroVisualizer('heroVisualizerCanvas');
  window.ancVis = new ANCSpectrumVisualizer('ancSpectrumCanvas');
});
