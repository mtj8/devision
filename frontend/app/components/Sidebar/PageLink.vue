<template>
  <RouterLink
    :to="link.path"
    class="group/page-link hover:bg-bg-lighter flex w-full items-center justify-start gap-2 rounded-lg px-3 py-2.5 transition"
    :class="{ 'bg-neutral-700 hover:bg-neutral-700!': isActive }"
  >
    <img class="size-6 transition group-hover/page-link:brightness-125" :class="{ 'brightness-125': isActive }" :src="link.icon" aria-hidden="true" draggable="false" />
    <p class="font-medium transition group-hover/page-link:brightness-125" :class="{ 'brightness-125': isActive }">{{ link.name }}</p>
  </RouterLink>
</template>

<script setup lang="ts">
defineProps<{
  link: SidebarLink;
  isActive: boolean;
}>();
</script>

<style scoped></style>
