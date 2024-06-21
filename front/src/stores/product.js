import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useProductStore = defineStore('product', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const companydall = ref(null) // 회사 정보 저장
  // 금융 예금 정보
  const productall = ref(null) // 금융 예금 정보 저장
  const optionall = ref(null) // 금융 예금 정보 옵션 저장
  const optiondetail = ref(null) // 금융 예금 정보 옵션 저장 세부정보

  // 금융 적금 정보
  const savingall = ref(null) // 금융 적금 정보 저장
  const savingoptionall = ref(null) // 금융 적금 정보 옵션 저장
  const savingoptiondetail = ref(null) // 금융 적금 정보 옵션 저장 세부정보
  
  // 회사 정보
  const getCompany = function () {
    return axios ({
      method : 'get',
      url : `${API_URL}/api/v1/products/`
    })
    .then(response => {
      companydall.value = response.data
    })
    .catch(error => {
      console.log(error)
    })
  }

  // 상품 정보
  const getProduct = function () {
    return axios ({
      method : 'get',
      url : `${API_URL}/api/v1/products/getTimeDepogit`
    })
    .then(response => {
      productall.value = response.data
    })
    .catch(error => {
      console.log(error)
    })
  }
  
  // 옵션 정보
  const getProductOption = function () {
    return axios ({
      method : 'get',
      url : `${API_URL}/api/v1/products/getTimeDepogitOption`
    })
    .then(response => {
      optionall.value = response.data
    })
    .catch(error => {
      console.log(error)
    })
  }

  // 옵션 세부 정보
  const getProductOptionDetail = function (fin_prdt_cd) {
    return axios ({
      method : 'get',
      url : `${API_URL}/api/v1/products/getTimeDepogitOption/${fin_prdt_cd}/`
    })
    .then(response => {
      optiondetail.value = response.data
    })
    .catch(error => {
      console.log(error)
    })
  }

  // 상품 정보
  const getSaving = function () {
    return axios ({
      method : 'get',
      url : `${API_URL}/api/v1/products/getSaving/`
    })
    .then(response => {
      savingall.value = response.data
    })
    .catch(error => {
      console.log(error)
    })
  }
  
  // 옵션 정보
  const getSavingOption = function () {
    return axios ({
      method : 'get',
      url : `${API_URL}/api/v1/products/getSavingOption/`
    })
    .then(response => {
      savingoptionall.value = response.data
    })
    .catch(error => {
      console.log(error)
    })
  }

  // 옵션 세부 정보
  const getSavingOptionDetail = function (fin_prdt_cd) {
    return axios ({
      method : 'get',
      url : `${API_URL}/api/v1/products/getSavingOption/${fin_prdt_cd}/`
    })
    .then(response => {
      savingoptiondetail.value = response.data
    })
    .catch(error => {
      console.log(error)
    })
  }

  return {  getCompany, companydall,
            getProduct, productall,
            getProductOption, optionall,
            getProductOptionDetail, optiondetail,
            getSaving, savingall,
            getSavingOption, savingoptionall,
            getSavingOptionDetail, savingoptiondetail,
            }

},{persist:true})
