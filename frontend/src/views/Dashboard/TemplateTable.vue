<template>
    <div class="mb-6">
        <TreeTable
            v-if="templateFS"
            :value="templateFS"
            class="w-full"
            data-key="path"
        >
            <Column expander field="title" header="Название">
                <template #body="{ node }">
                    <span v-if="node.children && node.children.length" class="font-semibold">
                        {{ node.path }}
                    </span>
                    <Button v-else-if="!node.children" class="p-button-text p-0" @click="goToTemplate(node.id)">
                        {{ node.path }}
                    </Button>
                    <span v-else class="font-semibold text-gray-400">
                        {{ node.path }} (пустая папка)
                    </span>
                </template>
            </Column>

            <Column header="Действия">
                <template #body="{ node }">
                    <TemplateActions
                        v-if="!node.children"
                        :template-id="node.id"
                    />
                </template>
            </Column>
        </TreeTable>

        <CreateTemplateDialog />
        <CreateFolderDialog :fs="templateFS" :visible-model="createTemplatesFolderDialog" />
        <MoveDialog :fs="templateFS" :visible-model="moveTemplateDialog" :selected-item="selectedTemplate" />
        <ViewTemplateDialog
            :visible-model="viewTemplateDialog"
            :template-id="currentTemplateId"
        />
    </div>
</template>

<script lang="ts" setup>
import { Button, Column, TreeTable } from 'primevue';
import TemplateActions from '@/views/Dashboard/TemplateActions.vue';
import { useDashboard } from '@/composables/useDashboard';
import CreateFolderDialog from '@/views/Dashboard/CreateFolderDialog.vue';
import MoveDialog from '@/views/Dashboard/MoveDialog.vue';
import CreateTemplateDialog from '@/views/Dashboard/CreateTemplateDialog.vue';
import ViewTemplateDialog from '@/views/Dashboard/ViewTemplateDialog.vue';
import { ref } from 'vue';

const { templateFS, createTemplatesFolderDialog, moveTemplateDialog, selectedTemplate, viewTemplateDialog } = useDashboard();

const currentTemplateId = ref<string | null>(null);

const goToTemplate = async (id: string) => {
    if (!id) return;
    currentTemplateId.value = id;
    viewTemplateDialog.value.visible = true;
};
</script>
