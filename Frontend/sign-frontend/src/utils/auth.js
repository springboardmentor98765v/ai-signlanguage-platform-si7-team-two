const USER_KEY = "signlearn_user";

const ROLE_HOME = {
    learner: "/dashboard",
    instructor: "/instructor",
    admin: "/admin",
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
    const role = user?.role || user?.role_id;
    return typeof role === "string" ? role.toLowerCase() : role;
}

export function getRoleHomePath(role) {
    return ROLE_HOME[role] || "/dashboard";
}

export function isAuthenticated() {
    return getUser() !== null;
}

export function clearSession() {
    localStorage.removeItem(USER_KEY);
}