const COUCHDB_URL = import.meta.env.VITE_COUCHDB_URL || 'http://localhost:5984';

export const COUCHDB_CONFIG = {
  url: COUCHDB_URL,
  database: 'text_mpc',
  username: 'admin',
  password: 'mpc123'
};

export const COUCHDB_HEADERS = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic ' + btoa(`${COUCHDB_CONFIG.username}:${COUCHDB_CONFIG.password}`)
};