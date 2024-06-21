<template>
  <div>
    <div class="container">
      <h1 class="title">정기 적금 상세</h1>
      <div class="saving-detail">
        <table>
          <tr>
            <td class="label">상품 번호:</td>
            <td class="value">{{ savingId }}</td>
          </tr>
          <tr>
            <td class="label">금융회사명:</td>
            <td class="value">{{ saving.kor_co_nm }}</td>
          </tr>
          <tr>
            <td class="label">상품 명:</td>
            <td class="value">{{ saving.fin_prdt_nm }}</td>
          </tr>
          <tr>
            <td class="label">가입 방법:</td>
            <td class="value">{{ saving.join_way }}</td>
          </tr>
          <tr>
            <td class="label">만기 후 이자율:</td>
            <td class="value">
              <div v-for="text in saving.mtrt_int.split('\n').map(line => line)">
                {{ text }}
              </div>
            </td>
          </tr>
          <tr>
            <td class="label">우대조건:</td>
            <td class="value">{{ saving.spcl_cnd }}</td>
          </tr>
          <tr>
            <td class="label">가입 대상:</td>
            <td class="value">{{ saving.join_member }}</td>
          </tr>
          <tr>
            <td class="label">기타 사항:</td>
            <td class="value">
              <div v-for="text in saving.etc_note.split('\n').map(line => line)">
                {{ text }}
              </div>
            </td>
          </tr>
          <tr>
            <td class="label">최고 한도:</td>
            <td class="value">{{ formatNumber(saving.max_limit) || '-' }}</td>
          </tr>
        </table>
        <button 
          :class="['action-button', join ? 'cancel-button' : 'join-button']" 
          @click="SignUpSavingProduct(savingId)"
        >
          {{ join ? '해지하기' : '가입하기' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useProductStore } from '@/stores/product'
import { useCustomerStore } from '@/stores/customer'
import axios from 'axios';

const route = useRoute()
const savingId = route.params.id
const store = useProductStore()
const user = useCustomerStore()
const listSaving = ref(null)
const API_URL = 'http://127.0.0.1:8000'

const saving = computed(() => store.savingall.find(saving => saving.id.toString() === savingId))
const join = ref(false)

const formatNumber = (value) => {
  if (!value) return '';
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

const SignUpSavingProduct = function (pk) {
  axios({
    method: 'post',
    url: `${API_URL}/api/v1/products/saving/${pk}/join/`,
    headers: {Authorization: `Token ${user.token}`},
  })
  .then(response => {
    join.value = !join.value; // 가입 상태를 반전시킴
  })
  .catch(error => {
    console.log(error)
  })
}

const CheckSignup = function () {
  return axios({
    method: 'get',
    url: `${API_URL}/api/v1/products/saving/signup/`,
    headers: {Authorization: `Token ${user.token}`},
  })
  .then(response => {
    listSaving.value = response.data
  })
  .catch(error => {
    console.log(error)
  })
}

onMounted(() => {
  CheckSignup().then(() => {
    for (const save of listSaving.value) {
      if (save.id.toString() === savingId) {
        join.value = true
    }}
  })
})
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  margin: 0 auto;
  width: 1200px;
}

.company-grid {
  display: flex;
  justify-content: center;
  width: 98%;
  overflow-x: auto;
  margin: 10px;
}

.title {
  text-align: center;
  font-size: 2em;
  margin-bottom: 20px;
}

.saving-detail {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  margin: 20px;
}

.saving-detail table {
  width: 100%;
  border-collapse: collapse;
}

.saving-detail td {
  padding: 8px;
  border: 1px solid #ddd;
}

.label {
  font-weight: bold;
  width: 30%;
  background-color: #f2f2f2;
}

.value {
  width: 70%;
}

.action-button {
  display: block;
  margin: 0 auto;
  margin-top: 10px;
  padding: 10px 20px;
  font-size: 1.2em;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.action-button:hover {
  background-color: #0056b3;
}

.cancel-button {
  background-color: #dc3545;
}

.cancel-button:hover {
  background-color: #c82333;
}
</style>
