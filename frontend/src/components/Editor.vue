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
                    <b>Bold</b>
                </Button>
                <Button class="text-white hover:bg-gray-700 px-3 py-1 rounded"
                        @click="editor.chain().focus().toggleItalic().run()">
                    <i>Italic</i>
                </Button>
                <Button class="text-white hover:bg-gray-700 px-3 py-1 rounded"
                        @click="editor.chain().focus().toggleStrike().run()">
                    <s>Strike</s>
                </Button>
            </div>
        </BubbleMenu>
        <div class="bg-surface-800 text-surface-300 flex justify-between p-3 rounded-t-lg">
            <div class="flex gap-2">
                <Button
                    :class="['px-3 py-1 min-w-[32px] min-h-[32px] flex items-center justify-center rounded text-primary-contrast', {'font-bold': editor?.isActive('heading') }]"
                    @click="editor.chain().focus().toggleHeading({level: 1}).run()">
                    <p>H<sub>1</sub></p>
                </Button>
                <Button
                    :class="['px-3 py-1 min-w-[32px] min-h-[32px] flex items-center justify-center rounded text-primary-contrast', {'bg-surface-600': editor?.isActive('code') }]"
                    @click="editor.chain().focus().toggleCode().run()">
                    <>
                </Button>
                <Button
                    class="px-3 py-1 min-w-[32px] min-h-[32px] flex items-center justify-center rounded text-color"
                    @click="editor.chain().focus().toggleBulletList().run()">
                    •
                </Button>
                <Button
                    class="px-3 py-1 min-w-[32px] min-h-[32px] flex items-center justify-center rounded text-color"
                    @click="editor.chain().focus().toggleOrderedList().run()">
                    1.
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
import { onBeforeMount, ref } from 'vue';
import StarterKit from '@tiptap/starter-kit';
import type { Optional } from '@/typing';

const editor = ref<Optional<Editor>>(null);

interface Props {
    description: string,
}

const props = defineProps<Props>();

const emit = defineEmits<{
    (e: 'update:description', value: string): void
}>();


onBeforeMount(() => {
    editor.value = new Editor({
        content: props.description,
        extensions: [StarterKit]
    });

    editor.value.on('update', () => {
        emit('update:description', editor.value?.getHTML() ?? '');
    });
});
</script>

<style lang="scss">
.ProseMirror {
    ul, ol {
        margin: 0.5rem 0;
        padding-left: 1.5rem;
        color: var(--text-color);
    }

    ul {
        list-style-type: disc;
    }

    ol {
        list-style-type: decimal;
    }

    li {
        margin-bottom: 0.25rem;
    }
}

.ProseMirror:focus {
    outline: none;
}
</style>
