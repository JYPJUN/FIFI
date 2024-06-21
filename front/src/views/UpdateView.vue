<template>
  <div class="form-container">
    <h1>게시글 수정</h1>
    <div v-if="article">
      <form @submit.prevent="updateArticle">
        <div class="form-group">
          <label for="title">제목:</label>
          <input id="title" v-model="editTitle" type="text" class="form-control">
        </div>
        <div class="form-group">
          <label for="content">내용:</label>
          <textarea id="content" v-model="editContent" class="form-control"></textarea>
        </div>
        <div class="button-group">
          <button type="submit" class="btn btn-primary">수정하기</button>
          <button type="button" @click="cancelUpdate" class="btn btn-secondary">취소</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCustomerStore } from '@/stores/customer';

const store = useCustomerStore();
const route = useRoute();
const router = useRouter();
const article = ref(null);
const editTitle = ref('');
const editContent = ref('');

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/`,
    headers: {
      'Authorization': `Token ${store.token}`
    }
  }).then(response => {
    article.value = response.data;
    editTitle.value = article.value.title;
    editContent.value = article.value.content;
  }).catch(error => {
    console.error('게시글을 불러오는데 실패했습니다.', error);
  });
});

function updateArticle() {
  axios({
    method: 'put',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/`,
    headers: {
      'Authorization': `Token ${store.token}`
    },
    data: {
      title: editTitle.value,
      content: editContent.value
    }
  }).then(() => {
    alert('게시글이 수정되었습니다.');
    router.push({ name: 'DetailView' });
  }).catch(error => {
    console.error('게시글 수정 실패', error);
  });
}

function cancelUpdate() {
  router.back();
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');

body {
  font-family: 'Noto Sans KR', sans-serif;
}

.form-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #555;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: 'Noto Sans KR', sans-serif;
}

textarea.form-control {
  height: 200px;
  resize: vertical;
}

.button-group {
  display: flex;
  justify-content: space-between;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  font-family: 'Noto Sans KR', sans-serif;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
