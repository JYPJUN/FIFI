<template>
  <div class="container">
  <div>
    <nav class="main-font">
      <RouterLink :to="{ name: 'FinancialCoView' }" class="link-font" active-class="active-link">금융회사</RouterLink> |
      <RouterLink :to="{ name: 'TimeDepositView' }" class="link-font" active-class="active-link">정기예금</RouterLink> |
      <RouterLink :to="{ name: 'SavingView' }" class="link-font" active-class="active-link">정기적금</RouterLink> |
      <RouterLink :to="{ name: 'RecommendView' }" class="link-font" active-class="active-link">상품 추천</RouterLink>
    </nav>
    <hr>
    <RouterView />
  </div>
</div>
</template>

<script setup>
import { useCustomerStore } from '@/stores/customer';
import { ref, onMounted } from 'vue';



</script>

<style scoped>

.container {
  display: flex;
  justify-content: center;
  align-items: center;
}

  .main-font {
    position: relative;
    font-size: 25px;
    left: 20px;
    margin-top: 20px;
  }

  .link-font {
    color: inherit;
    text-decoration: none;
  }

  .active-link {
    color: blue;
    font-weight: bold;
  }

</style>