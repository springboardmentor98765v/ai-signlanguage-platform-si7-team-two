const USER_KEY = "signlearn_user";
const TOKEN_KEY = "signlearn_token";


export function saveSession(user, token) {
    localStorage.setItem(
        USER_KEY,
        JSON.stringify(user)
    );

    if (token) {
        localStorage.setItem(
            TOKEN_KEY,
            token
        );
    }
}


export function getUser() {
    const user = localStorage.getItem(USER_KEY);

    if (!user) {
        return null;
    }

    try {
        return JSON.parse(user);
    } catch {
        return null;
    }
}


export function getToken() {
    return localStorage.getItem(TOKEN_KEY);
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

    if (normalized === "instructor") {
        return "/instructor";
    }

    if (normalized === "admin") {
        return "/admin";
    }

    if (normalized === "trainer") {
        return "/trainer";
    }

    return "/dashboard";
}


export function isAuthenticated() {
    return Boolean(
        getUser() &&
        getToken()
    );
}


export function clearSession() {
    localStorage.removeItem(USER_KEY);
    localStorage.removeItem(TOKEN_KEY);
}