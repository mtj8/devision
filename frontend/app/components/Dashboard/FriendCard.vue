<template>
  <NuxtLink :to="`/profile/${friend.uuid}`" class="bg-bg-base hover:bg-bg-lighter flex w-full items-center justify-start gap-3 rounded-lg px-4 py-2 transition">
    <UserProfileCircle :gradient="friend.profileGradient" />

    <div class="flex flex-col items-start justify-center">
      <p class="">{{ friend.displayName }}</p>
      <p class="text-text-lighter text-xs">@{{ friend.username }}</p>
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
defineProps<{ friend: PublicUser }>();
</script>

<style scoped></style>
