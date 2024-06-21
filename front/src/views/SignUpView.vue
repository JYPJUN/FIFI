<template>
  <div class="signup-container">
    <div class="signup-box">
      <h1 class="signup-title">회원가입</h1>
      <form @submit.prevent="signUp" class="signup-form">
        <div v-if="showAlert" class="alert">
          {{ alertMessage }}
        </div>
        
        <div class="form-group">
          <label for="username">아이디</label>
          <input type="text" id="username" v-model.trim="username" class="form-control" required />
        </div>
        
        <div class="form-group">
          <label for="password1">비밀번호</label>
          <input type="password" id="password1" v-model.trim="password1" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="password2">비밀번호 확인</label>
          <input type="password" id="password2" v-model.trim="password2" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="name">이름</label>
          <input type="text" id="name" v-model="name" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="birth_date">생년월일</label>
          <input type="date" id="birth_date" v-model="birth_date" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="email">이메일</label>
          <input type="email" id="email" v-model="email" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="nickname">닉네임</label>
          <input type="text" id="nickname" v-model="nickname" class="form-control" required />
        </div>

        <input type="submit" value="회원가입" class="submit-btn">
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useCustomerStore } from '@/stores/customer'

const API_URL = 'http://127.0.0.1:8000'

const username = ref(null) 
const password1 = ref(null)
const password2 = ref(null)
const birth_date = ref(null)
const email = ref(null)
const nickname = ref(null)
const name = ref(null)
const store = useCustomerStore()

const alertMessage = ref("");
const showAlert = ref(false);

const signUp = async function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    birth_date: birth_date.value,
    email: email.value,
    nickname: nickname.value,
    name: name.value,
  }

  axios({
    method: 'post',
    url: `${API_URL}/accounts/signup/`,
    data: payload
  })
  .then(response => {
    store.logIn({ username: username.value, password: password1.value });
  })
  .catch(error => {
    if (error.response && error.response.data) {
      const data = error.response.data;
      if (data.username) {
        alertMessage.value = `해당 아이디는 이미 존재합니다.`;
      } else if (data.password1) {
        alertMessage.value = `비밀번호 오류: ${data.password1[0]}`;
      } else if (data.password2) {
        alertMessage.value = `비밀번호 확인 오류: ${data.password2[0]}`;
      } else if (data.email) {
        alertMessage.value = `이메일 오류: ${data.email[0]}`;
      } else if (data.nickname) {
        alertMessage.value = `닉네임 오류: ${data.nickname[0]}`;
      } else if (data.non_field_errors) {
        alertMessage.value = data.non_field_errors[0];
      } else {
        alertMessage.value = "해당 닉네임은 이미 존재합니다.";
      }
    } else {
      alertMessage.value = "서버와 연결할 수 없습니다.";
    }
    showAlert.value = true;
    setTimeout(() => {
      showAlert.value = false;
    }, 2000);
  });
}
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}

.signup-box {
  position: relative;
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.signup-title {
  text-align: center;
  margin-bottom: 1rem;
  font-size: 2rem;
  color: #333;
}

.signup-form .form-group {
  margin-bottom: 1.5rem;
}

.signup-form label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #555;
}

.signup-form .form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
  box-sizing: border-box; /* 패딩과 테두리를 포함하여 너비를 계산 */
}

.signup-form .form-control:focus {
  border-color: #1675f2;
  outline: none;
}

.submit-btn {
  width: 100%;
  padding: 0.5rem; /* 입력 필드와 동일한 패딩 */
  border: none;
  border-radius: 5px;
  background-color: #1675f2;
  color: white;
  font-size: 1.25rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  box-sizing: border-box; /* 패딩과 테두리를 포함하여 너비를 계산 */
}

.submit-btn:hover {
  background-color: #125bb5;
}

.alert {
  position: absolute; /* 절대 위치로 설정 */
  top: -20px; /* 부모 요소 위로 20px 이동 */
  left: 50%; /* 수평 중앙 정렬 */
  transform: translateX(-50%); /* 중앙 정렬 보정 */
  background-color: #f8d7da;
  color: #721c24;
  padding: 0.5rem; /* 패딩을 줄여서 높이 감소 */
  border: 1px solid transparent;
  border-radius: 0.25rem;
  border-color: #f5c6cb;
  width: calc(100% - 40px); /* 좌우 여백 고려하여 너비 설정 */
  box-sizing: border-box;
  text-align: center;
}
</style>
