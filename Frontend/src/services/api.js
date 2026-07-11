import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export async function register(full_name, email, password) {
  const response = await API.post("/users/register", {
    full_name,
    email,
    password,
  });

  return response.data;
}

export async function login(email, password) {
  const response = await API.post("/users/login", {
    email,
    password,
  });

  return response.data;
}