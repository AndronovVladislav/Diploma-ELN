<template>
  <div class="experiment-list">
    <ExperimentCard
        v-for="experiment in props.experiments"
        :key="experiment.key"
        :experiment="experiment"
        @select="onSelect"
    />
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';
import ExperimentCard from './ExperimentCard.vue';

interface Experiment {
  title: string;
  description: string;
  key: string;
  isLeaf: boolean;
}

const props = defineProps<{
  experiments: Experiment[];
}>();

const emit = defineEmits(['select'])

const onSelect = (key: string) => {
  emit('select', key);
};
</script>

<style scoped>
.experiment-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}
</style>