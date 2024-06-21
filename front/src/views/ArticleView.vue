<template>
  <div class="view-container">
    <div style="width: 1500px;">
    <!-- 로그인해야 게시글 생성 가능 -->
    <RouterLink v-if="store.isLoggin" :to="{name:'CreateView'}" class="create-article-button">
      새 글 작성
    </RouterLink>
    <hr>
    <div class="nav-buttons-container">
    <RouterLink :to="{name: 'ArticleView'}" class="nav-button" :class="{ 'active-link': $route.name === 'ArticleView' }">최신순</RouterLink>
    <RouterLink :to="{name: 'TrendArticleView'}" class="nav-button" :class="{ 'active-link': $route.name === 'TrendArticleView' }">트렌드</RouterLink>
    <RouterLink :to="{name: 'MyArticleView'}" class="nav-button" :class="{ 'active-link': $route.name === 'MyArticleView' }">내가 쓴 글</RouterLink>
  </div>
    <ArticleList />
  </div>
</div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useArticleStore } from '@/stores/article';
import { useCustomerStore } from '@/stores/customer';
import { RouterLink } from 'vue-router';
import ArticleList from '@/components/ArticleList.vue';
// import TrendArticleView from '@/views/TrendArticleView.vue';

const store = useCustomerStore();
const storeArticle = useArticleStore();

onMounted(() => {
  storeArticle.getArticles();
});

</script>

<style scoped>
.view-container {
  display: flex;
  flex-direction: column;
  align-items: center; /* This centers the ArticleList */
  width: 100%; /* Ensures the container takes full width */
  padding-top: 60px; /* Provide space for the button */
}

.create-article-button {
  right: calc((100% - 1600px) / 2); /* Aligns button to the right end of the 1600px container */
  top: 10px; /* Position above the articles list */
  padding: 10px 20px;
  background-color: #383838;
  color: white;
  text-decoration: none;
  border-radius: 100px;
  text-align: center;
  display: inline-block;
}

.create-article-button:hover {
  background-color: #979393;
}

.nav-buttons-container {
  align-self: flex-start; 
  margin-bottom: 10px; /* 아래쪽 여백 */
}

.nav-button {
  margin-right: 10px; /* 우측 마진 */
  padding: 5px 10px;
  color: #888; /* 회색 */
  text-decoration: none;
  text-align: center;
}

.nav-button:hover {
  color: #555; /* 더 진한 회색 */
}

.active-link {
  color: black; /* existing style to set the link color to black */
  font-weight: bold; /* make the text bold */
}
</style>
