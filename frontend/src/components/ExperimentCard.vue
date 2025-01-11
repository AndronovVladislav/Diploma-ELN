<template>
  <div class="experiment-card" @click="handleClick">
    <h3>{{ experiment.title }}</h3>
    <p>{{ experiment.description }}</p>
  </div>
</template>

<script setup lang="ts">
import {defineProps, defineEmits} from 'vue'

interface Experiment {
  title: string
  description: string
  key: string
  isLeaf: boolean
}

const props = defineProps<{
  experiment: Experiment
}>()

const emit = defineEmits(['select'])

const handleClick = () => {
  emit('select', props.experiment.key)
}
</script>

<style scoped>
.experiment-card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: box-shadow 0.3s;
}

.experiment-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.experiment-card h3 {
  margin: 0 0 8px;
  color: #ff6060;
}

.experiment-card p {
  margin: 0;
  color: #333;
}
</style>