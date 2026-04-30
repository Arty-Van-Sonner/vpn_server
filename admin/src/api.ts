import axios from "axios";

export type User = {
  id: string;
  email: string;
  role: "admin" | "operator" | "viewer";
  is_active: boolean;
};

export type Node = {
  id: string;
  name: string;
  region: string;
  endpoint: string;
  status: "online" | "degraded" | "offline";
  capacity: number;
  load: number;
};

export type Session = {
  id: string;
  user_id: string;
  node_id: string;
  status: "active" | "ended" | "revoked";
  bytes_up: number;
  bytes_down: number;
};

const client = axios.create({
  baseURL: "http://localhost:8000/api/v1"
});

export const setToken = (token: string) => {
  client.defaults.headers.common.Authorization = `Bearer ${token}`;
};

export const login = async (email: string, password: string) => {
  const { data } = await client.post<{ access_token: string }>("/auth/login", { email, password });
  return data.access_token;
};

export const getUsers = async () => {
  const { data } = await client.get<User[]>("/admin/users");
  return data;
};

export const getNodes = async () => {
  const { data } = await client.get<Node[]>("/admin/nodes");
  return data;
};

export const getSessions = async () => {
  const { data } = await client.get<Session[]>("/admin/sessions");
  return data;
};

