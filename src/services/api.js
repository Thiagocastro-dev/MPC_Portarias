import axios from 'axios';
import { COUCHDB_CONFIG } from '../config/couchdb';

const api = axios.create({
  baseURL: COUCHDB_CONFIG.url,
  auth: {
    username: COUCHDB_CONFIG.username,
    password: COUCHDB_CONFIG.password
  }
});

export const searchPortarias = async (query) => {
  try {
    const response = await api.post(`/${COUCHDB_CONFIG.database}/_find`, {
      selector: {
        content: {
          $regex: `(?i)${query}`
        }
      },
      limit: 50,
      fields: ['_id', 'content']
    });
    
    // Ensure we only return serializable data
    return response.data.docs.map(doc => ({
      _id: doc._id,
      content: doc.content
    }));
  } catch (error) {
    // Handle specific error types
    if (error.response) {
      throw new Error(`Erro do servidor: ${error.response.status}`);
    } else if (error.request) {
      throw new Error('Erro de conexão com o servidor');
    } else {
      throw new Error('Erro ao buscar portarias');
    }
  }
};