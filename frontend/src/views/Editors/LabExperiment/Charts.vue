<template>
    <div v-if="mainColumn && data.length">
        <div class="card">
            <Chart
                v-for="column in otherColumns"
                :key="column"
                type="line"
                :data="getChartData(column)"
                :options="getChartOptions(column)"
                class="mb-6"
            />
        </div>
    </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import Chart from 'primevue/chart';

const props = defineProps<{
    mainColumn: string
    data: Record<string, any>[]
}>();

const otherColumns = computed(() =>
    props.data.length ? Object.keys(props.data[0]).filter(col => col !== props.mainColumn && col !== 'row') : []
);

function getChartData(column: string) {
    const sortedData = props.data.slice().sort((a, b) => a[column] - b[column]);
    return {
        labels: sortedData.map(row => row[column]),
        datasets: [
            {
                label: column,
                data: sortedData.map(row => row[props.mainColumn]),
                fill: false,
                borderColor: '#42A5F5',
                tension: 0
            }
        ]
    };
}

function getChartOptions(column: string) {
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
                        const y = context[0].raw;
                        return `${props.mainColumn}: ${y}`;
                    },
                    label: (context: any) => {
                        const x = context.label;
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
                    text: props.mainColumn,
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
</script>
