<template>
  <div class="profile-update-container">
    <h1 class="profile-update-header">프로필 수정</h1>
    <img :src="form.profile_img_url" class="profile-image-preview" alt="프로필 이미지 미리보기" v-if="form.profile_img_url"/>
    <form @submit.prevent="updateProfile">
    <div class="form-group">
      <label for="profile_img">프로필 이미지:</label>
      <input type="file" @change="onFileChange" id="profile_img" />
    </div>
    <div class="form-group">
      <label for="name">유저 이름:</label>
      <input type="text" v-model="form.name" id="name" />
    </div>
      <div class="form-group">
        <label for="username">유저 아이디:</label>
        <input type="text" v-model="form.username" id="username" disabled />
      </div>
      <div class="form-group">
        <label for="email">이메일:</label>
        <input type="email" v-model="form.email" id="email" disabled />
      </div>
      <div class="form-group">
        <label for="birth_date">생일:</label>
        <input type="date" v-model="form.birth_date" id="birth_date" disabled/>
      </div>
      <div class="form-group">
        <label for="income">연봉:</label>
        <input type="text" v-model="form.income" id="income">
        <small class="form-text text-muted"> - 만원 단위로 입력해주세요</small>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn">수정</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCustomerStore } from '@/stores/customer'

const store = useCustomerStore()
const route = useRoute()

const form = ref({
  username: '',
  name: '',
  email: '',
  birth_date: '',
  profile_img: null,
  profile_img_url: '',
  income: '',
})

onMounted(async () => {
  await store.getProfile()
  const detail = store.userdetail
  if (detail) {
    form.value = {
      username: detail.username,
      name: detail.name,
      email: detail.email,
      birth_date: detail.birth_date,
      profile_img: null,
      profile_img_url: detail.profile_img,
      income: detail.income,  // 소득 필드 초기화
    }
  }
})

const onFileChange = (e) => {
  const file = e.target.files[0]
  form.value.profile_img = file
  form.value.profile_img_url = URL.createObjectURL(file)
}

const updateProfile = async () => {
  const formData = new FormData()
  formData.append('name', form.value.name)
  formData.append('email', form.value.email)
  formData.append('birth_date', form.value.birth_date)
  formData.append('income', form.value.income)  // 소득 필드 추가
  if (form.value.profile_img) {
    formData.append('profile_img', form.value.profile_img)
  }

  try {
    await store.updateProfile(formData, route.params.id)
    await store.getProfile()  // Refresh profile data after update
  } catch (error) {
    console.error('프로필 업데이트 실패:', error)
  }
}
</script>

<style scoped>

.form-text {
  font-size: 0.875rem; /* 작은 글씨 크기 */
  color: #6c757d; /* 중간 회색 */
}

.profile-update-container {
  max-width: 800px;
  margin: auto;
  padding: 30px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(0,0,0,0.1);
}

.profile-update-header {
  text-align: center;
  margin-bottom: 20px;
  color: #495057;
  font-size: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.profile-image-preview {
  max-width: 200px;
  max-height: 200px;
  display: block;
  margin: 10px auto 20px;
  border-radius: 100%;
}

input[type="file"], input[type="text"], input[type="email"], input[type="date"] {
  width: calc(100% - 10px);
  margin: 5px;
  padding: 8px 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  transition: border-color .15s ease-in-out, box-shadow .15s ease-in-out;
}

input:focus {
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
}

.form-actions {
  text-align: center; /* Center the button inside this container */
}

.btn {
  width: 50%; /* Increase button width */
  padding: 10px 0; /* Better padding for touch interaction */
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color .15s ease-in-out; /* Smooth transition for hover effect */
}

.btn:hover {
  background-color: #0056b3;
}
</style>
