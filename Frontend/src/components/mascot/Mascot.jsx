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
   Mascot body dispatch — each mascot gets its own distinct artwork
   (ears, body shape, signature features).  The eye / mouth / hand
   state variants above remain mascot-agnostic and render on top.

   The previous implementation drew a single round-head SVG and only
   changed fill colour — so all 5 mascots looked identical apart from
   tint.  Now each mascot has a recognisable silhouette.
   --------------------------------------------------------------- */
function MascotSVG({ state, mascotId }) {
  // Resolve which mascot to render. Fall back to the active one, then
  // the first mascot in the array.
  const id =
    mascotId ||
    (typeof getActiveMascot === 'function' && getActiveMascot().id) ||
    MASCOTS[0].id

  // Per-mascot body. Dispatch by id, not by colour.
  let Body
  switch (id) {
    case 'fox':
      Body = <FoxBody />
      break
    case 'bear':
      Body = <BearBody />
      break
    case 'cat':
      Body = <CatBody />
      break
    case 'robot':
      Body = <RobotBody />
      break
    case 'owl':
    default:
      Body = <OwlBody />
  }

  // Eye expressions per state — shared across mascots.
  const eyes = {
    idle:        <EyesNormal />,
    celebrating: <EyesHappy />,
    encouraging: <EyesNormal />,
    oops:        <EyesSad />,
    dance:       <EyesHappy />,
  }

  // Mouth per state — shared across mascots.
  const mouths = {
    idle:        <MouthSmile />,
    celebrating: <MouthBig />,
    encouraging: <MouthSmile />,
    oops:        <MouthOops />,
    dance:       <MouthBig />,
  }

  // Hand position per state — shared across mascots.
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
      {Body}
      {eyes[state] || <EyesNormal />}
      {mouths[state] || <MouthSmile />}
      {hands[state] || <HandsDown />}
    </svg>
  )
}

/* --- Mascot-specific bodies --- */

function OwlBody() {
  // Wide rounded body, two large concentric eyes (owl signature),
  // small triangular tufts on top, soft chest feathers.
  const c = MASCOTS.find((m) => m.id === 'owl').color
  return (
    <g>
      {/* Body */}
      <ellipse cx="40" cy="48" rx="26" ry="22" fill={c} />
      {/* Head */}
      <circle cx="40" cy="30" r="22" fill={c} />
      {/* Ear tufts */}
      <path d="M22 14 L28 22 L20 22 Z" fill={c} />
      <path d="M58 14 L52 22 L60 22 Z" fill={c} />
      {/* Big owl eye discs */}
      <circle cx="30" cy="30" r="11" fill="white" />
      <circle cx="50" cy="30" r="11" fill="white" />
      {/* Belly feather V */}
      <path d="M28 44 Q40 56 52 44" fill="rgba(255,255,255,0.35)" />
    </g>
  )
}

function FoxBody() {
  // Slim head, tall pointed ears, distinctive white muzzle + face mask,
  // small bushy tail element.
  const c = MASCOTS.find((m) => m.id === 'fox').color
  return (
    <g>
      {/* Body */}
      <ellipse cx="40" cy="50" rx="20" ry="20" fill={c} />
      {/* Tail (peeks from behind) */}
      <path d="M62 56 Q72 50 70 38 Q66 44 64 52 Z" fill={c} />
      <path d="M66 42 Q70 38 69 32" stroke="white" strokeWidth="3" fill="none" strokeLinecap="round" />
      {/* Head */}
      <path d="M18 32 Q22 14 40 12 Q58 14 62 32 Q62 44 40 46 Q18 44 18 32 Z" fill={c} />
      {/* Pointed ears */}
      <path d="M20 22 L24 6 L30 22 Z" fill={c} />
      <path d="M60 22 L56 6 L50 22 Z" fill={c} />
      {/* Inner ear pink */}
      <path d="M23 20 L25 12 L28 20 Z" fill="#ffb6a3" />
      <path d="M57 20 L55 12 L52 20 Z" fill="#ffb6a3" />
      {/* White muzzle + face mask */}
      <path d="M28 34 Q40 50 52 34 Q40 38 28 34 Z" fill="white" />
      <path d="M28 34 L52 34 L52 28 L28 28 Z" fill="rgba(255,255,255,0.25)" />
      {/* Cheeks */}
      <ellipse cx="26" cy="36" rx="3" ry="2" fill="#ffb6a3" opacity="0.7" />
      <ellipse cx="54" cy="36" rx="3" ry="2" fill="#ffb6a3" opacity="0.7" />
    </g>
  )
}

function BearBody() {
  // Round body, round small ears on top, broad head, dark nose dot.
  const c = MASCOTS.find((m) => m.id === 'bear').color
  return (
    <g>
      {/* Body */}
      <ellipse cx="40" cy="50" rx="24" ry="22" fill={c} />
      {/* Head — slightly broader than owl's */}
      <circle cx="40" cy="32" r="22" fill={c} />
      {/* Small round ears */}
      <circle cx="22" cy="14" r="7" fill={c} />
      <circle cx="58" cy="14" r="7" fill={c} />
      {/* Inner ear */}
      <circle cx="22" cy="14" r="3.5" fill="#c9a98a" />
      <circle cx="58" cy="14" r="3.5" fill="#c9a98a" />
      {/* Snout */}
      <ellipse cx="40" cy="40" rx="10" ry="7" fill="#d9c1a3" />
      {/* Nose */}
      <ellipse cx="40" cy="36" rx="3.5" ry="2.5" fill="#3a2a1a" />
    </g>
  )
}

function CatBody() {
  // Sleek head, tall pointed ears with pink inner triangles, whiskers,
  // vertical slit pupils drawn on top of the shared eye variants.
  const c = MASCOTS.find((m) => m.id === 'cat').color
  return (
    <g>
      {/* Body */}
      <ellipse cx="40" cy="50" rx="20" ry="20" fill={c} />
      {/* Tail curl */}
      <path d="M58 60 Q72 64 70 46" stroke={c} strokeWidth="6" fill="none" strokeLinecap="round" />
      {/* Head — slightly narrower */}
      <path d="M22 30 Q22 14 40 12 Q58 14 58 30 Q58 44 40 46 Q22 44 22 30 Z" fill={c} />
      {/* Pointed ears */}
      <path d="M22 18 L18 4 L32 16 Z" fill={c} />
      <path d="M58 18 L62 4 L48 16 Z" fill={c} />
      {/* Inner ear */}
      <path d="M22 16 L20 8 L28 16 Z" fill="#ffb6d5" />
      <path d="M58 16 L60 8 L52 16 Z" fill="#ffb6d5" />
      {/* Muzzle */}
      <ellipse cx="40" cy="40" rx="6" ry="4" fill="white" />
      {/* Nose */}
      <path d="M38 36 L42 36 L40 39 Z" fill="#ff6f9c" />
      {/* Whiskers */}
      <line x1="14" y1="40" x2="28" y2="40" stroke="#222" strokeWidth="1" strokeLinecap="round" />
      <line x1="14" y1="44" x2="28" y2="42" stroke="#222" strokeWidth="1" strokeLinecap="round" />
      <line x1="66" y1="40" x2="52" y2="40" stroke="#222" strokeWidth="1" strokeLinecap="round" />
      <line x1="66" y1="44" x2="52" y2="42" stroke="#222" strokeWidth="1" strokeLinecap="round" />
    </g>
  )
}

function RobotBody() {
  // Square body, antenna with circle bulb, rectangular eyes, bolts on side.
  const c = MASCOTS.find((m) => m.id === 'robot').color
  return (
    <g>
      {/* Antenna */}
      <line x1="40" y1="6" x2="40" y2="14" stroke="#222" strokeWidth="2" strokeLinecap="round" />
      <circle cx="40" cy="6" r="3" fill="#ff5e5e" />
      {/* Head — rounded square */}
      <rect x="14" y="14" width="52" height="34" rx="6" fill={c} />
      {/* Body */}
      <rect x="20" y="46" width="40" height="26" rx="4" fill={c} />
      {/* Body panel line */}
      <line x1="22" y1="56" x2="58" y2="56" stroke="rgba(0,0,0,0.25)" strokeWidth="1" />
      {/* Bolts on side of head */}
      <circle cx="18" cy="22" r="1.5" fill="#222" />
      <circle cx="18" cy="40" r="1.5" fill="#222" />
      <circle cx="62" cy="22" r="1.5" fill="#222" />
      <circle cx="62" cy="40" r="1.5" fill="#222" />
      {/* Bolts on body */}
      <circle cx="24" cy="50" r="1.5" fill="#222" />
      <circle cx="56" cy="50" r="1.5" fill="#222" />
      {/* Eye screen backdrop (the eye variants draw on top) */}
      <rect x="22" y="22" width="36" height="14" rx="3" fill="#0d1b2a" />
    </g>
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
