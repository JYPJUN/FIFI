<template>
  <div class="form-container">
    <h1>게시글 작성</h1>
    <form @submit.prevent="createArticle">
      <div class="form-group">
        <label for="title">제목:</label>
        <input type="text" v-model.trim="title" id="title" class="form-control">
      </div>
      <div class="form-group">
        <label for="content">내용:</label>
        <textarea v-model.trim="content" id="content" class="form-control" @input="autoResize"></textarea>
      </div>
      <div class="form-group">
        <label for="image">이미지:</label>
        <input type="file" @change="onFileChange" id="image" class="form-control">
        <div v-if="imageUrl" class="image-preview">
          <img :src="imageUrl" alt="Image Preview" />
        </div>
      </div>
      <input type="submit" value="제출" class="submit-button">
    </form>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useCustomerStore } from '@/stores/customer'
import { useArticleStore } from '@/stores/article'
import { useRouter } from 'vue-router';

const store = useCustomerStore()
const storeArticle = useArticleStore()
const router = useRouter();
const title = ref('');
const content = ref('');
const image = ref(null);
const imageUrl = ref(null);

const onFileChange = (e) => {
  const file = e.target.files[0];
  if (file) {
    image.value = file;
    imageUrl.value = URL.createObjectURL(file);
  } else {
    image.value = null;
    imageUrl.value = null;
  }
};

const createArticle = () => {
  const formData = new FormData();
  formData.append('title', title.value);
  formData.append('content', content.value);
  if (image.value) {
    formData.append('image', image.value);
  }

  axios({
    method: 'post',
    url: `${storeArticle.API_URL}/api/v1/articles/`,
    data: formData,
    headers: {
      Authorization: `Token ${store.token}`,
      'Content-Type': 'multipart/form-data',
    },
  })
  .then((response) => {
    router.push({ name: 'ArticleView' });
  })
  .catch((error) => {
    console.error(error.response.data);
  });
};

const autoResize = (event) => {
  const element = event.target;
  element.style.height = 'auto';
  element.style.height = element.scrollHeight + 'px';
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');

body {
  font-family: 'Noto Sans KR', sans-serif;
}

.form-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  /* box-shadow: 0 0 10px rgba(0,0,0,0.1); */
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: auto;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
  padding: 0 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: 'Noto Sans KR', sans-serif;
}

textarea.form-control {
  min-height: 500px;
  resize: none; /* Disable manual resizing */
}

.image-preview {
  margin-top: 10px;
}

.image-preview img {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.submit-button {
  width: 100%;
  padding: 10px;
  background-color: #383838;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-button:hover {
  background-color: #979393;
}
</style>
