<template>
    <Panel class="p-4">
        <template #header>
            <div>
                <span class="text-xl font-bold">Compare Experiments</span>
            </div>
        </template>
        <div class="flex flex-col gap-6">
            <div class="flex flex-wrap gap-4">
                <MultiSelect
                    v-model="selectedExperiments"
                    :options="experimentOptions"
                    optionLabel="label"
                    placeholder="Select experiments"
                    @change="fetchExperiments"
                    class="w-full md:w-1/2"
                />
                <Select
                    v-if="commonColumns.length"
                    v-model="mainColumn"
                    :options="commonColumns"
                    optionLabel="label"
                    optionValue="label"
                    placeholder="Select main column"
                    class="w-full md:w-1/2"
                />
                <MultiSelect
                    v-if="commonColumns.length"
                    v-model="secondaryColumns"
                    :options="secondaryColumnOptions"
                    optionLabel="label"
                    placeholder="Select secondary columns"
                    class="w-full md:w-1/2"
                />
            </div>
            <div class="mt-6" v-if="experiments.length">
                <div class="card">
                    <Chart
                        v-for="column in secondaryColumns"
                        :key="column.label"
                        type="line"
                        :data="getChartData(column.label)"
                        :options="getChartOptions(column.label)"
                        class="mb-6"
                    />
                </div>
            </div>
        </div>
    </Panel>
</template>

<script setup lang="ts">
import { computed, onMounted, Ref, ref } from 'vue';
import { MultiSelect, Select } from 'primevue';
import Chart from 'primevue/chart';
import Panel from 'primevue/panel';
import api from '@/api/axios';
import { Experiment, FileSystem } from '@/views/Dashboard/typing';

interface ExperimentColumn {
    name: string;
    ontology_ref: string;
}

interface ExperimentFull {
    id: number;
    name: string;
    columns: ExperimentColumn[];
    data: Record<string, any>[];
}

interface SelectOption {
    id: string | number;
    label: string;
}

const selectedExperiments = ref<SelectOption[]>([]);
const experiments = ref<ExperimentFull[]>([]);
const mainColumn = ref<string>('');
const secondaryColumns = ref<{ label: string }[]>([]);

const experimentOptions: Ref<SelectOption[]> = ref([]);

async function fetchExperiments() {
    experiments.value = [];
    for (const exp of selectedExperiments.value) {
        const expOption = experimentOptions.value.find(e => e.id === exp.id);
        if (expOption) {
            const response = await api.get(`/experiment/${exp.id}`);
            const { columns, measurements } = response.data;
            experiments.value.push({ id: Number(exp.id), name: expOption.label, data: measurements, columns });
        }
    }
}

const commonColumns = computed(() => {
    if (experiments.value.length === 0) {
        return [];
    }
    const allColumns = experiments.value.map(exp => exp.columns);
    const common = allColumns.reduce((acc, curr) => acc.filter(col =>
        curr.some(c => c.name === col.name && c.ontology_ref === col.ontology_ref)
    ));
    return common.map(col => ({ label: col.name }));
});

const secondaryColumnOptions = computed(() =>
    commonColumns.value.filter(col => col.label !== mainColumn.value)
);

function getChartData(column: string) {
    if (!mainColumn.value) return { datasets: [] };

    const datasets = experiments.value.map((exp, index) => {
        const sorted = [...exp.data]
            .filter(row => !isNaN(Number(row[column])) && !isNaN(Number(row[mainColumn.value])))
            .sort((a, b) => Number(a[column]) - Number(b[column]));
        return {
            label: exp.name,
            data: sorted.map(row => ({ x: Number(row[column]), y: Number(row[mainColumn.value]) })),
            fill: false,
            borderColor: getColor(index),
            tension: 0
        };
    });

    const labels = Array.from(new Set(
        datasets.flatMap(ds => ds.data.map(point => point.x))
    )).sort((a, b) => a - b);

    return {
        labels,
        datasets
    };
}

function getColor(index: number) {
    const colors = ['#42A5F5', '#66BB6A', '#FFA726', '#EF5350', '#AB47BC'];
    return colors[index % colors.length];
}

function getChartOptions(column: string) {
    if (!mainColumn.value) return {};

    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--p-text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--p-text-muted-color');
    const surfaceBorder = documentStyle.getPropertyValue('--p-content-border-color');

    return {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    color: textColor
                }
            },
            tooltip: {
                callbacks: {
                    title: (context: any) => {
                        const y = context[0].raw.y;
                        return `${mainColumn.value}: ${y}`;
                    },
                    label: (context: any) => {
                        const x = context.raw.x;
                        return `${column}: ${x}`;
                    }
                }
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: column,
                    color: textColor
                },
                ticks: {
                    color: textColorSecondary
                },
                grid: {
                    color: surfaceBorder
                }
            },
            y: {
                title: {
                    display: true,
                    text: mainColumn.value,
                    color: textColor
                },
                ticks: {
                    color: textColorSecondary
                },
                grid: {
                    color: surfaceBorder
                }
            }
        }
    };
}

function flatten(fileSystem: FileSystem): Experiment[] {
    let experiments: Experiment[] = [];
    for (const item of fileSystem) {
        if (!('children' in item)) {
            experiments.push(item as Experiment);
        } else {
            experiments = experiments.concat(flatten(item.children));
        }
    }
    return experiments;
}

onMounted(async () => {
    const params = new URLSearchParams();
    const desired_keys = ['id', 'path'];

    for (const key of desired_keys) {
        params.append('desired_keys', key);
    }

    const response = await api.get<FileSystem>(`experiment/?${params.toString()}`);
    const flattenedExperiments = flatten(response.data);
    experimentOptions.value = flattenedExperiments.map((exp: any) => ({ label: exp.path, id: Number(exp.id) }));
});
</script>
