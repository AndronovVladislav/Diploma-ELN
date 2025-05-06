<template>
    <div v-if="form_info" class="grid grid-cols-2">
        <Card class="m-4">
            <template #title>
                <div class="mb-4">
                    Профиль пользователя
                </div>
            </template>

            <template #content>
                <div class="grid grid-cols-5">
                    <Avatar icon="pi pi-user" size="xlarge" class="col-span-1" />
                    <div class="col-span-4">
                        <IftaLabel class="mb-2">
                            <InputText id="username" v-model="form_info.username" variant="filled" disabled />
                            <label for="username">Никнейм</label>
                        </IftaLabel>
                        <IftaLabel class="mb-2">
                            <InputText id="name" v-model="form_info.name" variant="filled" />
                            <label for="name">Имя</label>
                        </IftaLabel>
                        <IftaLabel class="mb-2">
                            <InputText id="surname" v-model="form_info.surname" variant="filled" />
                            <label for="surname">Фамилия</label>
                        </IftaLabel>
                        <IftaLabel class="mb-2">
                            <InputText id="position" v-model="form_info.position" variant="filled" />
                            <label for="position">Должность</label>
                        </IftaLabel>
                        <IftaLabel class="mb-2">
                            <InputText id="registered_at" :value="formattedDate(form_info.registered_at)"
                                       variant="filled" disabled />
                            <label for="registered_at">Дата регистрации</label>
                        </IftaLabel>
                    </div>
                </div>
            </template>

            <template #footer>
                <div class="flex justify-end" v-if="isDirty">
                  <Button label="Сохранить" icon="pi pi-check" @click="saveProfile" class="p-button-success p-mr-2" />
                  <Button label="Отмена" icon="pi pi-times" @click="cancelEdit" class="p-button-secondary p-button-text" />
                </div>
            </template>
        </Card>

        <Card class="m-4">
            <template #title>
                Статистика экспериментов
            </template>

            <template #content>
                <p>Всего: {{ stats.total }}</p>
                <p>Лабораторных: {{ stats.lab }}</p>
                <p>Вычислительных: {{ stats.comp }}</p>
                <DataTable :value="stats.recent" responsiveLayout="scroll">
                    <Column header="Название">
                        <template #body="slotProps">
                            <a :href="slotProps.data.link" target="_blank" class="text-blue-600 hover:underline">
                                {{ slotProps.data.name }}
                            </a>
                        </template>
                    </Column>
                    <Column field="date" header="Дата" />
                </DataTable>
            </template>
        </Card>
    </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { computed, onBeforeMount, ref } from 'vue';

import Card from 'primevue/card';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import api from '@/api/axios';
import { AxiosError } from 'axios';
import { useNotifier } from '@/composables/useNotifier';
import { ExperimentKind } from '@/views/Dashboard/typing';

const Notifier = useNotifier();

interface UserInfo {
    username: string;
    name: string;
    surname: string;

    registered_at: string;
    last_login: string;

    position: string;
    email: string;

    experiments: {
        id: number
        name: string
        kind: ExperimentKind
        updated_at: string
    }[];
}

interface RecentExperiment {
    id: number;
    name: string;
    link: string;
    date: string;
}

const router = useRouter();
const user_info = ref<UserInfo>();
const form_info = ref<Partial<UserInfo>>({});

const stats = computed(() => {
    if (!user_info.value) {
        return { lab: 0, comp: 0, total: 0, recent: [] };
    }

    const exps = user_info.value.experiments;
    const lab = exps.filter(e => e.kind === ExperimentKind.LABORATORY).length;
    const comp = exps.length - lab;
    const total = exps.length;
    const sorted = [...exps].sort((a, b) =>
        new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
    );
    const recent: RecentExperiment[] = sorted.slice(0, 5).map(e => ({
        id: e.id,
        name: e.name,
        link: `/experiment/${e.kind === ExperimentKind.LABORATORY ? 'laboratory' : 'computational'}/${e.id}`,
        date: e.updated_at.slice(0, 10)
    }));
    return { lab, comp, total, recent };
});

function formattedDate(dt: string): string {
    return new Date(dt).toLocaleString('ru-RU', {
        dateStyle: 'medium',
        timeStyle: 'short'
    });
}

async function saveProfile(): Promise<void> {
    const payload = {
        username: form_info.value.username,
        name: form_info.value.name,
        surname: form_info.value.surname,
        position: form_info.value.position
    };
    try {
        const { data } = await api.patch<UserInfo>('/user/profile', payload);
        user_info.value = data;
        form_info.value = { ...data };
        Notifier.success({ detail: 'Профиль успешно обновлён' });
    } catch (error) {
        Notifier.error({
            detail: error instanceof AxiosError && error.response ? error.response.data : 'Ошибка при обновлении профиля'
        });
    }
}

function cancelEdit(): void {
    if (user_info.value) {
        form_info.value = { ...user_info.value };
    }
}

const isDirty = computed((): boolean => {
  if (!user_info.value) {
    return false;
  }
  return (
    form_info.value.username !== user_info.value.username ||
    form_info.value.name !== user_info.value.name ||
    form_info.value.surname !== user_info.value.surname ||
    form_info.value.position !== user_info.value.position
  );
});

onBeforeMount(async () => {
    try {
        user_info.value = (await api.get<UserInfo>('/user/profile')).data;
        form_info.value = { ...user_info.value };
    } catch (error) {
        console.log(error);
        Notifier.error({ detail: error instanceof AxiosError && error.response ? error.response.data : 'Неизвестная ошибка' });
    }
});
</script>
