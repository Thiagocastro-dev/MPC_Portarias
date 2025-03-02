`<template>
  <div>
    <LoadingSpinner v-if="store.loading" />
    <ErrorMessage
      v-else-if="store.error"
      :message="store.error"
    />
    <div v-else>
      <div v-if="store.portarias.length === 0" class="text-center q-pa-md">
        Nenhuma portaria encontrada
      </div>
      <q-list v-else bordered separator>
        <PortariaItem
          v-for="portaria in store.portarias"
          :key="portaria._id"
          :portaria="portaria"
          @view="showPortaria(portaria)"
        />
      </q-list>

      <div class="q-pa-lg flex flex-center">
        <q-pagination
          v-if="store.totalPages > 1"
          v-model="currentPage"
          :max="store.totalPages"
          :max-pages="6"
          boundary-numbers
          direction-links
          @update:model-value="handlePageChange"
        />
      </div>

      <PortariaDialog
        v-model="showDialog"
        :portaria="selectedPortaria"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { usePortariaStore } from '../stores/portariaStore';
import LoadingSpinner from './ui/LoadingSpinner.vue';
import ErrorMessage from './ui/ErrorMessage.vue';
import PortariaItem from './portaria/PortariaItem.vue';
import PortariaDialog from './portaria/PortariaDialog.vue';

const store = usePortariaStore();
const showDialog = ref(false);
const selectedPortaria = ref(null);
const currentPage = computed({
  get: () => store.currentPage,
  set: (value) => store.currentPage = value
});

const showPortaria = (portaria) => {
  selectedPortaria.value = portaria;
  showDialog.value = true;
};

const handlePageChange = async (page) => {
  await store.searchPortarias(store.currentQuery, page);
  window.scrollTo({ top: 0, behavior: 'smooth' });
};
</script>`