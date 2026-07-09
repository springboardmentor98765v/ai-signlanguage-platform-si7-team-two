// Placeholder API layer — wired up to real backend endpoints on Day 6.
// Expected fields from Intern 2 (Backend):
//   auth: { token, role }
//   lessons: { title, level, letters }
//   practice: { predicted_sign, confidence }

export async function login(email, password) {
  return { token: 'mock-token', role: 'student' }
}

export async function register(name, email, password) {
  return { token: 'mock-token', role: 'student' }
}
