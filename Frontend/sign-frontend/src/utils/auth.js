const USER_KEY = "signlearn_user";

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

    return user?.role;
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