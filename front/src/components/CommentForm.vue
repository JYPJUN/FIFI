<template>
  <form @submit.prevent="submitComment" class="comment-form">
    <div class="input-group">
      <textarea v-model="newComment" placeholder="댓글을 입력하세요" class="comment-textarea"></textarea>
      <button type="submit" class="btn-submit-comment">댓글 작성</button>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { useCustomerStore } from '@/stores/customer'
import { defineEmits } from 'vue'

const emit = defineEmits(['commentAdded'])
const route = useRoute()
const store = useCustomerStore()
const newComment = ref('')
const router = useRouter()

function submitComment() {
  if (!store.token) {
    alert('로그인 해주세요.')
    router.push({name: 'LogInView'})
    return 
  }

  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/comments/`,
    headers: {
      'Authorization': `Token ${store.token}`
    },
    data: {
      content: newComment.value,
    }
  })
  .then((response) => {
    newComment.value = ''
    console.log(response.data)
    emit('commentAdded', response.data)
  })
  .catch(error => {
    console.log(error)
  })
}
</script>

<style scoped>
.comment-form {
  display: flex;
  justify-content: center;
  width: 100%;
  margin: 20px auto;
}

.input-group {
  display: flex;
  width: 100%;
  max-width: 600px;
}

.comment-textarea {
  flex: 1;
  padding: 10px;
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: none;
  height: 20px; /* Set the desired height here */
}

.btn-submit-comment {
  padding: 10px 20px;
  margin-left: 10px; /* Creates a gap between the textarea and the button */
  background-color: #1675F2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-family: 'Noto Sans KR', sans-serif;
  transition: background-color 0.3s;
}

.btn-submit-comment:hover {
  background-color: #125bb5;
}
</style>