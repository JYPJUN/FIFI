<template>
  <canvas ref="canvas"></canvas>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import { Chart, LineController, LineElement, PointElement, LinearScale, Title, CategoryScale, Tooltip, Legend } from 'chart.js';

Chart.register(LineController, LineElement, PointElement, LinearScale, Title, CategoryScale, Tooltip, Legend);

const props = defineProps({
  chartData: {
    type: Object,
    required: false
  }
});

const canvas = ref(null);
let chartInstance = null;

onMounted(() => {
  if (props.chartData) {
    chartInstance = new Chart(canvas.value, {
      type: 'line',
      data: props.chartData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: 'category'
          },
          y: {
            beginAtZero: true,
            ticks: {
              callback: function(value) {
                return value.toFixed(2);
              }
            }
          }
        },
        plugins: {
          legend: {
            display: true
          },
          tooltip: {
            enabled: true
          }
        },
        elements: {
          line: {
            tension: 0.3
          },
          point: {
            radius: 2,
            hitRadius: 5,
            hoverRadius: 4
          }
        }
      }
    });
  }
});

watch(
  () => props.chartData,
  (newData) => {
    if (chartInstance) {
      chartInstance.data = newData;
      chartInstance.update();
    } else if (newData) {
      chartInstance = new Chart(canvas.value, {
        type: 'line',
        data: newData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              type: 'category'
            },
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  return value.toFixed(2);
                }
              }
            }
          },
          plugins: {
            legend: {
              display: true
            },
            tooltip: {
              enabled: true
            }
          },
          elements: {
            line: {
              tension: 0.3
            },
            point: {
              radius: 2,
              hitRadius: 5,
              hoverRadius: 4
            }
          }
        }
      });
    }
  }
);
</script>

<style scoped>
canvas {
  width: 100% !important;
  max-width: 1000px;
  height: 400px !important;
}
</style>
