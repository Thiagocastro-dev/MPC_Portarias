`<template>
  <div class="search-container q-mb-lg">
    <q-input
      v-model="searchQuery"
      filled
      label="Buscar Portarias"
      placeholder="Digite o termo de busca e pressione Enter"
      class="q-mb-md"
      clearable
      :loading="store.loading"
      :error="!!store.error"
      :error-message="store.error"
      @keyup.enter="handleSearch"
      @clear="handleClear"
    >
      <template v-slot:append>
        <q-btn
          round
          dense
          flat
          icon="search"
          @click="handleSearch"
          :disable="!searchQuery?.trim() && store.selectedTags.length === 0"
          :loading="store.loading"
        />
      </template>
    </q-input>

    <div class="tags-container q-mb-md">
      <q-chip
        v-for="tag in store.availableTags"
        :key="tag"
        :selected="store.selectedTags.includes(tag)"
        clickable
        @click="store.toggleTag(tag)"
        :color="store.selectedTags.includes(tag) ? 'primary' : 'grey-3'"
        text-color="store.selectedTags.includes(tag) ? 'white' : 'black'"
      >
        {{ tag }}
      </q-chip>
    </div>
    
    <div v-if="store.hasResults" class="text-caption">
      Encontrados {{ store.resultCount }} resultados para "{{ store.currentQuery }}"
      <template v-if="store.selectedTags.length > 0">
        com as tags: {{ store.selectedTags.join(', ') }}
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { usePortariaStore } from '../stores/portariaStore';

const searchQuery = ref('');
const store = usePortariaStore();

const handleSearch = async () => {
  if (!searchQuery.value?.trim() && store.selectedTags.length === 0) return;
  await store.searchPortarias(searchQuery.value);
};

const handleClear = () => {
  searchQuery.value = '';
  store.clearSearch();
};

onMounted(async () => {
  await store.loadTags();
});
</script>

<style scoped>
.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>`