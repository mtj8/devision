<template>
  <div class="flex h-dvh flex-col items-center justify-center">
    <p class="text-5xl font-extrabold">sorry, this page is for COOL KIDS ONLY</p>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  requiresAuth: false,
  redirectIfAuth: true
});
</script>

<style scoped></style>
