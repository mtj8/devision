<template>
  <div ref="page" class="flex flex-col items-center justify-center gap-6 p-10">
    <h2 class="text-3xl font-bold">Friends</h2>

    <div class="flex w-full flex-col items-center justify-center border-b border-neutral-600">
      <NuxtLink
        v-for="friend in loadedFriends"
        :key="friend.uuid"
        :to="`/profile/${friend.uuid}`"
        class="hover:bg-bg-lighter flex w-full items-center justify-between rounded-lg border-t border-neutral-600 px-10 py-3 transition"
      >
        <div class="flex items-center justify-center gap-4">
          <UserProfileCircle :gradient="friend.profileGradient" />
          <p class="text-xl font-medium">{{ friend.displayName }}</p>
        </div>
      </NuxtLink>
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
const { friends } = storeToRefs(userStore);

const page = useTemplateRef("page");

const loadedFriends = ref<PublicUser[]>(friends.value.slice(0, 5));
const loadedFriendsIndex = ref(friends.value.length <= 5 ? -1 : 5);

function infiniteScrollHandler() {
  if (!page.value || loadedFriendsIndex.value === -1) return;

  const scrollTop = page.value.scrollTop;
  const pageHeight = page.value.clientHeight;
  const scrollHeight = page.value.scrollHeight;

  if (scrollTop + pageHeight >= scrollHeight - 100) {
    const newIndex = loadedFriendsIndex.value + 5;

    loadedFriends.value.push(...friends.value.slice(loadedFriendsIndex.value, newIndex));
    loadedFriendsIndex.value = newIndex;

    if (newIndex > friends.value.length - 1) loadedFriendsIndex.value = -1;
  }
}
</script>

<style scoped></style>
