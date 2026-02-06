<template>
  <div class="relative m-6 flex w-1/3 items-center justify-center">
    <div class="absolute top-1/2 left-1/2 flex h-full w-full -translate-x-1/2 -translate-y-1/2 flex-col overflow-hidden rounded-xl">
      <div class="w-full px-6 pt-28 opacity-60 transition" :style="{ background: `linear-gradient(to bottom right, #${editableUser.profileGradient[1]}, #${editableUser.profileGradient[0]})` }"></div>
      <div class="h-full w-full px-6 pb-6 opacity-10" :style="{ background: `linear-gradient(to bottom, #${editableUser.profileGradient[0]}, #${editableUser.profileGradient[1]})` }"></div>
    </div>
    <div class="z-1 flex w-full flex-col items-start justify-start gap-4 rounded-xl p-6 pt-16">
      <div class="flex items-center justify-center gap-4">
        <UserProfileCircle :gradient="editableUser.profileGradient" class="-ml-2 size-24" />
        <div class="du-tooltip group/visibility-toggle" :data-tip="editableUser.isPublic ? 'Your profile can be viewed by anyone.' : 'Only friends can view your profile.'">
          <div
            :role="isOwner ? 'button' : undefined"
            class="bg-bg-darker group-hover/visibility-toggle:bg-bg-base flex w-32 items-center justify-center gap-1.5 rounded-full border border-neutral-600 py-1.5 group-hover/visibility-toggle:border-neutral-500/75"
            :disabled="!isOwner"
            :aria-hidden="isOwner ? undefined : 'true'"
            :aria-label="isOwner ? 'Toggle your profile\'s visibility' : undefined"
            @click="editableUser.isPublic = !editableUser.isPublic"
          >
            <div class="du-swap du-swap-rotate">
              <img class="size-6" :class="`du-swap-${editableUser.isPublic ? 'off' : 'on'}`" src="/icons/eye-on.svg" aria-hidden="true" draggable="false" />
              <img class="size-6" :class="`du-swap-${editableUser.isPublic ? 'on' : 'off'}`" src="/icons/eye-off.svg" aria-hidden="true" draggable="false" />
            </div>
            <p class="text-neutral-300 group-hover/visibility-toggle:text-neutral-200">{{ editableUser.isPublic ? "Public" : "Private" }}</p>
          </div>
        </div>
      </div>

      <div class="flex flex-col items-start justify-start">
        <h1 class="text-2xl font-bold">{{ editableUser.displayName }}</h1>
        <p class="text-sm">
          @{{ user.username }}<span v-if="user.isPublic"> · Level {{ user.level }}</span>
        </p>
      </div>

      <div class="flex flex-col items-start justify-start">
        <h3 class="text-xs font-bold">Member Since</h3>
        <p class="text-sm">{{ new Date(user.createdAt).toLocaleString(undefined, { year: "numeric", month: "short", day: "numeric" }) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" generic="T extends User">
const props = defineProps<{
  /** The user to display. */
  user: T;
  /** Whether the profile is being viewed by its user. */
  isOwner: boolean;
}>();

interface EditableUser {
  displayName: PublicUser["displayName"];
  profileGradient: PublicUser["profileGradient"];
  isPublic: boolean;
  school: PublicUser["school"];
  gradYear: PublicUser["gradYear"];
  major: PublicUser["major"];
  bio: PublicUser["bio"];
  socials: PublicUser["socials"];
  skills: PublicUser["skills"];
  interests: PublicUser["interests"];
}

function generateEditableUser(): T extends PublicUser ? EditableUser : undefined {
  type Return = ReturnType<typeof generateEditableUser>;

  if (!props.user.isPublic) return undefined as Return;
  return {
    displayName: props.user.displayName,
    profileGradient: [...props.user.profileGradient],
    isPublic: props.user.isPublic as boolean,
    school: props.user.school,
    gradYear: props.user.gradYear,
    major: props.user.major,
    bio: props.user.bio,
    socials: { ...props.user.socials },
    skills: [...props.user.skills],
    interests: [...props.user.interests]
  } satisfies EditableUser as Return;
}

const editableUser = ref((generateEditableUser() ?? props.user) as EditableUser);
const userIsEdited = computed(() => {
  if (!props.user.isPublic) return false;

  return (
    editableUser.value.displayName !== props.user.displayName ||
    editableUser.value.profileGradient[0] !== props.user.profileGradient[0] ||
    editableUser.value.profileGradient[1] !== props.user.profileGradient[1] ||
    editableUser.value.isPublic !== props.user.isPublic ||
    editableUser.value.school !== props.user.school ||
    editableUser.value.gradYear !== props.user.gradYear ||
    editableUser.value.major !== props.user.major ||
    editableUser.value.bio !== props.user.bio ||
    JSON.stringify(editableUser.value.socials) !== JSON.stringify(props.user.socials) ||
    JSON.stringify(editableUser.value.skills) !== JSON.stringify(props.user.skills) ||
    JSON.stringify(editableUser.value.interests) !== JSON.stringify(props.user.interests)
  );
});
</script>

<style scoped></style>
