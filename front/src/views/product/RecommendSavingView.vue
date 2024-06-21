<template>
  <div class="container">
    <h1 style="text-align: center;">적금 추천</h1>
    <h4 style="position: relative; left: 30px;">⁕ 금융 상품 추천은 나이, 연봉, 회사 선호도, 상품 가입 유저 기준으로 산출됩니다.</h4>
    <table style="margin: 30px;">
      <thead>
        <tr>
          <th @click="sortBy('saving_company')">
            금융상품명
            <span v-if="currentSort === 'saving_company'">
              <i :class="currentSortDir === 'asc' ? 'arrow up' : 'arrow down'"></i>
            </span>
          </th>
          <th @click="sortBy('saving_name')">
            금융회사명
            <span v-if="currentSort === 'saving_name'">
              <i :class="currentSortDir === 'asc' ? 'arrow up' : 'arrow down'"></i>
            </span>
          </th>
          <th @click="sortBy('age')">
            나이 비중
            <span v-if="currentSort === 'age'">
              <i :class="currentSortDir === 'asc' ? 'arrow up' : 'arrow down'"></i>
            </span>
          </th>
          <th @click="sortBy('income')">
            연봉 비중
            <span v-if="currentSort === 'income'">
              <i :class="currentSortDir === 'asc' ? 'arrow up' : 'arrow down'"></i>
            </span>
          </th>
          <th @click="sortBy('preference')">
            회사 선호도 비중
            <span v-if="currentSort === 'preference'">
              <i :class="currentSortDir === 'asc' ? 'arrow up' : 'arrow down'"></i>
            </span>
          </th>
          <th @click="sortBy('user_count')">
            가입 유저 비중
            <span v-if="currentSort === 'user_count'">
              <i :class="currentSortDir === 'asc' ? 'arrow up' : 'arrow down'"></i>
            </span>
          </th>
          <th @click="sortBy('total_score')">
            총 점수
            <span v-if="currentSort === 'total_score'">
              <i :class="currentSortDir === 'asc' ? 'arrow up' : 'arrow down'"></i>
            </span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="record in sortedRecords" :key="record.id" @click="goToDetail(record.id)">
          <td>{{ record.saving_name }}</td>
          <td>{{ record.saving_company }}</td>
          <td>{{ formatValue(record.age) }}</td>
          <td>{{ formatValue(record.income) }}</td>
          <td>{{ formatValue(record.preference) }}</td>
          <td>{{ formatValue(record.user_count) }}</td>
          <td>{{ formatValue(record.total_score) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
import { useCustomerStore } from '@/stores/customer';
import { useRouter } from 'vue-router';

const API_URL = 'http://127.0.0.1:8000';

export default {
  data() {
    return {
      records: [],
      currentSort: 'total_score',
      currentSortDir: 'desc'
    };
  },
  created() {
    this.fetchRecords();
  },
  methods: {
    fetchRecords() {
      const store = useCustomerStore();
      axios.get(`${API_URL}/api/v1/products/saving/getrecommendproduct/`, {
        headers: { Authorization: `Token ${store.token}` }
      })
      .then(response => {
        this.records = response.data;
      })
      .catch(error => {
        console.error('Error fetching records:', error);
      });
    },
    sortBy(key) {
      if (this.currentSort === key) {
        this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
      } else {
        this.currentSort = key;
        this.currentSortDir = 'asc';
      }
    },
    goToDetail(id) {
      this.$router.push({ name: 'SavingDetailView', params: { id } });
    },
    formatValue(value) {
      return Number(value).toFixed(2);
    }
  },
  computed: {
    sortedRecords() {
      return this.records.slice().sort((a, b) => {
        let modifier = 1;
        if (this.currentSortDir === 'desc') modifier = -1;
        if (a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
        if (a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        return 0;
      });
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  width: 100%;
  width: 1200px;
  margin: 0 auto;
}

table {
  border-collapse: collapse;
  margin: 20px 0;
  text-align: center;
}

thead th {
  background-color: #f2f2f2;
  cursor: pointer;
  position: relative;
  user-select: none;
}

thead th:hover {
  background-color: #e0e0e0;
}

th, td {
  border: 1px solid #dddddd;
  padding: 12px 15px;
}

tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

tbody tr:hover {
  background-color: #f1f1f1;
}

.arrow {
  display: inline-block;
  margin-left: 5px;
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
}

.arrow.up {
  border-bottom: 6px solid black;
}

.arrow.down {
  border-top: 6px solid black;
}
</style>
