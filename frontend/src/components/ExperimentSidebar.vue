<template>
  <ALayoutSider collapsible v-model:collapsed="collapsed" width="250" style="background: #fff;">
    <AMenu mode="inline" :inlineCollapsed="collapsed">
      <ASubMenu v-for="project in props.treeData" :key="project.key">
        <template #title>
        <span @click="() => onSelect([project.key])">
          <AFolderOutlined @click="() => onSelect([project.key])"/>
          <span v-if="!collapsed">{{ project.title }}</span>
        </span>
        </template>
        <AMenuItem
            v-for="experiment in project.children" :key="experiment.key"
            @click="() => onSelect([experiment.key])"
        >
          <AFileOutlined/>
          <span>{{ experiment.title }}</span>
        </AMenuItem>
      </ASubMenu>
    </AMenu>
    <template #trigger>
      <div class="ant-layout-sider-trigger">
        <AMenuFoldOutlined v-if="!collapsed"/>
        <AMenuUnfoldOutlined v-if="collapsed"/>
      </div>
    </template>
  </ALayoutSider>
</template>

<script setup lang="ts">
import {defineProps, defineEmits, ref} from 'vue';
import {Menu as AMenu, SubMenu as ASubMenu} from 'ant-design-vue';
import {
  FolderOutlined as AFolderOutlined,
  FileOutlined as AFileOutlined,
  MenuFoldOutlined as AMenuFoldOutlined,
  MenuUnfoldOutlined as AMenuUnfoldOutlined
} from '@ant-design/icons-vue';

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
  console.log(keys)
  emit('select', keys);
};
</script>

<style scoped>
.ant-layout-sider-trigger {
  background-color: #ff6060; /* Фоновый цвет */
  border-radius: 50%; /* Округлая форма */
  font-size: 20px; /* Размер иконки */
  color: white; /* Цвет иконки */
  padding: 8px; /* Отступы */
  cursor: pointer; /* Курсор */
  transition: background-color 0.3s;
}

.ant-layout-sider-trigger:hover {
  background-color: #e05252; /* Фоновый цвет при наведении */
}
</style>