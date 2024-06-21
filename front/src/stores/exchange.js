import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useExchangeStore = defineStore('exchange', () => {

  const API_URL = 'http://127.0.0.1:8000'
  // 게시글 임시 데이터
  const exchangedetail = ref(null) // 환율 정보 저장
  
  //환율 정보
  const getExchange = function () { 
    return axios ({
      method: 'get',
      url: `${API_URL}/api/v1/exchange/`
    })
    .then(response => {
      exchangedetail.value = response.data
    })
    .catch(error => {
      console.log(error)
    })
  }

  return {  API_URL,
            getExchange, exchangedetail,
          }

  

},{persist:true})
