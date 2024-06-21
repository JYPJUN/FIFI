<template>
  <div class="container">
      <KakaoMap />
  </div>
</template>

<script setup>
import KakaoMap from '@/components/KakaoMap.vue';


</script>

<style scoped>

.container {
  display: flex;
  flex-direction: column;
  margin: 0 auto;
  width: 70%;
  margin-top: 40px;
  padding: 70px;
}

</style>