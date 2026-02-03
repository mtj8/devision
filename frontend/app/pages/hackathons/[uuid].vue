<template>
  <div v-if="hackathon" class="flex w-full flex-col items-center justify-center gap-8 p-10">
    <!-- @vue-expect-error -->
    <div class="relative flex h-50 w-full items-center justify-center overflow-hidden rounded-lg" :class="{ 'bg-gradient-to-br from-green-400 to-sky-500': !hackathon.img }">
      <h1 class="pointer-events-none absolute top-1/2 left-1/2 z-2 -translate-x-1/2 -translate-y-1/2 text-4xl font-bold text-white select-none">{{ hackathon.name }}</h1>
      <div class="absolute top-1/2 left-1/2 z-1 h-full w-full -translate-x-1/2 -translate-y-1/2 bg-black/35 duration-300 hover:bg-transparent"></div>
      <!-- @vue-expect-error -->
      <img v-if="hackathon.img" :src="hackathon.img" />
    </div>

    <p class="text-center">{{ hackathon.description }}</p>

    <div class="flex w-full items-center justify-center gap-10">
      <div class="bg-bg-darker flex w-1/2 shrink-0 flex-col items-center justify-start rounded-lg p-6" :class="{ 'w-full!': !hackathon.team }">
        <h3 class="mb-4 text-2xl font-bold text-white">Info</h3>

        <p class="text-lg font-medium">Starts {{ daysUntil(hackathon.startDate) }}</p>
        <p class="text-lg font-medium">Ends {{ daysUntil(hackathon.endDate) }}</p>
        <p class="mt-4 text-xl font-medium text-neutral-100">{{ hackathon.participants }} Participants</p>

        <a
          href="https://kennethng.dev"
          rel="noopener noreferrer"
          target="_blank"
          class="bg-bg-darkest mt-6 flex items-center justify-center gap-2 rounded-lg px-6 py-3 transition hover:bg-neutral-700"
        >
          <p class="text">View external site</p>
          <img src="/icons/open.svg" aria-hidden="true" class="size-6" />
        </a>
      </div>

      <div v-if="hackathon.team" class="bg-bg-darker flex w-1/2 shrink-0 flex-col items-center justify-start rounded-lg p-6">
        <h3 class="mb-4 text-2xl font-bold text-white">Your Team</h3>

        <div class="flex w-full flex-col items-center justify-center gap-1">
          <div v-if="user" class="flex w-full items-center justify-between rounded-lg px-10 py-2 transition select-none">
            <div class="flex items-center justify-center gap-4">
              <UserProfileCircle :gradient="user.profileGradient" />
              <p class="text-xl font-medium">You</p>
            </div>
          </div>
          <NuxtLink
            v-for="member in hackathon.team.members"
            :key="member.uuid"
            :to="`/profile/${member.uuid}`"
            class="hover:bg-bg-lighter flex w-full items-center justify-between rounded-lg px-10 py-2 transition"
          >
            <div class="flex items-center justify-center gap-4">
              <UserProfileCircle :gradient="member.profileGradient" />
              <p class="text-xl font-medium">{{ member.displayName }}</p>
            </div>
          </NuxtLink>
        </div>
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

const route = useRoute();
const uuid = String(route.params.uuid);
const userStore = useUserStore();
const { currentHackathons, user } = storeToRefs(userStore);
const hackathon = computed(() => currentHackathons.value.find((hackathon) => hackathon.uuid === uuid));
</script>

<style scoped></style>
