let audioCtx = null;

function getContext() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
  return audioCtx;
}

function playTone(freq, type, duration, vol, delay = 0) {
  try {
    const ctx = getContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    
    osc.type = type;
    osc.frequency.setValueAtTime(freq, ctx.currentTime + delay);
    
    gain.gain.setValueAtTime(vol, ctx.currentTime + delay);
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + delay + duration);
    
    osc.connect(gain);
    gain.connect(ctx.destination);
    
    osc.start(ctx.currentTime + delay);
    osc.stop(ctx.currentTime + delay + duration);
  } catch (e) {
    console.error("Audio playback failed", e);
  }
}

export function playSuccessChime() {
  // A pleasant major arpeggio
  playTone(523.25, 'sine', 0.3, 0.1, 0);      // C5
  playTone(659.25, 'sine', 0.3, 0.1, 0.1);    // E5
  playTone(783.99, 'sine', 0.4, 0.1, 0.2);    // G5
  playTone(1046.50, 'sine', 0.6, 0.1, 0.3);   // C6
}

export function playCelebrationFanfare() {
  // Triumphant fanfare
  playTone(392.00, 'square', 0.2, 0.05, 0);      // G4
  playTone(392.00, 'square', 0.2, 0.05, 0.2);    // G4
  playTone(392.00, 'square', 0.2, 0.05, 0.4);    // G4
  playTone(523.25, 'square', 0.6, 0.05, 0.6);    // C5
  
  playTone(392.00, 'sine', 0.2, 0.1, 0);
  playTone(392.00, 'sine', 0.2, 0.1, 0.2);
  playTone(392.00, 'sine', 0.2, 0.1, 0.4);
  playTone(523.25, 'sine', 0.6, 0.1, 0.6);
}
