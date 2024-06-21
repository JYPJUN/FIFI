<!-- MyArticleView.vue -->
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
import { onMounted, ref, computed } from 'vue';
import ArticleList from '@/components/ArticleList.vue';
import { useArticleStore } from '@/stores/article';
import { useCustomerStore } from '@/stores/customer';
import { RouterLink } from 'vue-router';

const store = useCustomerStore();
const storeArticle = useArticleStore();
const currentPage = ref(1);
const itemsPerPage = ref(10);

const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return storeArticle.articles.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(storeArticle.articles.length / itemsPerPage.value);
});

function setCurrentPage(page) {
  currentPage.value = page;
}

// 페이지가 마운트될 때 내가 작성한 게시글 가져오기
onMounted(() => {
  storeArticle.getMyArticles();
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

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  max-width: 1600px;
  width: 100%;
  min-height: 100vh; /* Ensures the container's vertical size doesn't shrink */
  margin: auto;
  padding: 20px;
  background: #f8f9fa;
}

.article-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  gap: 10px;
  width: 100%;
}

.pagination {
  display: flex;
  gap: 10px;
  padding-top: 20px;
}

.pagination button {
  padding: 5px 10px;
  border: 1px solid #ccc;
  background: white;
  cursor: pointer;
}

.pagination button.active {
  background-color: #007BFF;
  color: white;
  border-color: #007BFF;
}

.active-link {
  color: black; /* existing style to set the link color to black */
  font-weight: bold; /* make the text bold */
}
</style>
