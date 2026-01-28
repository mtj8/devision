<template>
  <NuxtLink
    v-if="user"
    to="/profile"
    class="group/user-card bg-bg-base hover:bg-bg-lighter absolute bottom-3 left-1/2 flex h-18 w-19/20 -translate-x-1/2 flex-col items-center justify-center rounded-lg pt-1 shadow-lg transition"
  >
    <div class="mb-2 flex w-full items-center justify-around">
      <div class="flex items-center justify-center gap-3 select-none">
        <UserProfileCircle :gradient="user.profileGradient" />

        <div class="flex flex-col items-start justify-center">
          <p class="w-32 overflow-hidden text-nowrap overflow-ellipsis">{{ user.displayName }}</p>
          <p class="text-text-lighter text-xs">@{{ user.username }}</p>
        </div>
      </div>

      <NuxtLink to="/profile/settings" class="du-tooltip group/settings rounded-full p-1 transition hover:bg-neutral-700" data-tip="User Settings" @click.prevent>
        <img
          class="size-6 transition-transform duration-1500 group-hover/settings:rotate-360 group-hover/settings:brightness-110"
          src="/icons/settings.svg"
          alt="Open user settings"
          draggable="false"
        />
      </NuxtLink>
    </div>

    <div class="du-tooltip absolute bottom-0 left-0 w-full cursor-default" :data-tip="`Level ${user.level} - ${user.xp}/${user.xpNeeded} XP`" @click.prevent>
      <div class="relative h-1 w-full overflow-hidden rounded-b-lg bg-neutral-900 transition-[height] group-hover/user-card:h-1.5">
        <div
          class="absolute top-0 left-0 h-full bg-gradient-to-r from-green-500 via-green-400 to-green-500 transition group-hover:brightness-125"
          :style="{ width: `${Math.max(5, Math.min((user.xp / user.xpNeeded) * 100, 95))}%` }"
        ></div>
      </div>
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
const userStore = useUserStore();
const { user } = storeToRefs(userStore);
</script>

<style scoped></style>
