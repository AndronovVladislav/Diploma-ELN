<template>
  <ConfigProvider :theme="{ token: { colorPrimary: '#ff6060' } }"/>
  <ALayout style="min-height: 100vh">
    <!-- Сайдбар -->
    <ExperimentSidebar
        :treeData="treeData"
        @select="onSelect"
    />

    <ALayout>
      <!-- Верхняя панель с вкладками -->
      <ALayoutHeader style="background: #fff; padding: 0">
        <AMenu mode="horizontal" :defaultSelectedKeys="['experiments']">
          <AMenuItem key="dashboard" @click="navigateTo('Dashboard')">Панель управления</AMenuItem>
          <AMenuItem key="experiments" @click="navigateTo('Experiments')">Эксперименты</AMenuItem>
          <AMenuItem key="templates" @click="navigateTo('Templates')">Шаблоны</AMenuItem>
          <AMenuItem key="settings" @click="navigateTo('Settings')">Настройки</AMenuItem>
        </AMenu>
      </ALayoutHeader>

      <!-- Основное окно для просмотра и редактирования экспериментов -->
      <ALayoutContent style="margin: 0 16px; padding: 24px; background: #fff;">
        <h1>Эксперименты</h1>
        <div v-if="selectedExperiment">
          <h2>{{ selectedExperiment.title }}</h2>
          <p>{{ selectedExperiment.description }}</p>
          <AButton type="primary" @click="editExperiment">Редактировать</AButton>
        </div>
        <div v-else-if="currentProjectExperiments.length > 0">
          <ExperimentList
              :experiments="currentProjectExperiments"
              @select="onExperimentSelect"
          />
        </div>
        <div v-else>
          <p>Выберите эксперимент или проект для просмотра или редактирования.</p>
        </div>
      </ALayoutContent>

      <!-- Подвал -->
      <Footer/>
    </ALayout>
  </ALayout>
</template>

<script setup lang="ts">
import {ref, computed} from 'vue'
import {useRouter} from 'vue-router'
import {
  ConfigProvider,
  Layout as ALayout,
  LayoutHeader as ALayoutHeader,
  LayoutContent as ALayoutContent,
  Menu as AMenu,
  MenuItem as AMenuItem,
  Button as AButton
} from 'ant-design-vue'
import ExperimentSidebar from '../components/ExperimentSidebar.vue'
import ExperimentList from '../components/ExperimentList.vue'
import Footer from '../components/Footer.vue'

interface Experiment {
  icon: string
  title: string
  description: string
  key: string
  isLeaf: boolean
}

interface Project {
  icon: string
  title: string
  key: string
  children: Experiment[]
}

const selectedProjectKey = ref<string>('')
const selectedExperiment = ref<Experiment | null>(null)

const treeData: Project[] = [
  {
    title: 'Проект 1',
    key: 'project-1',
    icon: 'FolderOutlined',
    children: [
      {
        title: 'Эксперимент 1.1',
        description: 'Описание эксперимента 1.1',
        key: 'experiment-1.1',
        isLeaf: true,
        icon: 'FileOutlined',
      },
      {
        title: 'Эксперимент 1.2',
        description: 'Описание эксперимента 1.2',
        key: 'experiment-1.2',
        isLeaf: true,
        icon: 'FileOutlined',
      },
    ],
  },
  {
    title: 'Проект 2',
    key: 'project-2',
    icon: 'FolderOutlined',
    children: [
      {
        title: 'Эксперимент 2.1',
        description: 'Описание эксперимента 2.1',
        key: 'experiment-2.1',
        isLeaf: true,
        icon: 'FileOutlined',
      },
      {
        title: 'Эксперимент 2.2',
        description: 'Описание эксперимента 2.2',
        key: 'experiment-2.2',
        isLeaf: true,
        icon: 'FileOutlined',
      },
    ],
  },
]

const currentProjectExperiments = computed(() => {
  const project = treeData.find(p => p.key === selectedProjectKey.value)
  return project ? project.children : []
})

const onSelect = (keys: string[]) => {
  selectedExperiment.value = findExperimentByKey(keys[0])
  if (selectedExperiment.value === null) {
    const project = treeData.find(proj => proj.key === keys[0])
    if (project) {
      selectedProjectKey.value = project.key
    }
  } else {
    selectedProjectKey.value = ''
  }
}

const onExperimentSelect = (key: string) => {
  const experiment = findExperimentByKey(key)
  if (experiment) {
    selectedExperiment.value = experiment
  }
}

const findExperimentByKey = (key: string): Experiment | null => {
  for (const project of treeData) {
    for (const experiment of project.children) {
      if (experiment.key === key) {
        return experiment
      }
    }
  }
  return null
}

const editExperiment = () => {
  if (selectedExperiment.value) {
    alert(`Редактирование эксперимента: ${selectedExperiment.value.title}`)
  }
}

const router = useRouter()

const navigateTo = (name: string) => {
  router.push({name})
}
</script>
