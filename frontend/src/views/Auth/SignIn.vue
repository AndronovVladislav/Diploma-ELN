<template>
    <FloatingConfigurator />
    <div
        class="bg-surface-50 dark:bg-surface-950 flex items-center justify-center min-h-screen min-w-[100vw] overflow-hidden">
        <div class="flex flex-col items-center w-1/2 justify-center">
            <div class="w-full"
                 style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="bg-surface-0 dark:bg-surface-900 py-20 px-8 sm:px-20" style="border-radius: 53px">
                    <div class="flex justify-center">
                        <img alt="Logo" height="180" src="/logo.svg" width="180">
                    </div>

                    <div class="text-center">
                        <div class="text-surface-900 dark:text-surface-0 text-3xl font-medium mb-4">
                            Welcome to AlChem!
                        </div>
                    </div>

                    <div class="card mt-4">
                        <div class="flex flex-col md:flex-row">
                            <div class="w-full md:w-5/12 flex flex-col items-center justify-center gap-3 py-5">
                                <InputGroup class="mt-4">
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
                                <InputGroup class="mb-4">
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
                                <div class="flex">
                                    <Button class="w-full max-w-[17.35rem] mx-auto" icon="pi pi-user"
                                            label="Sign in" @click="signIn">
                                    </Button>
                                </div>
                            </div>
                            <div class="w-full md:w-2/12">
                                <Divider class="!hidden md:!flex" layout="vertical"><b>OR</b></Divider>
                                <Divider align="center" class="!flex md:!hidden" layout="horizontal"><b>OR</b></Divider>
                            </div>
                            <div class="w-full md:w-5/12 flex items-center justify-center py-5">
                                <RouterLink to="/auth/signup">
                                    <Button class="w-full max-w-[17.35rem] mx-auto" icon="pi pi-user-plus"
                                            label="Sign Up">
                                    </Button>
                                </RouterLink>
                            </div>
                        </div>
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
import { useCoreStore } from '@/stores/core';
import router from '@/router';
import { AxiosError } from 'axios';
import { useNotifier } from '@/composables/useNotifier';

const username = ref('');
const password = ref('');
const coreStore = useCoreStore();

const Notifier = useNotifier();

async function signIn() {
    try {
        await api.post('/auth/login', { username: username.value, password: password.value })
            .then(response => {
                coreStore.username = response.data.username;
                coreStore.access_token = response.data.access_token;
                coreStore.refresh_token = response.data.refresh_token;
            });
        await router.push('/');
    } catch (error) {
        console.error(error);
        Notifier.error({ detail: error instanceof AxiosError && error.response ? error.response.data : 'Неизвестная ошибка' });
    }
}

</script>
