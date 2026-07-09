import { lessons } from '../data/mockData.js'

function badgeClass(difficulty) {
  if (difficulty === 'Beginner') return 'badge badge-beginner'
  if (difficulty === 'Intermediate') return 'badge badge-intermediate'
  return 'badge badge-advanced'
}

export default function Lessons() {
  return (
    <div>
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
    </div>
  )
}
