<template>
    <FloatingConfigurator />
    <div
        class="bg-surface-50 dark:bg-surface-950 flex items-center justify-center min-h-screen min-w-[100vw] overflow-hidden">
        <div class="flex flex-col items-center justify-center">
            <div
                style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full bg-surface-0 dark:bg-surface-900 py-20 px-8 sm:px-20" style="border-radius: 53px">
                    <div class="flex justify-center">
                        <img src="/logo.svg" alt="Logo" height="180" width="180">
                    </div>

                    <div class="text-center">
                        <div class="text-surface-900 dark:text-surface-0 text-3xl font-medium mb-4">
                            Добро пожаловать в AlChem!
                        </div>
                        <span class="text-muted-color font-medium">
                            Войдите или
                            <router-link to="/auth/signup" class="text-primary font-medium hover:underline">зарегистрируйтесь</router-link>, чтобы продолжить
                        </span>
                    </div>

                    <div>
                        <InputGroup class="my-4">
                            <InputGroupAddon>
                                <i class="pi pi-user"></i>
                            </InputGroupAddon>
                            <FloatLabel variant="on">
                                <InputText
                                    id="username"
                                    v-model="username"
                                    class="w-full md:w-[30rem] mb-8"
                                />
                                <label
                                    for="username"
                                    class="block text-surface-900 dark:text-surface-0 text-base font-medium"
                                >
                                    Имя пользователя
                                </label>
                            </FloatLabel>
                        </InputGroup>

                        <InputGroup class="my-4">
                            <InputGroupAddon>
                                <i class="pi pi-lock"></i>
                            </InputGroupAddon>
                            <FloatLabel variant="on">
                                <Password
                                    inputId="password"
                                    v-model="password"
                                    :toggleMask="true"
                                    class="mb-4"
                                    fluid
                                    :feedback="false"
                                >
                                </Password>
                                <label for="password"
                                       class="block text-surface-900 dark:text-surface-0 text-base font-medium">
                                    Пароль
                                </label>
                            </FloatLabel>
                        </InputGroup>

                        <Button label="Войти" class="w-full" @click="signIn"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import FloatingConfigurator from '@/sakai/components/FloatingConfigurator.vue';
import { ref } from 'vue';
import { FloatLabel, InputGroup, InputGroupAddon, InputText } from 'primevue';
import api from '@/api/axios';
import { useCoreStore } from '@/stores/core';
import router from '@/router';

const username = ref('');
const password = ref('');
const coreStore = useCoreStore();

async function signIn() {
    try {
        await api.post('/auth/login', { username: username.value, password: password.value })
            .then(response => {
                coreStore.access_token = response.data.access_token;
                coreStore.refresh_token = response.data.refresh_token;
            });
        await router.push('/');
    } catch (error) {
        console.error(error);
    }
}

</script>

