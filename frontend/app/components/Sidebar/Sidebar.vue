<template>
  <div class="bg-bg-darker relative flex h-full w-72 shrink-0 flex-col items-center justify-between p-3">
    <div class="flex w-full flex-col items-center justify-center gap-1">
      <SidebarPageLink v-for="link in pageLinks" :key="link.path" :link="link" :is-active="route.path === link.path || ('customActiveTest' in link ? link.customActiveTest() : false)" />
    </div>

    <div class="my-3 h-1 w-full rounded-full bg-neutral-700"></div>

    <div class="hackathon-scroll mb-20 flex h-full w-full flex-col items-center justify-start overflow-y-scroll">
      <SidebarHackathonLink v-for="hackathon in currentHackathons" :key="hackathon.uuid" :hackathon="hackathon" :is-active="route.path.includes(`/hackathons/${hackathon.uuid}`)" />
    </div>

    <SidebarUserCard />
  </div>
</template>

<script setup lang="ts">
const route = useRoute();

const userStore = useUserStore();
const { currentHackathons, friends } = storeToRefs(userStore);

const pageLinks = [
  {
    name: "Dashboard",
    icon: "/icons/bonfire.svg",
    path: "/home"
  },
  {
    name: "Past Hackathons",
    icon: "/icons/calendar.svg",
    path: "/profile/history"
  },
  {
    name: "Friends",
    icon: "/icons/people.svg",
    path: "/profile/friends",
    customActiveTest: () => route.name === "profile-uuid" && friends.value.some((friend) => route.params.uuid === friend.uuid) // viewing a profile and theyre a friend
  }
] as const satisfies SidebarLink[];
</script>

<style scoped>
.hackathon-scroll {
  scrollbar-width: none;
}
</style>
