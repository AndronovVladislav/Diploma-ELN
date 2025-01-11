<template>
  <ALayout id="app">
    <Home/>
  </ALayout>
</template>

<script setup lang="ts">
import Home from './views/Home.vue';
</script>

<style>
body {
  display: fill;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #d2d2d3;
}
</style>