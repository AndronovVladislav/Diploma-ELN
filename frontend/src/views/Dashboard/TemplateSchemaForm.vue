<template>
    <div class="flex flex-col gap-3 px-3 py-4">
        <InputGroup>
            <InputGroupAddon>
                <i class="pi pi-tag"></i>
            </InputGroupAddon>
            <FloatLabel variant="on">
                <InputText
                    id="templateName"
                    :model-value="name"
                    :readonly="readonly"
                    class="w-full"
                />
                <label for="templateName">Название шаблона</label>
            </FloatLabel>
        </InputGroup>

        <InputGroup v-if="!readonly">
            <InputGroupAddon>
                <i class="pi pi-folder"></i>
            </InputGroupAddon>
            <FloatLabel variant="on">
                <Select
                    id="templateFolder"
                    :model-value="selectedFolder"
                    :options="folderOptions"
                    optionLabel="path"
                    class="w-full"
                    :disabled="readonly"
                />
                <label for="templateFolder">Путь</label>
            </FloatLabel>
        </InputGroup>

        <div class="grid grid-cols-2 gap-4">
            <FloatLabel variant="on" class="col-span-1">
                <Textarea
                    id="inputSchema"
                    :model-value="schemas.input"
                    rows="4"
                    autoResize
                    class="w-full"
                    :readonly="readonly"
                />
                <label for="inputSchema">Input schema (JSON)</label>
            </FloatLabel>

            <FloatLabel variant="on" class="col-span-1">
                <Textarea
                    id="outputSchema"
                    :model-value="schemas.output"
                    rows="4"
                    autoResize
                    class="w-full"
                    :readonly="readonly"
                />
                <label for="outputSchema">Output schema (JSON)</label>
            </FloatLabel>

            <FloatLabel variant="on" class="col-span-1">
                <Textarea
                    id="parametersSchema"
                    :model-value="schemas.parameters"
                    rows="4"
                    autoResize
                    class="w-full"
                    :readonly="readonly"
                />
                <label for="parametersSchema">Parameters schema (JSON)</label>
            </FloatLabel>

            <FloatLabel variant="on" class="col-span-1">
                <Textarea
                    id="contextSchema"
                    :model-value="schemas.context"
                    rows="4"
                    autoResize
                    class="w-full"
                    :readonly="readonly"
                />
                <label for="contextSchema">Context schema (JSON)</label>
            </FloatLabel>
        </div>
    </div>
</template>

<script setup lang="ts">
import { FloatLabel, InputGroup, InputGroupAddon, InputText, Select, Textarea } from 'primevue';
import type { SimplifiedView } from '@/views/Dashboard/typing';

defineProps<{
    name: string;
    folderOptions: SimplifiedView[];
    selectedFolder: SimplifiedView | null;
    schemas: {
        input: string;
        output: string;
        parameters: string;
        context: string;
    };
    readonly?: boolean;
}>();
</script>
