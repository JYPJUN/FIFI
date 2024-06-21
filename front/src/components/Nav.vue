<template>
  <div>
    <div class="header-links">
      <!-- Logo and Navigation Links Together -->
      <div class="logo-and-nav">
        <RouterLink :to="{ name: 'HomeView' }" class="logo-link" >
          <img class="FIFI" alt="Fifi" src="/main_img/FIFI_Logo2_1.png" />
          <div class="text-wrapper">FIFI</div>
        </RouterLink>
        <RouterLink 
          :to="{ name: 'product' }" 
          class="nav-link, link-font"
          active-class="active-link"
          @click.prevent="checkLoginAndNavigate('product')"
        >
          상품조회
        </RouterLink>
        <RouterLink :to="{ name: 'ExchangeView' }" class="nav-link, link-font" active-class="active-link">환율계산기</RouterLink>
        <RouterLink :to="{ name: 'ArticleView' }" class="nav-link, link-font" active-class="active-link">커뮤니티</RouterLink>
        <RouterLink :to="{ name: 'KakaoView' }" class="nav-link, link-font" active-class="active-link">주변은행</RouterLink>
      </div>
      
      <!-- Authentication and Profile Links -->
      <div class="auth-links">
        <RouterLink v-if="!store.isLoggin" :to="{ name: 'SignUpView' }" class="auth-button">회원가입</RouterLink>
        <RouterLink v-if="!store.isLoggin" :to="{ name: 'LogInView' }" class="auth-button">로그인</RouterLink>
          <div v-if="store.isLoggin" class="profile-dropdown">
            <div class="profile-container">
              <img :src="store.userdetail.profile_img" class="profile-image" alt="Profile Image" />
              <span class="profile-username">{{ store.userdetail.nickname }}</span>
            </div>
            <div class="dropdown-content">
            <RouterLink :to="{ name: 'ProfileView' }">프로필</RouterLink>
            <a @click.prevent="logOut" class="logout-link">로그아웃</a>
          </div>
        </div>
      </div>
    </div>
  </div>
    
</template>

<script setup>
import { useCustomerStore } from '@/stores/customer'
import { useRouter } from 'vue-router'

const store = useCustomerStore()
const router = useRouter()

const logOut = function () {
  store.logOut()
}

if (store.isLoggin) {
  store.getProfile()
}

const checkLoginAndNavigate = (routeName) => {
  if (!store.isLoggin) {
    alert('로그인 해주세요.')
    router.push({ name: 'LogInView' })
  } else {
    router.push({ name: `${routeName}` })
  }
}

</script>


<style scoped>
.logout-link {
  color: inherit;
  text-decoration: none;
  cursor: pointer;
  font-size: 15px;
  display: block;
  padding: 12px 16px;
}
.active-link {
  color: blue;
  font-weight: bold;
}

.header-links {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  padding: 10px;
  width: 100%;
}

.link-font {
  color: inherit;
  text-decoration: none;
  font-weight: bold;
  font-size: 20px;
}
.active-link {
  color: blue;
}

.div-wrapper {
  background-color: #ffffff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  padding: 10px;
  width: 100%;
}

.logo-and-nav {
  display: flex;
  align-items: center;
  gap: 20px;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
}

.FIFI {
  height: 40px;
  object-fit: cover;
  margin-right: 10px;
}

.text-wrapper {
  color: #000000;
  font-family: "Noto Sans KR-Bold", Helvetica;
  font-size: 25px;
  font-weight: 700;
}


.nav-link {
  font-family: "Noto Sans KR-Light", Helvetica;
  font-size: 15px;
  font-weight: 300;
  color: inherit;
  text-decoration: none;
}

.auth-links {
  display: flex;
  gap: 20px;
  margin-right: 10px;
}

.auth-button {
  padding: 5px 10px;
  border: none;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
}

.auth-button:hover {
  background-color: #0056b3;
}

.profile-dropdown {
  position: relative;
  display: inline-block;
}

.profile-dropdown .dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 100px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.profile-dropdown .dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.profile-dropdown:hover .dropdown-content {
  display: block;
}

.profile-image {
  width: 50px;
  height: 50px;
  border-radius: 20px;
  object-fit: cover;
  cursor: pointer;
  margin-right: 60px
}
.nav-links {
  display: flex;
  gap: 20px;
}

.profile-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.profile-username {
  position: absolute;
  left: 50px;
  top: 10px;
  font-size: 1.2em;
  color: #333;
}

</style>
