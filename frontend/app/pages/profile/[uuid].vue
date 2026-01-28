<template>
  <div class="flex flex-col items-center justify-center"></div>
</template>

<script setup lang="ts">
definePageMeta({
  requiresAuth: true,
  redirectIfAuth: false,
  middleware: (to) => {
    const userStore = useUserStore();
    console.log(to.name);
    if (userStore.user?.uuid === to.params.uuid) return navigateTo("/profile");
  },
  layout: "dashboard"
});
</script>

<style scoped></style>
