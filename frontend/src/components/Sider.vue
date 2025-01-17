<template>
  <ALayoutSider collapsible v-model:collapsed="collapsed" class="sider">
    <ADirectoryTree
        defaultExpandAll
        @select="onSelect"
        :treeData="treeData"
    />
  </ALayoutSider>
</template>

<script setup lang="ts">
import {
  DirectoryTree as ADirectoryTree,
  Layout as ALayout,
} from 'ant-design-vue';
import {ref} from "vue";

const ALayoutSider = ALayout.Sider;

const collapsed = ref<boolean>(false);

const onSelect = (selectedKeys: string[]): void => {
  const selectedKey = selectedKeys[0];
  const [projectKey, experimentKey] = selectedKey.split('-');
  selectedProjectTitle.value = projectKey;
  selectedExperimentTitle.value = experimentKey;
  const experiment = findExperimentByKey(selectedKey);
  if (experiment) {
    selectedExperiment.value = experiment;
  }
};

</script>

<style scoped>

</style>