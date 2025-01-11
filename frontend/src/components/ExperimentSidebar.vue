<template>
  <ALayoutSider collapsible v-model:collapsed="collapsed" width="250" style="background: #fff;">
    <AMenu mode="inline" :inlineCollapsed="collapsed">
      <ASubMenu v-for="project in props.treeData" :key="project.key">
        <template #title>
        <span>
          <AFolderOutlined/>
          <span v-if="!collapsed">{{ project.title }}</span>
        </span>
        </template>
        <AMenuItem v-for="experiment in project.children" :key="experiment.key">
          <AFileOutlined/>
          <span>{{ experiment.title }}</span>
        </AMenuItem>
      </ASubMenu>
    </AMenu>
  </ALayoutSider>
</template>

<script setup lang="ts">
import {defineProps, defineEmits, ref} from 'vue';
import {Menu as AMenu, SubMenu as ASubMenu} from 'ant-design-vue';
import {FolderOutlined as AFolderOutlined, FileOutlined as AFileOutlined} from '@ant-design/icons-vue';

interface Experiment {
  // icon: string;
  title: string;
  description: string;
  key: string;
  isLeaf: boolean;
}

interface Project {
  // icon: string;
  title: string;
  key: string;
  children: Experiment[];
}

const props = defineProps<{
  treeData: Project[];
}>();

const emit = defineEmits(['select'])

const collapsed = ref<boolean>(false)

const onSelect = (keys: string[]) => {
  emit('select', keys);
};
</script>
