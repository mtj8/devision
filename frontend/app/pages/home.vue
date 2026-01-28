<template>
  <div v-if="isLoaded" class="flex flex-col items-start justify-start gap-6 overflow-y-scroll p-10">
    <h3 class="text-3xl font-bold">Dashboard</h3>

    <div class="flex w-full items-start justify-between gap-6">
      <div class="flex grow flex-col items-center justify-center gap-6">
        <DashboardHackathonCard v-for="hackathon in currentHackathons.slice(0, 5)" :key="hackathon.uuid" :hackathon="hackathon" />
      </div>

      <div class="flex w-72 shrink-0 flex-col items-center justify-center gap-6">
        <div class="bg-bg-darker flex w-full flex-col items-center justify-start gap-2 rounded-lg p-2">
          <DashboardFriendCard v-for="friend in friends.slice(0, 5)" :key="friend.uuid" :friend="friend" />
          <NuxtLink to="/profile/friends" class="bg-bg-base hover:bg-bg-lighter flex w-full items-center justify-start gap-4 rounded-lg px-4 py-2 transition">
            <img class="ms-1 size-8" src="/icons/people.svg" aria-hidden="true" draggable="false" />
            <p>View All Friends</p>
          </NuxtLink>
        </div>

        <NuxtLink class="bg-bg-darker hover:bg-bg-darkest group/find-hackathons flex w-full items-center justify-center gap-3 rounded-lg px-8 py-3 transition" to="/hackathons">
          <img src="/icons/search.svg" aria-hidden="true" class="size-7 transition group-hover/find-hackathons:brightness-125" draggable="false" />
          <p class="text-lg font-medium transition group-hover/find-hackathons:brightness-125">Find Hackathons</p>
        </NuxtLink>
      </div>
    </div>
  </div>
  <div v-else class="flex flex-col items-start justify-start gap-6 overflow-y-scroll p-10"></div>
</template>

<script setup lang="ts">
definePageMeta({
  requiresAuth: true,
  redirectIfAuth: false,
  layout: "dashboard"
});

const userStore = useUserStore();
const { currentHackathons, friends } = storeToRefs(userStore);

const isLoaded = ref(false);
onMounted(() => setTimeout(() => (isLoaded.value = true), 200));

// TODO: add infinite scroll for hackathons
</script>

<style scoped></style>
