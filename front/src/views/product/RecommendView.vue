<template>
  <div class="container">
    <div>
  <div style="font-size: 20px; margin: 20px;">
    <RouterLink :to="{ name: 'RecommendDepositView' }" class="link-font" active-class="active-link">예금 추천</RouterLink> |
    <RouterLink :to="{ name: 'RecommendSavingView' }" class="link-font" active-class="active-link">적금 추천</RouterLink>
  </div>

  <RouterView />
</div>
</div>
</template>

<script setup>


</script>

<style scoped>

.link-font {
    color: inherit;
    text-decoration: none;
  }
.active-link {
  color: blue;
  font-weight: bold;
}
.container {
  display: flex;
  justify-content: center;
}

</style>
