<template>
  <div class="container">
    <div >
  <div style="font-size: 20px; margin: 20px;">
    <RouterLink :to="{ name: 'TimeDepositListView' }" class="link-font" active-class="active-link">전체 예금</RouterLink> |
    <RouterLink :to="{ name: 'TimeDepositCompareView' }" class="link-font" active-class="active-link">예금 비교</RouterLink>
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
