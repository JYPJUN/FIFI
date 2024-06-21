<template>
  <div class="container">
    <div class="calculator-section" style="margin: 20px;">
      <h1>환율 계산기</h1>
      <div class="input-group">
        <label for="currency1">환전할 통화:</label>
        <div class="input-wrapper">
          <input v-model.number="amount" type="number" id="amount1" placeholder="금액" />
          <select v-model="selectedCurrency1" id="currency1">
            <option v-for="item in uniqueCurrencies" :value="item.cur_unit" :key="item.cur_unit">
              {{ item.cur_nm }} ({{ item.cur_unit }})
            </option>
          </select>
        </div>
      </div>
      <div class="input-group">
        <label for="currency2">받을 통화:</label>
        <div class="input-wrapper">
          <input v-model="convertedAmount" type="number" id="amount2" readonly />
          <select v-model="selectedCurrency2" id="currency2">
            <option v-for="item in uniqueCurrencies" :value="item.cur_unit" :key="item.cur_unit">
              {{ item.cur_nm }} ({{ item.cur_unit }})
            </option>
          </select>
        </div>
      </div>
      <div v-if="calculatedRates" class="rates">
        <p>1 {{ selectedCurrency1 }} = {{ calculatedRates.exchangeRate }} {{ selectedCurrency2 }}</p>
      </div>
    </div>

    <div class="graph-section" style="text-align: center; margin: 20px;">
      <h2>환율 그래프 ({{ selectedCurrency2 }})</h2>
      <line-chart v-if="chartData" :chart-data="chartData" class="chart"></line-chart>
    </div>
  </div>
</template>

<script setup>
import { useExchangeStore } from '@/stores/exchange';
import { ref, onMounted, computed, watch } from 'vue';
import LineChart from './LineChart.vue'; // LineChart 컴포넌트를 import 합니다.

const store = useExchangeStore();
const detail = ref([]);
const amount = ref(1);
const selectedCurrency1 = ref('KRW'); // 기본값을 'USD'로 설정
const selectedCurrency2 = ref('USD'); // 기본값을 'KRW'로 설정
const calculatedRates = ref(null);
const convertedAmount = ref(0);

onMounted(() => {
  store.getExchange().then(() => {
    detail.value = store.exchangedetail;
    calculateRates();
  });
});

const uniqueCurrencies = computed(() => {
  const seen = new Set();
  return detail.value.filter(item => {
    if (seen.has(item.cur_unit)) {
      return false;
    } else {
      seen.add(item.cur_unit);
      return true;
    } 
  });
});

watch([amount, selectedCurrency1, selectedCurrency2, detail], () => {
  calculateRates();
});

const calculateRates = () => {
  const currency1 = getLatestCurrencyRate(selectedCurrency1.value);
  const currency2 = getLatestCurrencyRate(selectedCurrency2.value);
  if (currency1 && currency2) {
    const exchangeRate = currency1.deal_bas_r / currency2.deal_bas_r;
    calculatedRates.value = {
      exchangeRate: exchangeRate.toFixed(6),
      convertedAmount: (amount.value * exchangeRate).toFixed(6)
    };
    convertedAmount.value = (amount.value * exchangeRate).toFixed(6);
  } else {
    calculatedRates.value = null;
    convertedAmount.value = 0;
  }
};

const getLatestCurrencyRate = (currency) => {
  const currencyRates = detail.value.filter(item => item.cur_unit === currency);
  if (currencyRates.length === 0) return null;
  return currencyRates.reduce((latest, item) => {
    return new Date(item.date) > new Date(latest.date) ? item : latest;
  }, currencyRates[0]);
};

const getFilteredData = () => {
  return detail.value.filter(item => item.cur_unit === selectedCurrency2.value);
};

const chartData = computed(() => {
  if (!selectedCurrency2.value) return null;
  const currencyData = getFilteredData();
  const labels = currencyData.map(item => item.date);
  const data = currencyData.map(item => item.deal_bas_r);
  return {
    labels: labels,
    datasets: [
      {
        label: `매매 기준율 (${selectedCurrency2.value})`,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
        hoverBackgroundColor: 'rgba(75, 192, 192, 0.4)',
        hoverBorderColor: 'rgba(75, 192, 192, 1)',
        data: data,
        fill: false,
        lineTension: 0,
        pointRadius: 1,
        pointHoverRadius: 3
      }
    ]
  };
});
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-between;
  max-width: 1500px;
  margin: 0 auto;
  text-align: center;
  margin-top: 40px;
  padding: 50px;
}

.calculator-section, .graph-section {
  width: 45%;
}

.calculator-section {
  margin-right: 20px;
}

.input-group {
  margin-bottom: 20px;
  text-align: left;
}

.input-wrapper {
  display: flex;
  align-items: center;
}

.input-wrapper input,
.input-wrapper select {
  padding: 10px;
  font-size: 1em;
}

.input-wrapper input {
  width: 50%;
  margin-right: 20px;
}

.input-wrapper select {
  width: 50%;
}

.rates {
  margin-top: 20px;
  text-align: left;
}

.graph-section {
  margin-top: 20px;
  text-align: left;
}

.chart {
  max-width: 1000px;
  margin: 0 auto;
}

canvas {
  width: 100% !important;
  max-width: 1000px;
  height: 400px !important;
}
</style>
