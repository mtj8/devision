<template>
  <div class="flex w-full flex-col items-center justify-center">
    <div class="flex h-40 w-full items-center justify-between rounded-lg bg-[#252525] px-10 py-5 shadow-lg">
      <div class="flex flex-col items-start justify-center gap-2">
        <h4 class="w-96 overflow-hidden text-2xl font-semibold text-nowrap overflow-ellipsis">{{ hackathon.name }}</h4>
        <p class="line-clamp-4 w-96 text-sm text-gray-400">{{ hackathon.description }}</p>
      </div>

      <div class="flex flex-col items-end justify-center gap-2">
        <p class="text-sm text-gray-400" :title="hackathon.startDate.toLocaleString()">Starts: {{ daysUntil(hackathon.startDate) }}</p>
        <p class="text-sm text-gray-400" :title="hackathon.endDate.toLocaleString()">Ends: {{ daysUntil(hackathon.endDate) }}</p>
        <NuxtLink :to="`/hackathons/${hackathon.uuid}`" class="bg-theme rounded-lg px-6 py-1.5 text-lg font-medium transition hover:brightness-105">View Hackathon</NuxtLink>
      </div>
    </div>

    <div v-if="hackathon.team" class="bg-bg-darker flex h-16 w-4/5 items-center justify-between rounded-b-lg px-4 py-2">
      <div class="flex flex-col items-start justify-center">
        <p class="text-sm text-neutral-400">Your Team</p>
        <h5>{{ hackathon.team.name }}</h5>
      </div>

      <div class="flex flex-col items-end justify-center">
        <p class="text-sm text-neutral-400">Members</p>
        <span>
          <span v-for="(member, index) in hackathon.team.members" :key="member.uuid">
            <NuxtLink :to="`/profile/${member.uuid}`" class="transition hover:underline hover:brightness-105">{{ member.displayName }}</NuxtLink
            >{{ index < hackathon.team.members.length - 1 ? ", " : "" }}
          </span>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ hackathon: Hackathon }>();

const now = Date.now();

/** Returns a string describing the time remaining until the specified date.
 * @param date The future date to calculate the time remaining until.
 * @return A string representing the time remaining until the date in days, hours, or minutes.
 */
function daysUntil(date: Date) {
  const diffTime = date.getTime() - now;

  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  if (diffDays >= 7) return date.toLocaleString();
  if (diffDays >= 1) return `${diffDays} day${diffDays !== 1 ? "s" : ""}`;

  const diffHours = Math.ceil(diffTime / (1000 * 60 * 60));
  if (diffHours >= 1) return `${diffHours} hour${diffHours !== 1 ? "s" : ""}`;

  const diffMinutes = Math.ceil(diffTime / (1000 * 60));
  return `${diffMinutes} minute${diffMinutes !== 1 ? "s" : ""}`;
}
</script>

<style scoped></style>
