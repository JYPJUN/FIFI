<template>
  <div class="container">
    <h1>금융회사</h1>
    <div class="company-grid">
      <div class="company-card" v-for="company in CompanyAll" :key="company.id">
        <img class="company-logo" alt="Element" :src="`/bank/${company.id}.png`" />
        <div class="company-info">
          <p class="company-name">{{ company.kor_co_nm }}</p>
          <p class="company-link"><a :href="company.homp_url" target="_blank">홈페이지 바로가기</a></p>
          <p class="company-contact">고객센터: {{ formatPhoneNumber(company.cal_tel) }}</p>
        </div>
        <button class="like-button" @click="toggleLike(company.id)">
          <span v-if="likecompany.includes(company.id)">💖</span>
          <span v-else>🤍</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useProductStore } from '@/stores/product';
import { useCustomerStore } from '@/stores/customer';
import { ref, onMounted } from 'vue';
import axios from 'axios';

const store = useProductStore();
const user = useCustomerStore();
const API_URL = 'http://127.0.0.1:8000';

const CompanyAll = ref([]);
const likecompany = ref([]);

// 휴대폰 넘버 수정하기
const formatPhoneNumber = function (phoneNumber) {
  if (phoneNumber.length === 8) {
    return phoneNumber.replace(/(\d{4})(\d{4})/, '$1-$2');
  }
  return phoneNumber;
};

// 클릭 시 좋아요 버튼
const toggleLike = function (companyId) {
  axios({
    method: 'post',
    url: `${API_URL}/api/v1/products/${companyId}/likes/`,
    headers: { Authorization: `Token ${user.token}` },
  })
    .then(response => {
      if (likecompany.value.includes(companyId)) {
        likecompany.value = likecompany.value.filter(id => id !== companyId);
      } else {
        likecompany.value.push(companyId);
      }
    })
    .catch(error => {
      console.log(error);
    });
};

// 전체 리스트 회사 좋아요 여부 확인하기
const CheckLikeCompany = function () {
  return axios({
    method: 'get',
    url: `${API_URL}/api/v1/products/company/likes/`,
    headers: { Authorization: `Token ${user.token}` },
  })
    .then(response => {
      // 좋아요한 회사의 ID만 추출하여 likecompany 배열에 저장
      likecompany.value = response.data.map(company => company.id);
    })
    .catch(error => {
      console.log(error);
    });
};

onMounted(() => {
  store.getCompany().then(() => {
    CompanyAll.value = store.companydall;
  });
  CheckLikeCompany();
});
</script>



<style scoped>
.container {
  display: flex;
  flex-direction: column;
  width: 1200px;
}

.company-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
  margin-bottom: 16px;
}

.company-card {
  width: calc(25% - 16px);
  min-width: 200px;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  position: relative; /* 좋아요 버튼 위치 설정을 위해 */
}

.company-logo {
  width: 80px;
  height: 80px;
  object-fit: contain;
  margin-bottom: 8px;
}

.company-info {
  text-align: left;
}

.company-name {
  font-weight: bold;
  margin-bottom: 8px;
}

.company-link a {
  color: #007bff;
  text-decoration: none;
}

.company-link a:hover {
  text-decoration: underline;
}

.company-contact {
  color: #666;
}

.like-button {
  background: none;
  border: none;
  color: #ff0000;
  font-size: 1.2em;
  cursor: pointer;
  position: absolute;
  top: 16px;
  right: 16px;
}

.like-button:hover {
  color: #ff6666;
}
</style>
