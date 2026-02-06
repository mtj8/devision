<template>
  <div class="flex h-[calc(100dvh-3.5rem)] w-full items-start justify-between gap-6 overflow-y-scroll p-10">
    <ProfileCard v-if="user" :user="user" is-owner />

    <div class="w-2/3"></div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  requiresAuth: true,
  redirectIfAuth: false,
  layout: "dashboard"
});

const userStore = useUserStore();
const { user } = storeToRefs(userStore);
</script>

<style scoped></style>
