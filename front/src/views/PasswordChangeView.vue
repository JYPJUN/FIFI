<template>
  <div class="password-change-container">
    <form @submit.prevent="passwordChange" class="password-form">
      <div class="form-group">
        <label for="new_password1">변경할 비밀번호</label>
        <input type="password" id="new_password1" v-model.trim="new_password1" class="form-input">
      </div>
      <div class="form-group">
        <label for="new_password2">비밀번호 확인</label>
        <input type="password" id="new_password2" v-model.trim="new_password2" class="form-input">
      </div>
      <input type="submit" value="비밀번호 변경" class="submit-btn">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCustomerStore } from '@/stores/customer'

const new_password1 = ref('')
const new_password2 = ref('')
const store = useCustomerStore()

const passwordChange = function() {
  const payload = {
    new_password1: new_password1.value,
    new_password2: new_password2.value
  }
  store.passwordChange(payload)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');

.password-change-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
  background-color: #f9f9f9;
  font-family: 'Noto Sans KR', sans-serif;
}

.password-form {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 700;
  color: #333;
}

.form-input {
  width: 95%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.form-input:focus {
  border-color: #007BFF;
  outline: none;
}

.submit-btn {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  background-color: #007BFF;
  color: white;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.3s;
  width: 100%;
}

.submit-btn:hover {
  background-color: #0056b3;
}
</style>
