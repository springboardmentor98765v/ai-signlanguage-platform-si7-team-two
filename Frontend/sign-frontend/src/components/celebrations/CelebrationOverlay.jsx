import { useEffect, useRef } from 'react'
import confetti from 'canvas-confetti'
import Mascot from '../mascot/Mascot.jsx'
import './CelebrationOverlay.css'

/**
 * Full-screen celebration overlay.
 *
 * Props:
 *   type      — 'course' | 'badge'
 *   title     — main heading (e.g. "Course Complete!")
 *   subtitle  — secondary line (e.g. "You finished all 26 letters!")
 *   onDismiss — called when the user clicks "Continue" or presses Escape
 *
 * 'course' → bigger celebration: full-screen confetti, large mascot, gradient title
 * 'badge'  → trophy zoom from small to large as focal point, with confetti burst
 *
 * Confetti is skipped when prefers-reduced-motion is set — the overlay
 * still appears in full with text and mascot (just no particle rain).
 * Does NOT block underlying UI updates — dismissing via onDismiss is instant.
 */
export default function CelebrationOverlay({ type = 'badge', title, subtitle, onDismiss }) {
  const canvasRef = useRef(null)
  const confettiRef = useRef(null)

  // Dismiss on Escape
  useEffect(() => {
    function handleKey(e) {
      if (e.key === 'Escape') onDismiss?.()
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [onDismiss])

  // Fire confetti — respects prefers-reduced-motion
  useEffect(() => {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (prefersReducedMotion) return

    const canvas = canvasRef.current
    if (!canvas) return

    confettiRef.current = confetti.create(canvas, { resize: true, useWorker: true })

    const fire = (particleRatio, opts) =>
      confettiRef.current({
        ...opts,
        origin: { y: 0.6 },
        particleCount: Math.floor(250 * particleRatio),
      })

    if (type === 'course') {
      // Sustained confetti shower for course completion
      fire(0.25, { spread: 26, startVelocity: 55, colors: ['#2fd48f', '#f4c452', '#ff7a59', '#9b8cf5'] })
      fire(0.20, { spread: 60, colors: ['#6be8b4', '#ffb199', '#c3b8ff'] })
      fire(0.35, { spread: 100, decay: 0.91, scalar: 0.8, colors: ['#f4c452', '#2fd48f'] })
      fire(0.10, { spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.2 })
      fire(0.10, { spread: 120, startVelocity: 45, colors: ['#ff7a59', '#9b8cf5'] })

      // Second burst after 0.8s for extra impact
      const t = setTimeout(() => {
        if (!confettiRef.current) return
        fire(0.2, { spread: 80, startVelocity: 50, colors: ['#2fd48f', '#f4c452'] })
      }, 800)
      return () => {
        clearTimeout(t)
        confettiRef.current?.reset()
        confettiRef.current = null
      }
    } else {
      // Single big burst for badge
      fire(0.3, { spread: 70, startVelocity: 60, colors: ['#f4c452', '#ff7a59', '#9b8cf5'] })
      fire(0.2, { spread: 90, decay: 0.9, scalar: 0.9, colors: ['#2fd48f', '#f4c452'] })
      return () => {
        confettiRef.current?.reset()
        confettiRef.current = null
      }
    }
  }, [type])

  const isCourse = type === 'course'

  return (
    <div
      className="celebration-overlay"
      role="dialog"
      aria-modal="true"
      aria-labelledby="celebration-title"
      onClick={(e) => { if (e.target === e.currentTarget) onDismiss?.() }}
    >
      {/* Full-viewport confetti canvas — pointer-events: none so it never blocks clicks */}
      <canvas
        ref={canvasRef}
        style={{
          position: 'fixed',
          inset: 0,
          width: '100%',
          height: '100%',
          pointerEvents: 'none',
          zIndex: 1,
        }}
      />

      <div className="celebration-card">
        {/* Icon / Trophy */}
        {isCourse ? (
          <>
            <Mascot state="celebrating" size="lg" aria-hidden={true} />
            <span className="celebration-course-icon" aria-hidden="true">🎓</span>
          </>
        ) : (
          <span className="celebration-trophy" role="img" aria-label="Trophy">🏆</span>
        )}

        {/* Stars */}
        <div className="celebration-stars" aria-hidden="true">
          <span>⭐</span><span>⭐</span><span>⭐</span>
        </div>

        <h2 className="celebration-title" id="celebration-title">
          {title || (isCourse ? '🎉 Course Complete!' : '🏅 Badge Earned!')}
        </h2>

        {subtitle && (
          <p className="celebration-subtitle">{subtitle}</p>
        )}

        <button
          className="celebration-dismiss"
          onClick={onDismiss}
          autoFocus
        >
          Continue →
        </button>
      </div>
    </div>
  )
}
