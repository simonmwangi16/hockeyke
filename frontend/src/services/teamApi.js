import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const getTeamOverview = (teamId) => {
  return api.get(`/teams/${teamId}/overview/`);
};

export const getTeamMatches = (teamId) => {
  return api.get(`/teams/${teamId}/matches/`);
};

export const getTeamStats = (teamId) => {
  return api.get(`/teams/${teamId}/stats/`);
};

export const getTeamTable = (teamId) => {
  return api.get(`/teams/${teamId}/table/`);
};