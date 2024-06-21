<template>
  <div class="container">
    <h1 style="text-align: center;">정기 적금 상품 정보</h1>
    <div class="filter-container">
      <div style="position: relative; left: 120px;">
      <label for="bank-filter">은행 선택: </label>
      <select id="bank-filter" v-model="selectedBank" @change="filterByBank">
        <option value="">전체</option>
        <option v-for="bank in uniqueBanks" :key="bank" :value="bank">{{ bank }}</option>
      </select>
    </div>
    </div>
    <div class="company-grid">
      <table>
        <thead>
          <tr>
            <th>상품번호</th>
            <th>은행이름</th>
            <th>상품명</th>
            <th class="td-text">1개월</th>
            <th class="td-text">3개월</th>
            <th class="td-text">6개월</th>
            <th class="td-text">12개월</th>
            <th class="td-text">24개월</th>
            <th class="td-text">36개월</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="saving in filteredSavings" :key="saving.id" @click="goToDetail(saving.id)">
            <td class="td-text">{{ saving.id }}</td>
            <td>{{ saving.kor_co_nm }}</td>
            <td>{{ saving.fin_prdt_nm }}</td>
            <td class="td-text">{{ saving.rates['1'] || 'N/A' }}</td>
            <td class="td-text">{{ saving.rates['3'] || 'N/A' }}</td>
            <td class="td-text">{{ saving.rates['6'] || 'N/A' }}</td>
            <td class="td-text">{{ saving.rates['12'] || 'N/A' }}</td>
            <td class="td-text">{{ saving.rates['24'] || 'N/A' }}</td>
            <td class="td-text">{{ saving.rates['36'] || 'N/A' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useProductStore } from '@/stores/product'
import { useRouter } from 'vue-router'

const store = useProductStore()
const savingListWithRates = ref([])
const selectedBank = ref('')
const router = useRouter()

const fetchInterestRates = async (fin_prdt_cd) => {
  try {
    await store.getSavingOptionDetail(fin_prdt_cd)
    const savingoptions = store.savingoptiondetail
    const rates = {
      '1': '-',
      '3': '-',
      '6': '-',
      '12': '-',
      '24': '-',
      '36': '-',
    }
    for (const option of savingoptions) {
      if (option.save_trm in rates) {
        rates[option.save_trm] = option.intr_rate2
      }
    }
    return rates
  } catch (error) {
    console.error(`Error fetching interest rates for ${fin_prdt_cd}:`, error)
    return {}
  }
}

const fetchSavingListWithRates = async () => {
  try {
    await store.getSaving()
    const savings = store.savingall
    const savingsWithRates = await Promise.all(savings.map(async (saving) => {
      const rates = await fetchInterestRates(saving.fin_prdt_cd)
      return { ...saving, rates }
    }))
    savingListWithRates.value = savingsWithRates
  } catch (error) {
    console.error('Error fetching product list with rates:', error)
  }
}

const goToDetail = (savingId) => {
  window.scrollTo({
    top: 0,
  })
  router.push({ name: 'SavingDetailView', params: { id: savingId } })
}

const uniqueBanks = computed(() => {
  const banks = savingListWithRates.value.map(saving => saving.kor_co_nm)
  return [...new Set(banks)]
})

const filteredSavings = computed(() => {
  if (!selectedBank.value) {
    return savingListWithRates.value
  }
  return savingListWithRates.value.filter(saving => saving.kor_co_nm === selectedBank.value)
})

const filterByBank = () => {
  console.log(`Selected bank: ${selectedBank.value}`)
}

onMounted(fetchSavingListWithRates)
</script>

<style scoped>
.td-text{
  text-align: center;
}

.container {
  display: flex;
  flex-direction: column;
  width: 1200px;
}

.filter-container {
  margin-bottom: 20px;
}

.company-grid {
  display: flex;
  justify-content: center;
  width: 98%;
  overflow-x: auto;
  margin: 10px;
}

table {
  border-collapse: collapse;
  text-align: left;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f2f2f2;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f1f1;
}
</style>
