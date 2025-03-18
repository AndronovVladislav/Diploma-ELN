<template>
    <FloatingConfigurator />
    <div
        class="bg-surface-50 dark:bg-surface-950 flex items-center justify-center min-h-screen min-w-[100vw] overflow-hidden">
        <div class="flex flex-col items-center justify-center">
            <div
                style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full bg-surface-0 dark:bg-surface-900 py-20 px-8 sm:px-20" style="border-radius: 53px">
                    <div class="flex justify-center">
                        <img alt="Logo" height="180" src="/logo.svg" width="180">
                    </div>

                    <div class="text-center">
                        <div class="text-surface-900 dark:text-surface-0 text-3xl font-medium mb-4">
                            Добро пожаловать в AlChem!
                        </div>
                        <span class="text-muted-color font-medium">Зарегистрируйтесь, чтобы продолжить</span>
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
                                    class="block text-surface-900 dark:text-surface-0 text-base font-medium"
                                    for="username"
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
                                    v-model="password"
                                    :feedback="false"
                                    :toggleMask="true"
                                    class="mb-4"
                                    fluid
                                    inputId="password"
                                >
                                </Password>
                                <label class="block text-surface-900 dark:text-surface-0 text-base font-medium"
                                       for="password">
                                    Пароль
                                </label>
                            </FloatLabel>
                        </InputGroup>
                        <Button class="w-full" label="Зарегистрироваться" @click="signUp"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import FloatingConfigurator from '@/components/FloatingConfigurator.vue';
import { ref } from 'vue';
import { FloatLabel, InputGroup, InputGroupAddon, InputText } from 'primevue';
import api from '@/api/axios';
import router from '@/router';

const username = ref('');
const password = ref('');

async function signUp() {
    try {
        await api.post('/auth/signup', {
            username: username.value,
            password: password.value,
            role: 'researcher'
        });
        await router.push('/auth/login');
    } catch (error) {
        console.error(error);
    }
}
</script>
