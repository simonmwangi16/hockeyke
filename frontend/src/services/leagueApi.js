import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const getLeagueStandings = (params) => {
  return api.get("/stats/standings/", { params });
};

export const getLeagueFixtures = (params) => {
  return api.get("/matches/", { params });
};

export const getLeagueSeasonStats = (params) => {
  return api.get("/stats/season/", { params });
};

export const getHomeMatchFeed = (params) => {
  return api.get("/matches/home-feed/", { params });
};

export const getMatchDetail = (matchId) => {
  return api.get(`/matches/${matchId}/`);
};

export const getMatchForm = (matchId) => {
  return api.get(`/matches/${matchId}/form/`);
};

export const getMatchHeadToHead = (matchId) => {
  return api.get(`/matches/${matchId}/head-to-head/`);
};

export const getMatchTeamStats = (matchId) => {
  return api.get(`/matches/${matchId}/team-stats/`);
};

export const getMatchLeagueTable = (matchId) => {
  return api.get(`/matches/${matchId}/league-table/`);
};
