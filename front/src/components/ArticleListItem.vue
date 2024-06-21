<template>
  <div class="cards-container">
    <RouterLink :to="{ name: 'DetailView', params: { id: article.id } }" class="no-decoration">
      <div class="card">
        <img v-if="article.image" :src="`http://127.0.0.1:8000${article.image}`" alt="Article Image">
        <img v-else :src="`http://127.0.0.1:8000/media/article_image/article_basic.png`" alt="Default Image">
        <div class="content">
          <h3>{{ article.title }}</h3>
          <p>{{ article.content }}</p>
          <p> 💬  {{ article.comment_count }}</p>
          <p class="date">{{ article.created_at }}</p>
          <hr>
          <div class="user-info">
            <p v-if="article.user" class="username">by {{ article.user.username }}</p>
            <p> ❤ {{ article.like_count }}</p>
          </div>
        </div>
      </div>
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
defineProps({
  article: Object
})
</script>

<style scoped>
.no-decoration {
  text-decoration: none;
  color: inherit;
}

.card {
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  transition: transform 0.3s;
  cursor: pointer;
  background: #fff;
  width: 300px;
  height: 400px;
}

.card:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0,0,0,0.2);
}

.card img {
  width: 100%;
  height: 160px;
  object-fit: cover;
}

.content {
  padding: 10px;
  flex-grow: 1;
  overflow: hidden;
}

.user-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

hr {
  border: 0;
  height: 1px;
  background: #eee;
}

.date {
  font-size: 0.8em;
  color: #666666;
}

.username {
  font-weight: normal;
  color: black;
}
</style>