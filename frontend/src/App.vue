<template>
  <Layout id="app">
    <SignUpForm />
  </Layout>
</template>

<script>
import SignUpForm from './components/SignUp/SignUpForm.vue';
import { Layout } from 'ant-design-vue';

export default {
  components: {
    SignUpForm
  }
};
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