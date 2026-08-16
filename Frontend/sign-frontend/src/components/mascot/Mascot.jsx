import './Mascot.css'
import { getActiveMascot, MASCOTS } from './MascotPicker.jsx'
/**
 * Reusable animated mascot — a friendly round character that reacts to
 * game events across the whole app.
 *
 * Props:
 *   state  — 'idle' | 'celebrating' | 'encouraging' | 'oops' | 'dance'
 *   size   — 'sm' | 'md' | 'lg'  (default 'md')
 *   label  — optional speech-bubble text (e.g. "You're #1!")
 *   aria-hidden — pass true when the mascot is purely decorative
 *
 * Animations:
 *   idle        → gentle floating bob (loop)
 *   celebrating → energetic jump + spin (loop)
 *   encouraging → friendly left-right nod (loop)
 *   oops        → side-shake (plays once, then stays static)
 *   dance       → persistent wiggle (loop, for rank-1)
 *
 * All animations are suppressed under prefers-reduced-motion — the character
 * still renders in its static pose so the page remains visually consistent.
 */
export default function Mascot({
  state = 'idle',
  size = 'md',
  label,
  mascotId,
  'aria-hidden': ariaHidden,
}) {
  const isCelebrating = state === 'celebrating' || state === 'dance'

  return (
    <div
      className={`mascot-wrap mascot-${size} mascot-${state}`}
      role={ariaHidden ? undefined : 'img'}
      aria-label={ariaHidden ? undefined : `Mascot: ${state}`}
      aria-hidden={ariaHidden ? true : undefined}
    >
      {/* Stars — only shown when celebrating/dancing */}
      {isCelebrating && (
        <>
          <span className="mascot-star" aria-hidden="true">✦</span>
          <span className="mascot-star" aria-hidden="true">✦</span>
          <span className="mascot-star" aria-hidden="true">✦</span>
        </>
      )}

      {/* Speech bubble */}
      {label && <div className="mascot-bubble" aria-live="polite">{label}</div>}

      {/* The character SVG — all animation is applied via CSS to .mascot-body */}
      <div className="mascot-body">
        <MascotSVG state={state} mascotId={mascotId} />
      </div>
    </div>
  )
}

/* ---------------------------------------------------------------
   Self-authored SVG mascot — a simple, friendly round character
   with expressive eyes and hands.  All colours use CSS variables
   so the mascot automatically matches the app theme.
   --------------------------------------------------------------- */
function MascotSVG({ state, mascotId }) {
  // Eye expressions per state
  const eyes = {
    idle:        <EyesNormal />,
    celebrating: <EyesHappy />,
    encouraging: <EyesNormal />,
    oops:        <EyesSad />,
    dance:       <EyesHappy />,
  }

  // Mouth per state
  const mouths = {
    idle:        <MouthSmile />,
    celebrating: <MouthBig />,
    encouraging: <MouthSmile />,
    oops:        <MouthOops />,
    dance:       <MouthBig />,
  }

  // Hand position per state (arms up/down/wave)
  const hands = {
    idle:        <HandsDown />,
    celebrating: <HandsUp />,
    encouraging: <HandsWave />,
    oops:        <HandsDown />,
    dance:       <HandsUp />,
  }

  return (
    <svg
      viewBox="0 0 80 80"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      {/* Body */}
      <circle cx="40" cy="44" r="22" fill={mascotId ? (MASCOTS.find((m) => m.id === mascotId) || MASCOTS[0]).color : getActiveMascot().color} />

      {/* Head */}
      <circle cx="40" cy="30" r="20" fill={mascotId ? (MASCOTS.find((m) => m.id === mascotId) || MASCOTS[0]).color : getActiveMascot().color} />
      <path d="M24 16 L28 22 L20 28 Z" fill={mascotId ? (MASCOTS.find((m) => m.id === mascotId) || MASCOTS[0]).color : getActiveMascot().color} />
      <path d="M56 16 L52 22 L60 28 Z" fill={mascotId ? (MASCOTS.find((m) => m.id === mascotId) || MASCOTS[0]).color : getActiveMascot().color} />

      {/* Cheeks */}
      <ellipse cx="26" cy="35" rx="5" ry="3.5" fill="var(--accent, #ff7a59)" opacity="0.5" />
      <ellipse cx="54" cy="35" rx="5" ry="3.5" fill="var(--accent, #ff7a59)" opacity="0.5" />

      {/* Eyes */}
      {eyes[state] || <EyesNormal />}

      {/* Mouth */}
      {mouths[state] || <MouthSmile />}

      {/* Hands/Arms */}
      {hands[state] || <HandsDown />}

      {/* Ears / bumps */}
      <circle cx="20" cy="26" r="5" fill="var(--moss, #2fd48f)" />
      <circle cx="60" cy="26" r="5" fill="var(--moss, #2fd48f)" />
    </svg>
  )
}

/* --- Eye variants --- */
function EyesNormal() {
  return (
    <>
      <ellipse cx="32" cy="28" rx="3.5" ry="4" fill="#11101f" />
      <ellipse cx="48" cy="28" rx="3.5" ry="4" fill="#11101f" />
      {/* shine */}
      <circle cx="33.5" cy="26.5" r="1.2" fill="white" />
      <circle cx="49.5" cy="26.5" r="1.2" fill="white" />
    </>
  )
}

function EyesHappy() {
  return (
    <>
      {/* Squinting happy arcs */}
      <path d="M29 29 Q32 24 35 29" stroke="#11101f" strokeWidth="2.2" strokeLinecap="round" fill="none" />
      <path d="M45 29 Q48 24 51 29" stroke="#11101f" strokeWidth="2.2" strokeLinecap="round" fill="none" />
    </>
  )
}

function EyesSad() {
  return (
    <>
      {/* Worried brows + big eyes */}
      <ellipse cx="32" cy="29" rx="3" ry="3.5" fill="#11101f" />
      <ellipse cx="48" cy="29" rx="3" ry="3.5" fill="#11101f" />
      <circle cx="33" cy="27.5" r="1" fill="white" />
      <circle cx="49" cy="27.5" r="1" fill="white" />
      <path d="M29 23 Q32 21 35 23" stroke="#11101f" strokeWidth="1.8" strokeLinecap="round" fill="none" />
      <path d="M45 23 Q48 21 51 23" stroke="#11101f" strokeWidth="1.8" strokeLinecap="round" fill="none" />
    </>
  )
}

/* --- Mouth variants --- */
function MouthSmile() {
  return <path d="M33 37 Q40 43 47 37" stroke="#11101f" strokeWidth="2.2" strokeLinecap="round" fill="none" />
}

function MouthBig() {
  return (
    <>
      <path d="M30 36 Q40 46 50 36" stroke="#11101f" strokeWidth="2.5" strokeLinecap="round" fill="none" />
      <path d="M31 37 Q40 46 49 37" fill="white" opacity="0.6" />
    </>
  )
}

function MouthOops() {
  return <ellipse cx="40" cy="39" rx="5" ry="4" fill="#11101f" opacity="0.8" />
}

/* --- Hand/Arm variants --- */
function HandsDown() {
  return (
    <>
      {/* Left arm */}
      <line x1="20" y1="44" x2="14" y2="56" stroke="var(--moss, #2fd48f)" strokeWidth="5" strokeLinecap="round" />
      <circle cx="14" cy="58" r="4" fill="var(--moss, #2fd48f)" />
      {/* Right arm */}
      <line x1="60" y1="44" x2="66" y2="56" stroke="var(--moss, #2fd48f)" strokeWidth="5" strokeLinecap="round" />
      <circle cx="66" cy="58" r="4" fill="var(--moss, #2fd48f)" />
    </>
  )
}

function HandsUp() {
  return (
    <>
      {/* Left arm raised */}
      <line x1="20" y1="42" x2="10" y2="30" stroke="var(--moss, #2fd48f)" strokeWidth="5" strokeLinecap="round" />
      <circle cx="8" cy="28" r="5" fill="var(--gold, #f4c452)" />
      {/* Right arm raised */}
      <line x1="60" y1="42" x2="70" y2="30" stroke="var(--moss, #2fd48f)" strokeWidth="5" strokeLinecap="round" />
      <circle cx="72" cy="28" r="5" fill="var(--gold, #f4c452)" />
    </>
  )
}

function HandsWave() {
  return (
    <>
      {/* Left arm down */}
      <line x1="20" y1="44" x2="13" y2="56" stroke="var(--moss, #2fd48f)" strokeWidth="5" strokeLinecap="round" />
      <circle cx="12" cy="58" r="4" fill="var(--moss, #2fd48f)" />
      {/* Right arm waving */}
      <line x1="60" y1="42" x2="70" y2="33" stroke="var(--moss, #2fd48f)" strokeWidth="5" strokeLinecap="round" />
      <circle cx="72" cy="31" r="5" fill="var(--moss-light, #6be8b4)" />
    </>
  )
}
