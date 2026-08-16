import { useEffect, useRef, useState } from 'react'
import { MASCOTS, getActiveMascotId } from '../mascot/MascotPicker.jsx'
import './ChampionsRise.css'

// Order the three columns left-to-right as 2nd, 1st, 3rd (classic podium
// arrangement) but the animation itself is new: each column is a "stem"
// that grows up from the baseline, tallest first for #1, with the number
// counting up once its stem finishes growing. No blocks, no crown art —
// just motion built from the app's own colors.
const COLUMN_ORDER = [2, 1, 3]

function useCountUp(target, start) {
  const [value, setValue] = useState(0)

  useEffect(() => {
    if (!start) return
    let raf
    const duration = 900
    const startTime = performance.now()

    function tick(now) {
      const elapsed = now - startTime
      const progress = Math.min(elapsed / duration, 1)
      // ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3)
      setValue(Math.round(target * eased))
      if (progress < 1) raf = requestAnimationFrame(tick)
    }

    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [start, target])

  return value
}

const CRACKER_COLORS = ['var(--gold)', 'var(--accent)', 'var(--moss-light)', 'var(--violet-light)', 'var(--accent-light)']

function Crackers({ active }) {
  if (!active) return null

  const particles = Array.from({ length: 18 }, (_, i) => {
    const angle = (360 / 18) * i + (i % 2 === 0 ? 4 : -4)
    const distance = 46 + ((i * 13) % 34)
    const color = CRACKER_COLORS[i % CRACKER_COLORS.length]
    const delay = (i % 5) * 30

    return (
      <span
        key={i}
        className="champs-cracker-bit"
        style={{
          '--angle': `${angle}deg`,
          '--dist': `${distance}px`,
          '--bit-color': color,
          animationDelay: `${delay}ms`,
        }}
      />
    )
  })

  return <div className="champs-crackers" aria-hidden="true">{particles}</div>
}

function ChampionColumn({ entry, unit, delayMs, tallest, currentUser }) {
  const [grown, setGrown] = useState(false)
  const timerRef = useRef(null)

  useEffect(() => {
    timerRef.current = setTimeout(() => setGrown(true), delayMs)
    return () => clearTimeout(timerRef.current)
  }, [delayMs])

  const displayScore = useCountUp(Math.round(entry.score), grown)

  // Stem height purely relative to rank, not literal score scale —
  // keeps the layout stable even if scores are close together.
  const stemHeight = entry.rank === 1 ? 132 : entry.rank === 2 ? 100 : 74

  return (
    <div className="champs-col">
      <div className={`champs-avatar-wrap ${grown ? 'is-in' : ''}`}>
        {(() => {
          const isCurrentUser = currentUser && (entry.learner_id === currentUser.id || entry.learner_id === String(currentUser.id))
          let effectiveMascotId = entry.mascot_id
          if (isCurrentUser) {
            effectiveMascotId = currentUser.mascot_id || getActiveMascotId()
          }
          const mascotDef = MASCOTS.find((m) => m.id === effectiveMascotId)
          return (
            <>
        {entry.rank === 1 && grown && (
          <span className="champs-sparkle champs-sparkle-a" aria-hidden="true">✦</span>
        )}
        {entry.rank === 1 && grown && (
          <span className="champs-sparkle champs-sparkle-b" aria-hidden="true">✦</span>
        )}
        <div 
          className={`champs-avatar rank-${entry.rank}`} 
          style={{ '--avatar-bg': mascotDef?.color }}
        >
          {mascotDef ? (
            <span aria-hidden="true" style={{ fontSize: '1.4em' }}>{mascotDef.emoji}</span>
          ) : (
            entry.learner_name.charAt(0).toUpperCase()
          )}
        </div>
        <span className="champs-rank-chip">#{entry.rank}</span>
            </>
          )
        })()}
      </div>

      <p className="champs-name">{entry.learner_name}</p>
      <p className="champs-score">
        {displayScore}
        {unit}
      </p>

      <div
        className={`champs-stem rank-${entry.rank} ${grown ? 'is-grown' : ''}`}
        style={{ '--stem-h': `${stemHeight}px` }}
      />
    </div>
  )
}

export default function ChampionsRise({ entries, unit, currentUser }) {
  const [celebrate, setCelebrate] = useState(false)

  useEffect(() => {
    if (!entries || entries.length < 3) return
    // Fires once rank #1's stem (delayed 480ms, ~700ms grow transition)
    // has settled, so the crackers punctuate the reveal instead of
    // competing with it.
    const timer = setTimeout(() => setCelebrate(true), 1300)
    return () => clearTimeout(timer)
  }, [entries])

  if (!entries || entries.length < 3) return null

  const top3 = [1, 2, 3].map((rank) => entries.find((e) => e.rank === rank)).filter(Boolean)
  if (top3.length < 3) return null

  const byRank = Object.fromEntries(top3.map((e) => [e.rank, e]))

  // Stagger so the crowd rises first and the champion rises last,
  // like a held breath before the reveal.
  const delays = { 3: 0, 2: 220, 1: 480 }

  return (
    <div className="champs-rise-wrap" role="group" aria-label="Top 3 learners this week">
      <div className="champs-baseline" />
      <div className="champs-crackers-anchor">
        <Crackers active={celebrate} />
      </div>
      {COLUMN_ORDER.map((rank) => (
        <ChampionColumn
          key={rank}
          entry={byRank[rank]}
          unit={unit}
          delayMs={delays[rank]}
          tallest={rank === 1}
          currentUser={currentUser}
        />
      ))}
    </div>
  )
}