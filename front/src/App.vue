<template>
  <div>
    <header class="nav-size">
      <!-- 최 상단 Navar -->
      <Nav></Nav>
    </header>
    <hr />
    <!-- Navar에서 보여줄 화면 -->
    <RouterView />
  </div>
</template>

<script setup>
import Nav from "@/components/Nav.vue";
</script>

<style scoped>

.nav-size {
  margin: 25px;
}

</style>
