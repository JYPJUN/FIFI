<template>
  <div class="detail-page-container">
    <div class="detail-page">
      <div v-if="article">
        <h1>{{ article.title }}</h1>
        <div class="article-header">
          <p>작성자 : <span class="author">{{ article.user.username }}</span></p>
          <p>작성시간 : <span class="date">{{ new Date(article.created_at).toLocaleString() }}</span></p>
        </div>
        <div class="article-content">
          <div style="text-align: center;">
            <img :src="`http://127.0.0.1:8000${article.image}`" alt="" style="max-height: 500px;">
          </div>
          <p class="content">{{ article.content }}</p>

          <div v-if="article.user.username === store.user" class="article-actions">
            <button @click="deleteArticle" class="btn-delete">삭제</button>  
            <RouterLink :to="{ name: 'UpdateView', params: { id: article.id } }" class="btn-update">수정</RouterLink>
          </div>
          
          <div class="like-section">
            <button :class="{ 'btn-like': true, 'liked': isLiked }" @click="likeArticle">
              {{ isLiked ? '💖' : '🤍' }}
            </button>
            <p class="like-count">{{ article.like_count }}</p>
          </div>
          <hr>
          <CommentForm @commentAdded="handleComment"/>
          <CommentList :comments="comments" @commentDel="handleComment" />
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import axios from 'axios'
import { onMounted, ref, computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useCustomerStore } from '@/stores/customer'
import { useArticleStore } from '@/stores/article'
import router from '@/router'
import CommentForm from '@/components/CommentForm.vue'
import CommentList from '@/components/CommentList.vue'

const store = useCustomerStore()
const storeArticle = useArticleStore()
const route = useRoute()
const article = ref(null)
const comments = ref([])

onMounted(() => {
  fetchArticle()
  fetchComments()
  store.getProfile()
  storeArticle.getLikedArticles()
})

const isLiked = computed(() => {
  return storeArticle.likedArticles.some(a => a.id === article.value?.id)
})

function fetchArticle() {
  const config = {
    method: 'get',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/`,
  }
  if (store.token) {
    config.headers = {
      Authorization: `Token ${store.token}`
    }
  }
  axios(config)
  .then(response => {
    article.value = response.data
  })
  .catch(error => {
    console.log(error)
  })
}

function fetchComments() {
  const config = {
    method: 'get',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/comments/`,
  }

  if (store.token) {
    config.headers = {
      Authorization: `Token ${store.token}`
    }
  }
  axios(config)
  .then(response => {
    comments.value = response.data
  })
  .catch(error => {
    console.log(error)
  })
}

function handleComment() {
  fetchComments()
}

function deleteArticle() {
  axios({
    method: 'delete',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/`,
    headers: {
      'Authorization': `Token ${store.token}`
    }
  })
  .then(() => {
    alert('게시글이 삭제되었습니다람쥐🐿')
    router.push({ name: 'ArticleView' })
  })
  .catch(error => {
    console.log(error)
  })
}

function likeArticle() {
  if (!store.token) {
    alert('로그인 해주세요.');
    return;
  }
  storeArticle.toggleLike(route.params.id).then(data => {
    if (article.value) {
      article.value.like_count = data.like_count;
      article.value.is_liked = data.is_liked;
    }
  });
}
console.log(article.like_count)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR&display=swap');

.detail-page-container {
  display: flex;
  justify-content: center;
  background-color: #f0f0f0;
  padding: 20px;
}

.detail-page {
  width: 1200px;
  padding: 20px;
  font-family: 'Noto Sans KR', sans-serif;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.article-content {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
}

.article-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  color: #555;
}

.article-header .author, 
.article-header .date {
  font-weight: lighter;
}

.title {
  margin: 20px 0;
  font-size: 24px;
  color: #333;
}

.content {
  margin-bottom: 20px;
  line-height: 1.6;
  color: #444;
}

.article-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.btn-delete, .btn-update {
  font-size: 0.9em; /* Smaller text size */
  padding: 5px 5px;
  margin-right: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background: none; /* Remove background color */
  color: rgb(165, 165, 165); /* Initial color for both buttons */
}

.btn-delete:hover, .btn-update:hover {
  color: rgb(63, 63, 63); /* Darker gray on hover */
}

.btn-update {
  text-decoration: none; /* Remove underline from update button */
}

.btn-update:hover, .btn-update:focus, .btn-update:active {
  text-decoration: none; /* Ensure no underline on hover, focus, or active */
}

.btn-like {
  font-size: 24px;
  border: none;
  background: none;
  cursor: pointer;
}

.like-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.like-count {
  font-size: 18px;
  color: #333;
}

hr {
  margin: 20px 0;
  border: 0;
  border-top: 1px solid #eee;
}

.comment-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.btn-delete-comment {
  background: none;
  border: none;
  cursor: pointer;
}

.btn-delete-comment img {
  width: 20px;
  height: 20px;
}
</style>