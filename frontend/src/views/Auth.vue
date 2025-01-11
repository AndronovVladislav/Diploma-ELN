<template>
  <ConfigProvider :theme="{ token: { colorPrimary: '#ff6060' } }"/>

  <Card title="Вход или регистрация" bordered style="width: 400px; margin: 50px auto;">
    <Tabs v-model:activeKey="activeTab">
      <TabPane key="login" tab="Вход">
        <Form layout="vertical" @submit.prevent="handleLogin">
          <FormItem label="Электронная почта">
            <Input :value="loginForm.email" @input="loginForm.email = $event.target.value!" type="email"
                   placeholder="Введите email"/>
          </FormItem>

          <FormItem label="Пароль">
            <InputPassword :value="loginForm.password" @input="loginForm.password = $event.target.value!"
                           placeholder="Введите пароль"/>
          </FormItem>

          <FormItem>
            <Button type="primary" htmlType="submit" block>Войти</Button>
          </FormItem>
        </Form>
      </TabPane>

      <TabPane key="register" tab="Регистрация">
        <Form layout="vertical" @submit.prevent="handleRegister">
          <FormItem label="Электронная почта">
            <Input :value="signupForm.email" @input="signupForm.email = $event.target.value!" type="email"
                   placeholder="Введите email"/>
          </FormItem>

          <FormItem label="Пароль">
            <InputPassword :value="signupForm.password" @input="signupForm.password = $event.target.value!"
                           placeholder="Введите пароль"/>
          </FormItem>

          <FormItem label="Подтвердите пароль">
            <InputPassword :value="signupForm.confirmPassword"
                           @input="signupForm.confirmPassword = $event.target.value!" placeholder="Повторите пароль"/>
          </FormItem>

          <FormItem>
            <Button type="primary" htmlType="submit" block>Зарегистрироваться</Button>
          </FormItem>
        </Form>
      </TabPane>
    </Tabs>
  </Card>
</template>

<script lang="ts" setup>
import {Reactive, reactive, ref} from 'vue'
import {
  Button,
  Card,
  ConfigProvider,
  Form,
  FormItem,
  Input,
  InputPassword,
  message,
  TabPane,
  Tabs
} from 'ant-design-vue'

interface SignupForm {
  email: string,
  password: string,
  confirmPassword: string,
}

interface LoginForm {
  email: string,
  password: string,
}

const activeTab = ref('login')

const loginForm: Reactive<LoginForm> = reactive({
  email: '',
  password: '',
})

const signupForm: Reactive<SignupForm> = reactive({
  email: '',
  password: '',
  confirmPassword: '',
})

function handleLogin(): void {
  if (!(loginForm.email && loginForm.password)) {
    message.error('Пожалуйста, заполните все поля для входа')
    return
  }

  message.success('Вход успешно выполнен!')
  console.log('Login data:', loginForm)
}

function handleRegister(): void {
  if (!(signupForm.email && signupForm.password && signupForm.confirmPassword)) {
    message.error('Пожалуйста, заполните все поля для регистрации')
    console.log(signupForm.email, signupForm.password, signupForm.confirmPassword)
    return
  }

  if (signupForm.password !== signupForm.confirmPassword) {
    message.error('Пароли не совпадают!')
    return
  }

  message.success('Регистрация успешно выполнена!')
  console.log('Register data:', signupForm)
}
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  margin: 0;
}

.ant-card {
  width: 600px;
  margin: 50px auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 16px;
}

.ant-btn {
  transition: background-color 0.3s, border-color 0.3s;
}

.ant-input,
.ant-input-password {
  border-radius: 6px;
}
</style>
