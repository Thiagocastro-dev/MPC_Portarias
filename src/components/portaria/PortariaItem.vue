`<template>
  <q-item clickable @click="$emit('view')">
    <q-item-section>
      <q-item-label>{{ formatPortariaId(portaria._id) }}</q-item-label>
      <q-item-label caption lines="2">
        {{ truncateText(portaria.content) }}
      </q-item-label>
      <q-item-label caption>
        <q-chip
          v-for="tag in portaria.tags"
          :key="tag"
          size="sm"
          dense
          color="primary"
          text-color="white"
        >
          {{ tag }}
        </q-chip>
      </q-item-label>
    </q-item-section>
    
    <q-item-section side>
      <q-btn
        flat
        round
        color="primary"
        icon="visibility"
        @click.stop="$emit('view')"
      />
    </q-item-section>
  </q-item>
</template>

<script setup>
import { truncateText, formatPortariaId } from '../../utils/formatters';

defineProps({
  portaria: {
    type: Object,
    required: true
  }
});

defineEmits(['view']);
</script>`