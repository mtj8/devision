<template>
  <NuxtLink
    :to="`/hackathons/${hackathon.uuid}`"
    class="group/hackathon-card hover:bg-bg-lighter flex w-full flex-col items-start justify-center rounded-lg px-4 py-2 transition select-none"
    :class="{ 'bg-neutral-700 hover:bg-neutral-700!': isActive }"
  >
    <h4 class="w-56 overflow-hidden text-lg font-medium text-nowrap overflow-ellipsis transition group-hover/hackathon-card:brightness-125" :class="{ 'brightness-125': isActive }">
      {{ hackathon.name }}
    </h4>
    <p class="text-sm">{{ hackathon.participants }} Participants</p>
  </NuxtLink>
</template>

<script setup lang="ts">
defineProps<{
  hackathon: Hackathon;
  isActive: boolean;
}>();
</script>

<style scoped></style>
