<template>
  <div style="position: absolute;">
  </div>
  <div class="container">
    <!-- 경고 메시지 추가 -->
    <div v-if="showWarning" class="warning-message">
      {{ warningMessage }}
    </div>

    <h1 style="text-align: center;">정기 예금 상품 비교</h1>
    <div class="company-grid">
      <div style="display: flex; justify-content: center;">
        <div class="product-list">
          <div class="filter-buttons">
            <button @click="clearFilter" :class="{ active: !selectedCompany }">전체 보기</button>
            <button 
              v-for="company in uniqueCompanies" 
              :key="company" 
              @click="filterByCompany(company)"
              :class="{ active: selectedCompany === company }"
            >
              {{ company }}
            </button>
          </div>
          <div v-for="product in filteredProducts" :key="product.fin_prdt_cd" class="product-box">
            <p class="product-name">{{ product.fin_prdt_nm }}</p>
            <p>{{product.kor_co_nm}}</p>
            <div class="interest-rates">
              <p>최고 연 {{ product.options ? product.options.highest_rate : 'Loading...' }} %</p>
              <p>최저 연 {{ product.options ? product.options.lowest_rate : 'Loading...' }} %</p>
            </div>
            <div class="buttons">
              <button @click="addToCompare(product)">
                <span>+</span> 추가하기
              </button>
            </div>
          </div>
        </div>
        <div class="compare-box" :class="{ fixed: isFixed }">
          <h2 style="text-align: center;"> 상품 비교하기</h2>
          <div v-for="product in compare_list" :key="product.fin_prdt_cd" class="product-box">
            <p class="product-name">{{ product.fin_prdt_nm }}</p>
            <p>{{product.kor_co_nm}}</p>
            <div class="interest-rates">
              <p>최고 연 {{ product.options ? product.options.highest_rate : 'Loading...' }} %</p>
              <p>최저 연 {{ product.options ? product.options.lowest_rate : 'Loading...' }} %</p>
            </div>
            <div class="buttons">
              <button @click="removeFromCompare(product)"> <span>-</span> 빼기</button>
            </div>
          </div>
          <div v-for="n in 4 - compare_list.length" :key="n" class="compare-item empty">
            <p>비교할 상품 추가</p>
          </div>
          <button @click="compareProducts" class="compare-button" :disabled="compare_list.length < 2">비교하기</button>
        </div>
      </div>
    </div>
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <h2>비교 결과</h2>
        <div class="compare-grid">
          <div v-for="product in compare_list" :key="product.fin_prdt_cd" class="compare-item">
            <p class="product-name">{{ product.fin_prdt_nm }}</p>
            <p>{{product.kor_co_nm}}</p>
            <div class="interest-rates">
              <p :class="{ highlight: isDifferent('highest_rate', product.options ? product.options.highest_rate : 'Loading...') }">
                최고 연 {{ product.options ? product.options.highest_rate : 'Loading...' }} %
              </p>
              <p :class="{ highlight: isDifferent('lowest_rate', product.options ? product.options.lowest_rate : 'Loading...') }">
                최저 연 {{ product.options ? product.options.lowest_rate : 'Loading...' }} %
              </p>
            </div>
            <div class="details">
              <p :class="{ highlight: isDifferent('join_way', product.join_way) }">가입 방법: {{ product.join_way }}</p>
              <p :class="{ highlight: isDifferent('spcl_cnd', product.spcl_cnd) }">우대 조건: {{ product.spcl_cnd }}</p>
              <p :class="{ highlight: isDifferent('join_member', product.join_member) }">가입 대상: {{ product.join_member }}</p>
              <p :class="{ highlight: isDifferent('max_limit', product.max_limit) }">최고 한도: {{ product.max_limit }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useProductStore } from '@/stores/product'
import { useCustomerStore } from '@/stores/customer'
import axios from 'axios';

const store = useProductStore()
const user = useCustomerStore()
const product_detail = ref([])
const compare_list = ref([])
const selectedCompany = ref(null)
const isFixed = ref(false)
const showModal = ref(false)
const showWarning = ref(false);
const warningMessage = ref("");
const API_URL = 'http://127.0.0.1:8000'

onMounted(() => {
  store.getProduct().then((response) => {
    product_detail.value = store.productall
    product_detail.value.forEach(product => {
      getProductOption(product.fin_prdt_cd).then(options => {
        product.options = options;
      });
    });
  })
})

const addToCompare = (product) => {
  if (compare_list.value.length < 4 && !compare_list.value.includes(product)) {
    compare_list.value.push(product)
  } else {
    showWarningMessage("더 이상 추가할 수 없습니다.");
  }
}

const removeFromCompare = (product) => {
  compare_list.value = compare_list.value.filter(p => p.fin_prdt_cd !== product.fin_prdt_cd)
}

const compareProducts = () => {
  if (compare_list.value.length >= 2) {
    showModal.value = true;
  }
}

const closeModal = () => {
  showModal.value = false;
}

const showWarningMessage = (message) => {
  warningMessage.value = message;
  showWarning.value = true;
  setTimeout(() => {
    showWarning.value = false;
  }, 2000); // 2초 후에 메시지 숨김
}

const getProductOption = async function (fin_prdt_cd) {
  try {
    const response = await axios({
      method: 'get',
      url: `${API_URL}/api/v1/products/getTimeDepogitOption/${fin_prdt_cd}/`,
      headers: { Authorization: `Token ${user.token}` },
    });
    
    const options = response.data;
    const highest_rate = Math.max(...options.map(option => option.intr_rate));
    const lowest_rate = Math.min(...options.map(option => option.intr_rate));
    
    return { highest_rate, lowest_rate };
  } catch (error) {
    console.log(error);
    return { highest_rate: 'N/A', lowest_rate: 'N/A' };
  }
}

const uniqueCompanies = computed(() => {
  const companies = product_detail.value.map(product => product.kor_co_nm);
  return [...new Set(companies)];
});

const filteredProducts = computed(() => {
  if (selectedCompany.value) {
    return product_detail.value.filter(product => product.kor_co_nm === selectedCompany.value);
  }
  return product_detail.value;
});

const filterByCompany = (company) => {
  selectedCompany.value = company;
};

const clearFilter = () => {
  selectedCompany.value = null;
};

// Helper function to check if the value is different across the compare list
const isDifferent = (field, value) => {
  return compare_list.value.some(product => product[field] !== value);
};

</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  width: 1200px;
}

.warning-message {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  background-color: rgba(255, 0, 0, 0.8);
  color: white;
  border-radius: 10px;
  z-index: 1000;
}

.company-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 50px;
}

.product-list {
  display: flex;
  flex-direction: column;
  width: 550px;
  margin-right: 20px;
  max-height: 1100px;
  overflow-y: auto; /* 스크롤 가능하게 설정 */
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
  margin: 10px;
}

.filter-buttons button {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.filter-buttons button.active {
  background-color: #007bff;
  color: white;
}

.product-box {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  margin: 5px;
}

.product-name {
  font-size: 1.2em;
  font-weight: bold;
}

.interest-rates {
  margin-top: 10px;
}

.buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.buttons button {
  border: none;
  background-color: #007bff;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.buttons button span {
  margin-right: 5px;
}

.compare-box {
  position: sticky;
  width: 550px;
  top: 150px;
  max-height: 1100px;
  background: #f9f9f9;
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 10px;
}

.compare-item {
  justify-content: space-between;
  margin-bottom: 10px;
  padding: 5px;
  background: #fff;
  border-radius: 5px;
}

.compare-item.empty {
  background: #f0f0f0;
  justify-content: center;
}

.compare-button {
  font-size: 20px;
  width: 100%;
  height: 50px;
  border: 1px solid #ccc;
  background-color: #007bff;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

.compare-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0,0,0);
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 1500px;
  border-radius: 10px;
  position: relative;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.compare-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.compare-item {
  flex: 1;
  min-width: 200px;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.details {
  margin-top: 10px;
}

.highlight {
  background-color: rgba(255, 255, 0, 0.603);
  border-radius: 10%;
}
</style>
