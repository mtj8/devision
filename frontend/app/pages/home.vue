<template>
  <div ref="page" class="flex h-[calc(100dvh-3.5rem)] flex-col items-start justify-start gap-6 overflow-y-scroll p-10">
    <h3 class="text-3xl font-bold">Dashboard</h3>

    <div class="flex w-full items-start justify-between gap-6">
      <div class="flex grow flex-col items-center justify-center gap-6">
        <DashboardHackathonCard v-for="hackathon in loadedHackathons" :key="hackathon.uuid" :hackathon="hackathon" />
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
</template>

<script setup lang="ts">
definePageMeta({
  requiresAuth: true,
  redirectIfAuth: false,
  layout: "dashboard"
});

const userStore = useUserStore();
const { currentHackathons, friends } = storeToRefs(userStore);

const page = useTemplateRef("page");

const loadedHackathons = ref(currentHackathons.value.slice(0, 5));
const loadedHackathonsIndex = ref(currentHackathons.value.length <= 5 ? -1 : 5);

function infiniteScrollHandler() {
  if (!page.value || loadedHackathonsIndex.value === -1) return;

  const scrollTop = page.value.scrollTop;
  const pageHeight = page.value.clientHeight;
  const scrollHeight = page.value.scrollHeight;

  if (scrollTop + pageHeight >= scrollHeight - 100) {
    const newIndex = loadedHackathonsIndex.value + 5;

    loadedHackathons.value.push(...currentHackathons.value.slice(loadedHackathonsIndex.value, newIndex));
    loadedHackathonsIndex.value = newIndex;

    if (newIndex > currentHackathons.value.length - 1) loadedHackathonsIndex.value = -1;
  }
}
const stopPageWatcher = watch(
  page,
  (page) => {
    if (page) {
      page.addEventListener("scroll", infiniteScrollHandler);
      stopPageWatcher();
    }
  },
  { immediate: true }
);
onUnmounted(() => page.value?.removeEventListener("scroll", infiniteScrollHandler));
</script>

<style scoped></style>
