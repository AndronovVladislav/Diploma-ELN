<template>
    <div class="flex flex-col bg-surface-800 gap-0 rounded-lg shadow-md">
        <BubbleMenu
            :editor="editor"
            :tippy-options="{ duration: 100 }"
            v-if="editor"
        >
            <div class="bubble-menu flex gap-2 bg-surface-800 p-2 rounded-lg shadow-md">
                <Button @click="editor.chain().focus().toggleBold().run()"
                        class="text-white hover:bg-gray-700 px-3 py-1 rounded font">
                    Bold
                </Button>
                <Button @click="editor.chain().focus().toggleItalic().run()"
                        class="text-white hover:bg-gray-700 px-3 py-1 rounded">
                    Italic
                </Button>
                <Button @click="editor.chain().focus().toggleStrike().run()"
                        class="text-white hover:bg-gray-700 px-3 py-1 rounded">
                    Strike
                </Button>
            </div>
        </BubbleMenu>
        <div class="bg-surface-800 text-surface-300 flex justify-between p-3 rounded-t-lg">
            <div class="flex gap-2">
                <Button @click="editor.chain().focus().toggleBold().run()"
                        :class="['px-3 py-1 min-w-[32px] min-h-[32px] flex items-center justify-center rounded', {'font-bold': editor?.isActive('bold') }]">
                    B
                </Button>
                <Button @click="editor.chain().focus().toggleItalic().run()"
                        :class="['px-3 py-1 min-w-[32px] min-h-[32px] flex items-center justify-center rounded', {'font-bold': editor?.isActive('italic') }]">
                    I
                </Button>
                <Button @click="editor.chain().focus().toggleStrike().run()"
                        :class="['px-3 py-1 min-w-[32px] min-h-[32px] flex items-center justify-center rounded', {'font-bold': editor?.isActive('strike') }]">
                    S
                </Button>
            </div>
        </div>
        <div class="border border-surface-800 bg-surface-300 p-1 rounded-lg">
            <EditorContent :editor="editor" class="min-h-[300px] bg-primary-contrast p-4 rounded-md" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { Button } from 'primevue';
import { BubbleMenu, Editor, EditorContent } from '@tiptap/vue-3';
import { onMounted, ref, watch } from 'vue';
import StarterKit from '@tiptap/starter-kit';

const editor = ref(null);

interface Props {
    description: string,
}

const props = defineProps<Props>();

// const editorModules = ref({
//     toolbar: [
//         [{ header: [1, 2, 3, false] }],
//         ['bold', 'italic', 'underline'],
//         [{ list: 'ordered' }, { list: 'bullet' }],
//         ['clean']
//     ]
// });

watch(() => props.description, (newValue) => {
    if (editor.value) {
        editor.value.commands.setContent('<p>' + newValue + '</p>');
    }
});

onMounted(() => {
    console.log(props.description);
    editor.value = new Editor({
        content: '<p>' + props.description + '</p>',
        extensions: [StarterKit]
        // modules: editorModules.value,
    });
});
</script>

<style lang="scss">
.ProseMirror:focus {
    outline: none;
}
</style>
