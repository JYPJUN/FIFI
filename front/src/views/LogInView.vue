<template>
  <div class="login-container">
    <div class="login-box">
      <h1 class="logo-title">FIFI</h1>
      <p class="tagline">당신을 위한 금융상품 추천 서비스</p>
      <hr>
      <h1 class="login-title">로그인</h1>
      <form @submit.prevent="logIn" class="login-form">
        <div v-if="showAlert" class="alert">
          {{ alertMessage }}
        </div>
        <div class="form-group">
          <label for="username">아이디</label>
          <input type="text" id="username" v-model.trim="username" class="form-control">
        </div>
        
        <div class="form-group">
          <label for="password">비밀번호</label>
          <input type="password" id="password" v-model.trim="password" class="form-control">
        </div>

        <input type="submit" value="로그인" class="submit-btn">
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCustomerStore } from '@/stores/customer'

const username = ref(null)
const password = ref(null)
const store = useCustomerStore()

const alertMessage = ref("");
const showAlert = ref(false);

const logIn = async function() {
  const payload = {
    username: username.value,
    password: password.value
  }
  try {
    await store.logIn(payload);
  } catch (error) {
    alertMessage.value = '아이디와 비밀번호를 다시 확인해주세요';
    showAlert.value = true;
    setTimeout(() => {
      showAlert.value = false;
    }, 2000);
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  background-color: #f0f2f5;
}

.login-box {
  position: relative;
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.logo-title {
  font-family: "Noto Sans KR-Light", Helvetica;
  font-size: 2.5rem; /* 큰 사이즈 */
  margin-bottom: 0.5rem;
  color: #333;
}

.tagline {
  font-family: "Noto Sans KR-Light", Helvetica;
  font-size: 1rem; /* 일반 글씨체 크기 */
  margin-bottom: 1.5rem;
  color: #777;
}

.login-title {
  text-align: center;
  margin-bottom: 1rem;
  font-size: 2rem;
  color: #333;
}

.login-form .form-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

.login-form label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #555;
}

.login-form .form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
  box-sizing: border-box; /* 패딩과 테두리를 포함하여 너비를 계산 */
}

.login-form .form-control:focus {
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
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #f8d7da;
  color: #721c24;
  padding: 0.5rem;
  border: 1px solid transparent;
  border-radius: 0.25rem;
  border-color: #f5c6cb;
  width: calc(100% - 40px);
  box-sizing: border-box;
  text-align: center;
}
</style>
