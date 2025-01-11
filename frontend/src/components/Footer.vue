<template>
  <ConfigProvider :theme="{ token: { colorPrimary: '#ff6060' } }"/>
  <ALayoutFooter class="footer">
    <div class="footer-container">
      <div class="footer-right">
        <h3>AlChem</h3>
        <p>© 2025 Created by v-andronov</p>
      </div>
    </div>
  </ALayoutFooter>
</template>

<script setup lang="ts">
import {ConfigProvider, LayoutFooter as ALayoutFooter} from 'ant-design-vue';
</script>

<style scoped>
.footer {
  background-color: #f9f9f9;
  padding: 12px 48px;
  text-align: right;
  display: flex;
  justify-content: center;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
  box-shadow: 0 -4px 8px rgba(0, 0, 0, 0.1);
}

.footer-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  max-width: 1200px;
  width: 100%;
}

.footer-right h3 {
  margin-bottom: 8px;
  color: #ff6060;
}


@media (max-width: 768px) {
  .footer-container {
    flex-direction: column;
    align-items: center;
  }
}
</style>