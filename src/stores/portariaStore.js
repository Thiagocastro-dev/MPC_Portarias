import { defineStore } from 'pinia';
import { searchPortarias, getPortaria, getAllTags } from '../services/couchdbService';

export const usePortariaStore = defineStore('portaria', {
  state: () => ({
    portarias: [],
    loading: false,
    error: null,
    currentQuery: '',
    currentPage: 1,
    totalItems: 0,
    itemsPerPage: 10,
    selectedTags: [],
    availableTags: [],
    loadingTags: false
  }),

  actions: {
    async searchPortarias(query, page = 1) {
      if (!query?.trim() && this.selectedTags.length === 0) {
        this.clearSearch();
        return;
      }
      
      this.loading = true;
      this.error = null;
      this.currentQuery = query;
      this.currentPage = page;

      try {
        const { docs, total } = await searchPortarias(
          query,
          page,
          this.itemsPerPage,
          this.selectedTags
        );
        this.portarias = docs;
        this.totalItems = total;
      } catch (error) {
        this.error = error.message || 'Erro desconhecido';
        this.portarias = [];
      } finally {
        this.loading = false;
      }
    },

    async getPortaria(id) {
      try {
        return await getPortaria(id);
      } catch (error) {
        throw new Error('Erro ao buscar portaria');
      }
    },

    async loadTags() {
      this.loadingTags = true;
      try {
        this.availableTags = await getAllTags();
      } catch (error) {
        this.error = error.message;
      } finally {
        this.loadingTags = false;
      }
    },

    toggleTag(tag) {
      const index = this.selectedTags.indexOf(tag);
      if (index === -1) {
        this.selectedTags.push(tag);
      } else {
        this.selectedTags.splice(index, 1);
      }
      this.searchPortarias(this.currentQuery, 1);
    },

    clearSearch() {
      this.portarias = [];
      this.currentQuery = '';
      this.currentPage = 1;
      this.totalItems = 0;
      this.error = null;
      this.loading = false;
      this.selectedTags = [];
    }
  },

  getters: {
    hasResults: (state) => state.portarias.length > 0,
    resultCount: (state) => state.totalItems,
    totalPages: (state) => Math.ceil(state.totalItems / state.itemsPerPage)
  }
});