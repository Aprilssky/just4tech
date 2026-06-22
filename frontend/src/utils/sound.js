// Sound effects utility - generates sounds via Web Audio API (no files needed)
const STORAGE_KEY = 'j4t-sound-enabled'

let audioCtx = null
let _enabled = localStorage.getItem(STORAGE_KEY) !== 'false' // default on

export function isSoundEnabled() {
  return _enabled
}

export function toggleSound() {
  _enabled = !_enabled
  localStorage.setItem(STORAGE_KEY, _enabled ? 'true' : 'false')
  return _enabled
}

function getCtx() {
  if (!audioCtx) {
    try {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)()
    } catch {
      return null
    }
  }
  return audioCtx
}

function playTone(freq, duration, volume) {
  const ctx = getCtx()
  if (!ctx || !_enabled) return
  try {
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.type = 'sine'
    osc.frequency.setValueAtTime(freq, ctx.currentTime)
    gain.gain.setValueAtTime(volume, ctx.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration)
    osc.connect(gain)
    gain.connect(ctx.destination)
    osc.start()
    osc.stop(ctx.currentTime + duration)
  } catch { /* silent fail */ }
}

export function playClick() {
  playTone(880, 0.04, 0.08)
}

export function playNav() {
  playTone(660, 0.06, 0.06)
}
