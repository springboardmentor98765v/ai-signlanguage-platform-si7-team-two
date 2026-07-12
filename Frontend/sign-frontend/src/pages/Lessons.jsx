import { useState, useEffect } from 'react'
import { getLessons } from '../services/api.js'
import { lessons as mockLessons } from '../data/mockData.js'

function badgeClass(difficulty) {
  if (difficulty === 'Beginner') return 'badge badge-beginner'
  if (difficulty === 'Intermediate') return 'badge badge-intermediate'
  return 'badge badge-advanced'
}

export default function Lessons() {
  const [lessons, setLessons] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let isMounted = true

    async function fetchLessons() {
      setIsLoading(true)
      setError('')
      try {
        const data = await getLessons()
        if (isMounted) setLessons(data)
      } catch (err) {
        if (isMounted) setError(err.message || 'Could not load lessons.')
      } finally {
        if (isMounted) setIsLoading(false)
      }
    }

    fetchLessons()
    return () => { isMounted = false }
  }, [])

  if (isLoading) {
    return <p className="lessons-status">Loading lessons...</p>
  }

  if (error) {
    return (
      <div>
        <p className="lessons-status error">
          {error} Showing sample lessons instead.
        </p>
        <LessonGrid lessons={mockLessons} />
      </div>
    )
  }

  return <LessonGrid lessons={lessons} />
}

function LessonGrid({ lessons }) {
  return (
    <div className="lesson-grid">
      {lessons.map((lesson) => (
        <div className="lesson-card" key={lesson.id}>
          <div className="lesson-card-header">
            <h3>{lesson.title}</h3>
            <span className={badgeClass(lesson.difficulty)}>{lesson.difficulty}</span>
          </div>
          <p>{lesson.description}</p>
        </div>
      ))}
    </div>
  )
}
