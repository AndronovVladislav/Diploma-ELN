<template>
  <AConfigProvider :theme="{ token: { colorPrimary: '#ff6060' } }">
    <ALayout id="app">
      <Home/>
    </ALayout>
  </AConfigProvider>
</template>

<script setup lang="ts">
import {ConfigProvider as AConfigProvider} from 'ant-design-vue';

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