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
                            Welcome to AlChem!
                        </div>
                        <span class="text-muted-color font-medium">Sign up to continue</span>
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
                                    Username
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
                                    Password
                                </label>
                            </FloatLabel>
                        </InputGroup>

                        <div class="my-4 flex flex-col">
                            <InputGroup>
                                <InputGroupAddon>
                                    <i class="pi pi-lock"></i>
                                </InputGroupAddon>
                                <FloatLabel variant="on">
                                    <Password
                                        v-model="confirmPassword"
                                        :feedback="false"
                                        :toggleMask="true"
                                        class="mb-4"
                                        fluid
                                        inputId="confirmPassword"
                                    >
                                    </Password>
                                    <label class="block text-surface-900 dark:text-surface-0 text-base font-medium"
                                           for="confirmPassword">
                                        Confirm password
                                    </label>
                                </FloatLabel>
                            </InputGroup>
                            <div v-if="passwordError" class="text-red-500 text-sm mb-4">{{ passwordError }}</div>
                        </div>
                        <Button class="w-full" label="Sign up" @click="signUp"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import FloatingConfigurator from '@/components/FloatingConfigurator.vue';
import { ref } from 'vue';
import { FloatLabel, InputGroup, InputGroupAddon, InputText, Password } from 'primevue';
import api from '@/api/axios';
import router from '@/router';
import { useNotifier } from '@/composables/useNotifier';

const Notifier = useNotifier();

const username = ref('');
const password = ref('');
const confirmPassword = ref('');
const passwordError = ref<string | null>(null);

async function signUp() {
    passwordError.value = null;

    if (password.value.length < 12) {
        passwordError.value = 'Пароль должен содержать минимум 12 символов';
        return;
    }

    if (password.value !== confirmPassword.value) {
        passwordError.value = 'Пароли не совпадают';
        return;
    }

    try {
        const response = await api.post('/auth/signup', {
            username: username.value,
            password: password.value,
            role: 'researcher'
        });
        if (response.status === 201) {
            Notifier.success({ detail: 'Вы успешно зарегистрированы!' });
            await router.push('/auth/login');
        }
    } catch (error) {
        if (error.response && error.response.status === 409) {
            Notifier.error({ detail: 'Пользователь с таким именем уже существует' });
        } else {
            console.error(error);
        }
    }
}
</script>
