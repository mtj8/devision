export const useUserStore = defineStore("userStore", () => {
  const user = ref<UserProfile>();
  const isAuth = ref(false);

  const friends = ref<PublicUser[]>([]);
  const currentHackathons = ref<Hackathon[]>([]);

  return { user, isAuth, friends, currentHackathons };
});
