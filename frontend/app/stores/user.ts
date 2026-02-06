interface LoginOutput {
  user: PublicUser;
  // TODO: todo
  hackathons: any[];
  // TODO: todo
  friends: any[];
}

export const useUserStore = defineStore("userStore", () => {
  const user = ref<PublicUser>();
  const isAuth = ref(false);

  const friends = ref<PublicUser[]>([]);
  const currentHackathons = ref<Hackathon[]>([]);

  function parseLoginOutput(data: LoginOutput) {
    // @ts-expect-error parse unix timestamp to Date
    data.user.createdAt = new Date(data.user.createdAt * 1000);

    user.value = data.user;
    friends.value = data.friends;
    currentHackathons.value = data.hackathons;
  }

  async function init() {
    const { data, error } = await fetchEndpoint<LoginOutput>("init");
    if (error) return false;

    parseLoginOutput(data);
    // TODO: remove temp data
    // @ts-expect-error L womp womp
    data.user.major = "Computer Science";
    // @ts-expect-error L womp womp
    data.user.socials = {
      discord: "verycool.discord",
      instagram: "somewhat.cool.insta",
      github: "githubuser",
      linkedin: "https://www.linkedin.com/in/someone/",
      personal: "https://kennethng.dev/"
    };
    return (isAuth.value = true);
  }

  /** @returns `true` if login successful, `false` otherwise */
  async function login(email: string, password: string) {
    const { data, error } = await fetchEndpoint<LoginOutput>("login", "POST", { email, password });
    if (error) return false;

    parseLoginOutput(data);
    return (isAuth.value = true);
  }

  return { user, isAuth, friends, currentHackathons, init, login };
});
