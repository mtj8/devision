<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();

useSeoMeta({
  ogUrl: () => config.public.baseUrl,
  ogImage: () => `${config.public.baseUrl}logo/devision-full.png`,
  twitterCard: "summary_large_image",
  twitterImage: () => `${config.public.baseUrl}logo/devision-full.png`
});
</script>

<style scoped></style>
