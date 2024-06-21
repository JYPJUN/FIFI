<template>
  <div>
    <h3>댓글 목록</h3>
    <div v-for="comment in comments" :key="comment.id" class="comment-container">
      <div class="comment-content">
        <h5>{{ comment.user.username }}</h5>
        <p>{{ comment.content }}</p>
      </div>
      <button
        v-if="comment.user.username == store.user"
        @click="deleteComment(comment.id)"
        class="btn-delete-comment"
      >
        <img src="@/assets/trash-icon.png" alt="Delete">
      </button>
      <hr class="comment-divider">
    </div>
  </div>
</template>


<script setup>
import { ref, onBeforeUpdate } from 'vue'
import axios from 'axios'
import { useCustomerStore } from '@/stores/customer'

const store = useCustomerStore()
const comments = ref([])

const props = defineProps({
  comments: Array
})

const emit = defineEmits(['commentDel'])

function deleteComment(commentId) {
  axios({
    method: 'delete',
    url: `${store.API_URL}/api/v1/articles/comments/${commentId}/`,
    headers: {
      'Authorization': `Token ${store.token}`
    }
  })
  .then(() => {
    emit('commentDel')
  })
  .catch(error => {
    console.error(error)
  })
}

onBeforeUpdate(() => {
  comments.value = props.comments
})
</script>

<style scoped>
.comment-container {
  position: relative;
  margin-bottom: 20px;
}

.comment-content {
  flex: 1;
}

.divider-container {
  display: flex;
  align-items: center;
  position: relative;
}

.btn-delete-comment {
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.3s;
  margin-left: 10px;
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
}

.btn-delete-comment img {
  width: 20px;
  height: 20px;
  filter: brightness(0) saturate(100%) invert(41%) sepia(0%) saturate(0%) hue-rotate(204deg) brightness(91%) contrast(88%);
}

.btn-delete-comment:hover img {
  filter: brightness(0) saturate(100%) invert(27%) sepia(78%) saturate(4145%) hue-rotate(202deg) brightness(95%) contrast(89%);
}

.comment-divider {
  flex: 1;
  border: none;
  height: 1px;
  background-color: #ccc;
  margin: 5px 0;
}
</style>