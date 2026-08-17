/**
 * MascotPicker — Avatar selection for Profile page
 *
 * Shows 5 mascot characters as clickable tiles. Selection is persisted to
 * localStorage under 'signlearn_mascot' so it survives page refreshes.
 *
 * Mascots:
 *   owl     — wise, scholarly
 *   fox     — quick, clever
 *   bear    — gentle, encouraging
 *   cat     — curious, agile
 *   robot   — tech-forward, precise
 */
import { useState } from 'react'
import './MascotPicker.css'

export const MASCOTS = [
  {
    id: 'owl',
    name: 'Ollie the Owl',
    emoji: '🦉',
    desc: 'Wise guide',
    color: '#8b7355',
  },
  {
    id: 'fox',
    name: 'Fira the Fox',
    emoji: '🦊',
    desc: 'Quick learner',
    color: '#e8762a',
  },
  {
    id: 'bear',
    name: 'Bruno the Bear',
    emoji: '🐻',
    desc: 'Encouraging pal',
    color: '#7a5c3a',
  },
  {
    id: 'cat',
    name: 'Cleo the Cat',
    emoji: '🐱',
    desc: 'Curious explorer',
    color: '#9966cc',
  },
  {
    id: 'robot',
    name: 'Rix the Robot',
    emoji: '🤖',
    desc: 'Precision mode',
    color: '#4a9eba',
  },
]

export const MASCOT_STORAGE_KEY = 'signlearn_mascot'

export function getActiveMascotId() {
  return localStorage.getItem(MASCOT_STORAGE_KEY) || 'owl'
}

export function getActiveMascot() {
  const id = getActiveMascotId()
  return MASCOTS.find((m) => m.id === id) ?? MASCOTS[0]
}

/**
 * MascotPicker component.
 * @param {object} props
 * @param {string} [props.value] - currently selected mascot id (controlled)
 * @param {(id: string) => void} [props.onChange] - called when selection changes
 */
export default function MascotPicker({ value, onChange }) {
  const [selected, setSelected] = useState(value ?? getActiveMascotId())

  function handleSelect(id) {
    setSelected(id)
    localStorage.setItem(MASCOT_STORAGE_KEY, id)
    onChange?.(id)
  }

  return (
    <section className="mascot-picker" aria-labelledby="mascot-picker-title">
      <h3 id="mascot-picker-title" className="mascot-picker__title">
        Choose your companion
      </h3>
      <p className="mascot-picker__subtitle">
        Your mascot cheers you on during practice.
      </p>
      <div className="mascot-picker__grid" role="listbox" aria-label="Mascot selection">
        {MASCOTS.map((mascot) => {
          const isActive = selected === mascot.id
          return (
            <button
              key={mascot.id}
              role="option"
              aria-selected={isActive}
              className={`mascot-tile${isActive ? ' mascot-tile--active' : ''}`}
              onClick={() => handleSelect(mascot.id)}
              style={{ '--mascot-color': mascot.color }}
              title={mascot.name}
            >
              <span className="mascot-tile__emoji" aria-hidden="true">
                {mascot.emoji}
              </span>
              <span className="mascot-tile__name">{mascot.name}</span>
              <span className="mascot-tile__desc">{mascot.desc}</span>
              {isActive && (
                <span className="mascot-tile__check" aria-hidden="true">✓</span>
              )}
            </button>
          )
        })}
      </div>
    </section>
  )
}
