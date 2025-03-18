<template>
    <div class="flex flex-col bg-surface-800 gap-0 rounded-lg shadow-md">
        <BubbleMenu
            v-if="editor"
            :editor="editor"
            :tippy-options="{ duration: 100 }"
        >
            <div class="bubble-menu flex gap-2 bg-surface-800 p-2 rounded-lg shadow-md">
                <Button class="text-white hover:bg-gray-700 px-3 py-1 rounded font"
                        @click="editor.chain().focus().toggleBold().run()">
                    Bold
                </Button>
                <Button class="text-white hover:bg-gray-700 px-3 py-1 rounded"
                        @click="editor.chain().focus().toggleItalic().run()">
                    Italic
                </Button>
                <Button class="text-white hover:bg-gray-700 px-3 py-1 rounded"
                        @click="editor.chain().focus().toggleStrike().run()">
                    Strike
                </Button>
            </div>
        </BubbleMenu>
        <div class="bg-surface-800 text-surface-300 flex justify-between p-3 rounded-t-lg">
            <div class="flex gap-2">
                <Button :class="['px-3 py-1 min-w-[32px] min-h-[32px] flex items-center justify-center rounded', {'font-bold': editor?.isActive('bold') }]"
                        @click="editor.chain().focus().toggleBold().run()">
                    B
                </Button>
                <Button :class="['px-3 py-1 min-w-[32px] min-h-[32px] flex items-center justify-center rounded', {'font-bold': editor?.isActive('italic') }]"
                        @click="editor.chain().focus().toggleItalic().run()">
                    I
                </Button>
                <Button :class="['px-3 py-1 min-w-[32px] min-h-[32px] flex items-center justify-center rounded', {'font-bold': editor?.isActive('strike') }]"
                        @click="editor.chain().focus().toggleStrike().run()">
                    S
                </Button>
            </div>
        </div>
        <div class="border border-surface-800 bg-surface-300 p-1 rounded-lg">
            <EditorContent :editor="editor" class="min-h-[300px] bg-primary-contrast p-4 rounded-md" />
        </div>
    </div>
</template>

<script lang="ts" setup>
import { Button } from 'primevue';
import { BubbleMenu, Editor, EditorContent } from '@tiptap/vue-3';
import { onMounted, ref, watch } from 'vue';
import StarterKit from '@tiptap/starter-kit';

const editor = ref(null);

interface Props {
    description: string,
}

const props = defineProps<Props>();

watch(() => props.description, (newValue) => {
    if (editor.value) {
        editor.value.commands.setContent('<p>' + newValue + '</p>');
    }
});

onMounted(() => {
    editor.value = new Editor({
        content: '<p>' + props.description + '</p>',
        extensions: [StarterKit]
    });
});
</script>

<style lang="scss" scoped>
.ProseMirror:focus {
    outline: none;
}
</style>
