<template>
  <div class="container">
    <div class="article-grid">
      <ArticleListItem
        v-for="article in paginatedArticles"
        :key="article.id"
        :article="article"
      />
    </div>
    <div class="pagination">
      <button
        v-for="page in totalPages"
        :key="page"
        @click="setCurrentPage(page)"
        :class="{ active: currentPage === page }">
        {{ page }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import ArticleListItem from './ArticleListItem.vue';
import { useArticleStore } from '@/stores/article';

const storeArticle = useArticleStore();
const currentPage = ref(1);
const itemsPerPage = ref(16);

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
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  max-width: 1600px;
  width: 100%;
  min-height: 100vh; /* 컨테이너의 수직 크기가 줄어들지 않도록 설정 */
  margin: auto;
  padding: 20px;
  background: #f8f9fa;
}

.article-grid {
  display: flex;
  flex-wrap: wrap;
  align-items: start; /* Align items from the start */
  justify-content: flex-start; /* Start alignment of the cards */
  gap: 20px;
  width: 100%;
  margin-left: 200px;
}

.card {
  flex: 1 1 calc(20% - 0px); /* Update to fit 5 cards per row */
  max-width: calc(20% - 20px); /* Ensuring cards do not exceed this width */
  height: 400px;
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
</style>
