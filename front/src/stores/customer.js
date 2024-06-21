import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCustomerStore = defineStore('customer', () => {
  const token = ref(null)
  const API_URL = 'http://127.0.0.1:8000'
  const user = ref(null)
  const userdetail = ref(null)
  const router = useRouter()
  const isLoggin = ref(false)
  
  const logIn = async function(payload) {
    const username = payload.username
    const password = payload.password
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/accounts/login/`,
        data: {
          username, password
        }
      })
      token.value = response.data.key
      user.value = payload.username
      await getProfile()
      isLoggin.value = true
      router.push({ name: 'HomeView' })
    } catch (error) {
      if (error.response && error.response.data) {
        const data = error.response.data
        if (data.non_field_errors) {
          throw data.non_field_errors[0]
        }
      }
    }
  }

  const logOut = function () {
    axios({
      method: 'post',
      url : `${API_URL}/accounts/logout/`,
      headers : {
        Authorization: `Token ${token.value}`
      }
    })
    .then(response => {
      isLoggin.value = false
      token.value = null
      user.value = null
      userdetail.value = null
      router.push({name : 'HomeView'})
    })
    .catch(error => console.log(error))
  }

  const passwordChange = function (passwords) {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/password/change/`,
      headers: {
        'Authorization': `Token ${token.value}`,
        'Content-Type': 'application/json'
      },
      data: {
        new_password1: passwords.new_password1,
        new_password2: passwords.new_password2
      }
    })
    .then((response) => {
      console.log('비밀번호 변경 성공!')
      router.push({ name: 'ProfileView'})
    })
    .catch(error => {
      console.error('비밀번호 변경 실패:', error.response.data)
    })
  }

  const getProfile = async function () {
    try {
      const response = await axios({
        method: 'get',
        url : `${API_URL}/accounts/user/`,
        headers : {
          Authorization : `Token ${token.value}`
        }
      })
      userdetail.value = response.data
      return response.data
    } catch (error) {
      console.log(error)
      return null
    }
  }

  const updateProfile = function (formData, pk) {
    return axios.put(`${API_URL}/api/v1/accounts/update/${pk}/`, formData, {
      headers: {
        'Authorization': `Token ${token.value}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    .then(response => {
      userdetail.value = response.data
      router.push({ name: 'ProfileView' })
    })
    .catch(error => {
      console.error('프로필 업데이트 실패:', error.response)
    })
  }

  return { 
    API_URL, logIn, logOut, token, isLoggin,
    user, getProfile, userdetail, updateProfile, passwordChange,
  }
}, { persist: true })
