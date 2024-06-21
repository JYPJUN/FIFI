import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useCustomerStore } from './customer';

export const useArticleStore = defineStore('article', () => {
  const customerStore = useCustomerStore();
  const API_URL = 'http://127.0.0.1:8000'
  const likedArticles = ref([]); // 좋아요를 클릭한 게시글 데이터
  const articles = ref([])
  
   // Article
   const getArticles = function() {
    const config = {
      method: 'get',
      url: `${API_URL}/api/v1/articles/`
    };
  
    // Only add Authorization header if the user is logged in
    // if (customerStore.token) {
    //   config.headers = {
    //     Authorization: `Token ${customerStore.token}`
    //   };
    // }
    axios(config)
    .then(response => {
      articles.value = response.data;
    })
    .catch((error) => {
      console.log(error);
    });
  }
  
   // 좋아요 순으로 게시글 가져오기 함수 추가
   const getArticlesByLikes = function() {
    const config = {
      method: 'get',
      url: `${API_URL}/api/v1/articles/byliked/`
    }

    // if (customerStore.token) {
    //   config.headers = {
    //     Authorization: `Token ${customerStore.token}`
    //   }
    // }
    axios(config)
      .then(response => {
        articles.value = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }

  // 내가 작성한 게시글 조회 함수
  const getMyArticles = function() {
    const config = {
      method: 'get',
      url: `${API_URL}/api/v1/articles/myarticles/`
    };
  
    // Only add Authorization header if the user is logged in
    if (customerStore.token) {
      config.headers = {
        Authorization: `Token ${customerStore.token}`
      };
    }
    axios(config)
    .then(response => {
      articles.value = response.data;
    })
    .catch((error) => {
      console.log(error);
    });
  }


  // 좋아요를 클릭한 게시글
  const getLikedArticles = function() {
    if (!customerStore.token) {
      console.log('User is not authenticated');
      return;
    }

    const config = {
      method: 'get',
      url: `${API_URL}/api/v1/articles/liked_articles/`,
      headers: {
        Authorization: `Token ${customerStore.token}`
      }
    };

    axios(config)
      .then(response => {
        likedArticles.value = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  }

  const toggleLike = function(articleId) {
    if (!customerStore.token) {
      console.error('User is not authenticated');
      return;
    }
  
    const config = {
      method: 'post',
      url: `${API_URL}/api/v1/articles/${articleId}/likes/`,
      headers: { Authorization: `Token ${customerStore.token}` }
    };
  
    return axios(config)
      .then(response => {
        const index = articles.value.findIndex(article => article.id === articleId);
        if (index !== -1) {
          articles.value[index].like_count = response.data.like_count;
          articles.value[index].is_liked = response.data.is_liked;
        }
        getLikedArticles();
        return response.data;
      })
      .catch(error => {
        console.error('Error toggling like:', error);
      });
  }
  return {  API_URL,articles, likedArticles, 
          getArticlesByLikes ,getLikedArticles, toggleLike, getArticles,
          getMyArticles,
          }

  

},{persist:true})
