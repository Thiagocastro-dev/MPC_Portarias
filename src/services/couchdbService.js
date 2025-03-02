import axios from 'axios';
import { COUCHDB_CONFIG, COUCHDB_HEADERS } from '../config/couchdb';

const couchdbClient = axios.create({
  baseURL: COUCHDB_CONFIG.url,
  headers: COUCHDB_HEADERS
});

export const searchPortarias = async (query, page = 1, limit = 10, tags = []) => {
  try {
    const skip = (page - 1) * limit;
    let selector = {};
    
    if (query || tags.length > 0) {
      selector = {
        $and: []
      };
      
      if (query) {
        selector.$and.push({
          content: {
            $regex: `(?i)${query}`
          }
        });
      }
      
      if (tags.length > 0) {
        selector.$and.push({
          tags: {
            $in: tags
          }
        });
      }
    }

    const response = await couchdbClient.post(`/${COUCHDB_CONFIG.database}/_find`, {
      selector,
      limit,
      skip,
      fields: ['_id', 'content', 'tags']
    });
    
    // Get total count for pagination
    const totalResponse = await couchdbClient.post(`/${COUCHDB_CONFIG.database}/_find`, {
      selector,
      fields: ['_id']
    });
    
    return {
      docs: response.data.docs,
      total: totalResponse.data.docs.length
    };
  } catch (error) {
    if (error.response) {
      throw new Error(`Erro do servidor: ${error.response.status}`);
    } else if (error.request) {
      throw new Error('Erro de conexão com o servidor');
    }
    throw new Error('Erro ao buscar portarias');
  }
};

export const getPortaria = async (id) => {
  try {
    const response = await couchdbClient.get(`/${COUCHDB_CONFIG.database}/${id}`);
    return response.data;
  } catch (error) {
    throw new Error('Erro ao buscar portaria');
  }
};

export const getAllTags = async () => {
  try {
    const response = await couchdbClient.post(`/${COUCHDB_CONFIG.database}/_find`, {
      selector: {
        tags: { $exists: true }
      },
      fields: ['tags']
    });
    
    const allTags = response.data.docs
      .flatMap(doc => doc.tags || [])
      .filter((tag, index, self) => self.indexOf(tag) === index)
      .sort();
    
    return allTags;
  } catch (error) {
    throw new Error('Erro ao buscar tags');
  }
};