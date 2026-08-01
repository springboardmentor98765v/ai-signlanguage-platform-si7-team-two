const USER_KEY = "signlearn_user";

// TEMPORARY WORKAROUND: the backend's /auth/login response only returns
// role_id (a UUID), not a readable role name. These UUIDs are specific to
// this database's seed data — if the DB is ever reseeded, this map must be
// updated too. Ideally this goes away once the backend returns a role name
// directly in the login response.
const ROLE_ID_MAP = {
  '6b5dd979-0102-490f-841d-12e07a9d3dd3': 'learner',
  'e9186e06-6d41-4fa0-80b7-9f1ce4a5ad3c': 'instructor',
  'ae0e4eed-7e29-43ad-875d-2a83a1cbfd41': 'admin',
};

export function saveSession(user) {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function getUser() {
    const user = localStorage.getItem(USER_KEY);

    if (!user) return null;

    return JSON.parse(user);
}

export function getUserId() {
    const user = getUser();

    return user?.id;
}

export function getUserRole() {
    const user = getUser();

    if (!user) return null;
    if (user.role) return user.role;
    if (user.role_id && ROLE_ID_MAP[user.role_id]) return ROLE_ID_MAP[user.role_id];

    return user.role_id;
}

export function getRoleHomePath(role) {
    const normalized = (role || "").toLowerCase();

    if (normalized === "instructor") return "/instructor";
    if (normalized === "admin") return "/admin";

    // Default: learner, or any unrecognised/missing role
    return "/dashboard";
}

export function isAuthenticated() {
    return getUser() !== null;
}

export function clearSession() {
    localStorage.removeItem(USER_KEY);
}