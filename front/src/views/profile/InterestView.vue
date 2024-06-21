<template>
  <div class="container">
    
    <div class="view-toggle">
      <label>
        <input type="checkbox" v-model="isProfileView" />
        <span>{{ isProfileView ? '프로필' : '관심' }}</span>
      </label>
    </div>

    <div v-if="!isProfileView" class="interest-view">
      <h1>좋아요한 게시글</h1>
      <div v-if="!likedArticles || likedArticles.length === 0">
        <p>좋아요 한 게시글이 없습니다</p>
      </div>
      <div v-else>
        <div class="article-cards">
          <div v-for="article in likedArticles" :key="article.id" class="article-card">
            <div class="article-content">
              <h2>{{ article.title }}</h2>
              <p>{{ article.content }}</p>
              <div v-if="article.image" class="article-image-container">
                <img :src="article.image" alt="Article image" class="article-image"/>
              </div>
              <p>Likes: {{ article.like_count }}</p>
              <p>Comments: {{ article.comment_count }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isProfileView" class="profile-view">
      <h1 class="profile-header">Profile</h1>
      <div class="profile-container">
        <div v-if="detail" class="profile-details">
          <div class="profile-image-container">
            <img :src="`${detail.profile_img}?${new Date().getTime()}`" class="profile-image" alt="프로필 이미지">
          </div>
          <div class="profile-info">
            <p class="info-item"><span class="label">유저 아이디:</span> {{ detail.username }}</p>
            <p class="info-item"><span class="label">유저 이름:</span> {{ detail.name }}</p>
            <p class="info-item"><span class="label">이메일:</span> {{ detail.email }}</p>
            <p class="info-item"><span class="label">생일:</span> {{ detail.birth_date }}</p>
          </div>
          <RouterLink :to="{ name: 'ProfileUpdateView', params: { id: detail.pk } }" class="update-link">수정</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { useCustomerStore } from '@/stores/customer';
import { useArticleStore } from '@/stores/article';
import { onMounted, ref, watchEffect } from 'vue';

export default {
  name: 'InterestView',
  setup() {
    const isProfileView = ref(false);
    const store = useCustomerStore();
    const storeArticle = useArticleStore();
    const detail = ref(null);

    watchEffect(() => {
      detail.value = store.userdetail;
    });

    onMounted(() => {
      storeArticle.getLikedArticles();
      store.getProfile().then(() => {
        detail.value = store.userdetail;
      });
    });

    return {
      likedArticles: storeArticle.likedArticles,
      detail,
      isProfileView,
    };
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.view-toggle {
  display: inline-flex;
  align-items: center;
  margin-bottom: 20px;
}

label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

input[type="checkbox"] {
  appearance: none;
  position: relative;
  border: 2px solid gray;
  border-radius: 1.25em;
  width: 2.25em;
  height: 1.25em;
  background: transparent;
  outline: none;
  cursor: pointer;
  transition: background-color 250ms linear, border-color 250ms linear;
  vertical-align: middle;
}

input[type="checkbox"]::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 2px;
  width: 1em;
  height: 1em;
  border-radius: 50%;
  background-color: gray;
  transform: translateY(-50%);
  transition: left 250ms linear, background-color 250ms linear;
}

input[type="checkbox"]:checked {
  background-color: tomato;
  border-color: tomato;
}

input[type="checkbox"]:checked::before {
  background-color: white;
  left: calc(100% - 1em - 2px);
}

input[type="checkbox"]:focus-visible {
  outline: 2px solid tomato;
}

input[type="checkbox"]:enabled:hover {
  box-shadow: 0 0 0 4px lightgray;
}

.profile-view, .interest-view {
  width: 90%;
  max-width: 600px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

h1 {
  margin-bottom: 20px;
}

.profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.profile-header {
  text-align: center;
  color: #333;
  font-family: "Noto Sans KR-Bold", Helvetica, sans-serif;
  font-size: 24px;
  font-weight: 700;
}

.profile-details {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-info {
  width: 100%;
  text-align: center;
  margin-bottom: 20px;
}

.info-item {
  margin: 8px 0;
  font-family: "Noto Sans KR-Regular", Helvetica, sans-serif;
  font-size: 16px;
}

.label {
  font-weight: 700;
  color: #555;
}

.profile-image-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.update-link {
  display: inline-block;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-weight: bold;
}

.update-link:hover {
  background-color: #45a049;
}

.article-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.article-card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: calc(33.333% - 20px); /* Adjust width to fit 3 items per row with the given gap */
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  cursor: pointer;
}

.article-card:hover {
  background-color: #f9f9f9;
}

.article-content {
  width: 100%;
}

@media (max-width: 1024px) {
  .article-card {
    width: calc(50% - 20px); /* Adjusts to 2 items per row on smaller screens */
  }
}

@media (max-width: 768px) {
  .article-card {
    width: 100%; /* Full width on very small screens */
  }
}

.article-image-container {
  margin: 10px 0;
}

.article-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}
</style>
