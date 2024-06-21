<template>
  <div>
    <div class="div-wrapper-screen">
      <div class="div-4">
        <div class="overlap">
          <!-- 메인 1번 -->
          <div class="view">
            <img class="img" alt="Element" src="/main_img/메인1-이미지.png" />
            <div class="maintext-1-position
          ">
              <div class="textbigtext">
                사회 초년생의
                <br />
                FIT한 FIN-TECH
              </div>
              <p class="maintext-1-b">
                내 성향에 딱 맞는
                <br />
                트렌디한 추천 재테크로 쉽게해요
              </p>
              <div class="box-wrap" v-if="!store.isLoggin">
                <RouterLink
                  :to="{ name: 'LogInView' }"
                  style="text-decoration: none"
                  @click="scrollToTop"
                >
                  <div class="blue-box">
                    <div class="box-text">로그인</div>
                  </div>
                </RouterLink>
              </div>
              <div class="login-style" v-if="!store.isLoggin">
                <RouterLink :to="{ name: 'SignUpView' }" style="text-decoration: none">
                  <div class="blue-box">
                    <div class="box-text">회원가입</div>
                  </div>
                </RouterLink>
              </div>
            </div>
          </div>

          <!-- 메인2번 -->
          <div class="element-4">
            <img class="img2" alt="Element" src="/main_img/메인2-이미지.png" />
            <div class="maintext-2-position
          ">
              <div class="text-wrapper-1">상품 조회</div>
              <div class="textbigtext">
                나를 위한
                <br />
                금융 서비스
              </div>
              <p class="maintext-345-b">
                나에게 맞는 상품을 확인하고
                <br />
                똑! 부러지게 비교하고 선택!
              </p>
              <div class="box-wrap">
                <RouterLink
                  :to="{ name: 'product' }"
                  style="text-decoration: none"
                  @click="scrollToTop"
                >
                  <div class="blue-box">
                    <div class="box-text">상품 조회</div>
                  </div>
                </RouterLink>
              </div>
            </div>
          </div>
          
          <!-- 메인 3번 -->
          <div class="element-3">
            <img class="img" alt="Element" src="/main_img/메인3-이미지.png" />
            <div class="maintext-3-position">
              <div class="text-wrapper-1">환율 계산기</div>
              <div class="frame">
                <div class="maintext-3-t">
                  환전 조회 서비스
                </div>
                <p class="maintext-1-b">
                  환율 계산기를 이용하여
                  <br />
                  환전에 필요한 금액을 알아보세요!
                </p>
                <div class="box-wrap">
                  <RouterLink
                    :to="{ name: 'ExchangeView' }"
                    style="text-decoration: none"
                    @click="scrollToTop"
                  >
                    <div class="blue-box">
                      <div class="box-text">환전 조회</div>
                    </div>
                  </RouterLink>
                </div>
              </div>
            </div>
          </div>

          <!-- 메인 4번 -->
          <div class="element-2">
            <img class="img2" alt="Element" src="/main_img/메인4-이미지.png" />
            <div class="maintext-4-position">
              <div class="text-wrapper-1">커뮤니티</div>
              <div class="textbigtext">
                꽁꽁 얼어붙은
                <br />
                재테크를 재미있게
              </div>
              <p class="maintext-345-b">
                누구보다 빠르게 남들과는 다르게
                <br />
                최신 재테크 정보를 얻어가세요!
              </p>
              <div class="box-wrap">
                <RouterLink
                  :to="{ name: 'ArticleView' }"
                  style="text-decoration: none"
                  @click="scrollToTop"
                >
                  <div class="blue-box">
                    <div class="box-text">커뮤니티</div>
                  </div>
                </RouterLink>
              </div>
            </div>
          </div>

          <!-- 메인 5번 -->
          <div class="element">
            <img class="img" alt="Element" src="/main_img/메인5-이미지.png" />
            <div class="maintext-5-position">
              <div class="text-wrapper-1">주변 은행</div>
              <div class="textbigtext">
                내 주변, 동네
                <br />
                은행 검색하기
              </div>
              <div class="maintext-345-b">
                집 근처 은행을
                <br />
                지도에서 확인해보세요
              </div>
              <div class="box-wrap">
                <RouterLink
                  :to="{ name: 'KakaoView' }"
                  style="text-decoration: none"
                  @click="scrollToTop"
                >
                  <div class="blue-box">
                    <div class="box-text">지도 검색</div>
                  </div>
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCustomerStore } from "@/stores/customer";

const store = useCustomerStore();

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
  });
};
</script>

<style scoped>
.div-wrapper-screen {
  background-color: #ffffff;
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
}

.div-wrapper-screen .div-4 {
  background-color: #ffffff;
  position: relative;
  
}

.div-wrapper-screen .view {
  background-color: rgb(222, 236, 241);
  height: 750px;
  width: 1200px;
}

.div-wrapper-screen .element-4 {
  background-color: #f9f9f9;
  height: 750px;
  position: absolute;
  top: 749px;
  width: 1200px;
}

.div-wrapper-screen .element-3 {
  background-color: var(--variable-collection-2);
  height: 750px;
  left: 0;
  position: absolute;
  top: 1555px;
  width: 1200px;
}

.div-wrapper-screen .element-2 {
  background-color: rgb(222, 236, 241);
  height: 750px;
  left: 0;
  position: absolute;
  top: 2305px;
  width: 1200px;
}

.div-wrapper-screen .element {
  background-color: #f9f9f9;
  height: 750px;
  left: 0;
  position: absolute;
  top: 3055px;
  width: 1200px;
}

.div-wrapper-screen .img {
  height: 496px;
  left: 600px;
  position: absolute;
  top: 127px;
  width: 521px;
}

.div-wrapper-screen .img2 {
  height: 496px;
  left: 50px;
  position: absolute;
  top: 127px;
  width: 521px;
}

.div-wrapper-screen .maintext-1-position {
  height: 323px;
  left: 100px;
  position: absolute;
  top: 214px;
  width: 428px;
}

.div-wrapper-screen .maintext-2-position {
  height: 265px;
  left: 710px;
  position: absolute;
  top: 242px;
  width: 363px;
}

.div-wrapper-screen .maintext-3-position {
  height: 265px;
  left: 100px;
  position: absolute;
  top: 242px;
  width: 474px;
}

.div-wrapper-screen .maintext-4-position {
  height: 265px;
  left: 710px;
  position: absolute;
  top: 242px;
  width: 386px;
}

.div-wrapper-screen .maintext-5-position {
  height: 265px;
  left: 100px;
  position: absolute;
  top: 242px;
  width: 351px;
}


.div-wrapper-screen .textbigtext {
  color: #000000;
  font-size: 45px;
  font-weight: 700;
}

.div-wrapper-screen .maintext-345-b {
  color: #000000;
  font-size: 25px;
  font-weight: 300px;
  position: absolute;
  top: 170px;
}

.div-wrapper-screen .maintext-3-t {
  color: #000000;
  font-size: 50px;
  font-weight: 700;
}

.div-wrapper-screen .maintext-1-b {
  color: #000000;
  font-size: 25px;
  font-weight: 300px;
  position: absolute;
  top: 162px;
}

.div-wrapper-screen .box-text {
  color: #ffffff;
  font-size: 25px;
}

.div-wrapper-screen .box-wrap {
  position: absolute;
  top: 269px;
}

.div-wrapper-screen .blue-box {
  justify-content: center;
  align-items: center;
  background-color: #1675f2;
  border-radius: 8px;
  height: 54px;
  width: 150px;
  display: flex;
}

.div-wrapper-screen .login-style {
  top: 269px;
  left: 169px;
  position: absolute;
}

</style>
