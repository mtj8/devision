<template>
  <div
    class="size-10 shrink-0 rounded-full"
    :style="{
      background: `linear-gradient(to bottom right, #${gradient[0]}, #${gradient[1]})`
    }"
  ></div>
</template>

<script setup lang="ts">
defineProps<{ gradient: UserProfile["profileGradient"] }>();
</script>

<style scoped></style>
