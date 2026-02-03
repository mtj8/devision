<template>
  <div class="flex min-h-dvh w-screen flex-col items-center justify-center pb-6">
    <NuxtLink to="/">
      <img src="/devision-full.svg" aria-hidden="true" class="mb-6 h-32" />
    </NuxtLink>

    <h1 class="text-5xl font-bold">Welcome back!</h1>
    <div class="mb-4 flex flex-col items-center justify-center rounded-3xl px-2">
      <h3 class="mb-4">Login to your Devision account</h3>

      <form class="flex w-full flex-col items-center justify-center gap-7" @submit="login" @submit.prevent>
        <div class="relative flex flex-col items-start justify-center gap-1">
          <label class="font-medium" for="email">Email Address <span title="Required" class="text-red-500">*</span></label>
          <input
            id="email"
            v-model="email"
            class="bg-bg-darker border-bg-lighter focus:bg-bg-darkest h-12 w-88 rounded-lg border-2 px-4 transition focus:outline-none"
            type="email"
            required
            autocomplete="email"
          />
          <p v-show="emailErr.length > 0" class="error font-medium text-red-500">{{ emailErr }}</p>
        </div>

        <div class="relative flex flex-col items-start justify-center gap-1">
          <label class="font-medium" for="password">Password <span title="Required" class="text-red-500">*</span></label>
          <input
            id="password"
            v-model="password"
            class="bg-bg-darker border-bg-lighter focus:bg-bg-darkest h-12 w-88 rounded-lg border-2 px-4 transition focus:outline-none"
            type="password"
            required
            autocomplete="current-password"
          />
        </div>

        <p v-show="loginErr.length > 0" class="error -my-4 font-medium text-red-500">{{ loginErr }}</p>

        <div class="relative flex flex-col items-center justify-center gap-1">
          <button class="group w-40 items-center rounded-lg bg-sky-400 px-16 py-2 transition hover:bg-indigo-500" type="submit">
            <p class="font-medium text-neutral-800 transition group-hover:text-neutral-200">Login</p>
          </button>
        </div>
      </form>
    </div>

    <NuxtLink to="/signup" class="mt-3 text-neutral-200"> Don't have an account? <span class="underline underline-offset-2">Sign up here</span>. </NuxtLink>
    <NuxtLink to="/reset-password" class="mt-3 text-neutral-200"> Forgot password? <span class="underline underline-offset-2">Reset here</span>. </NuxtLink>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  requiresAuth: false,
  redirectIfAuth: true
});

const userStore = useUserStore();

const email = ref("");
const emailErr = ref("");
const password = ref("");
const loginErr = ref("");

async function login() {
  // hardcoded email and password mmmmmmmmmm
  if (email.value !== "chatgpt@gemini.claude" || password.value !== "password1235") return (loginErr.value = "Invalid email or password.");

  userStore.isAuth = true;
  userStore.user = {
    uuid: "fuck-fuck-fuck-fuck",
    displayName: "XxX_LeetCoder_XxX",
    profileGradient: ["565dc5", "56deff"],
    username: "l33tcoder",
    email: "l33tcoder@gmail.com",
    school: "Monsters University",
    level: 2,
    xp: 990,
    xpNeeded: 1000,
    isPublic: true,
    socials: {
      discord: null,
      instagram: null,
      github: null,
      linkedin: null,
      personal: null
    },
    bio: "Just another leet coder",
    skills: ["JavaScript"],
    interests: ["Coding", "Hacking", "AI"],
    createdAt: new Date()
  };
  userStore.friends = [
    {
      uuid: "9999-1111-2222-3333",
      friendsSince: new Date(1759976226 * 1000),
      displayName: "Joe Biden",
      profileGradient: ["00ff00", "00ffff"],
      username: "itsjoever",
      level: 3,
      isBlocked: false
    },
    {
      uuid: "8888-4444-5555-6666",
      displayName: "Elongated Muskrat",
      friendsSince: new Date(1758976226 * 1000),
      profileGradient: ["0000ff", "ff0000"],
      username: "therealelonmusk",
      level: 2,
      isBlocked: false
    },
    {
      uuid: "7777-7777-7777-7777",
      displayName: "Tim Apple",
      friendsSince: new Date(1756976226 * 1000),
      profileGradient: ["ffff00", "ff00ff"],
      username: "timapple",
      level: 5,
      isBlocked: false
    },
    {
      uuid: "6666-5555-4444-3333",
      displayName: "Ronald Rump",
      friendsSince: new Date(1754976226 * 1000),
      profileGradient: ["00ff00", "ff8800"],
      username: "realdonaldtrump",
      level: 4,
      isBlocked: false
    },
    {
      uuid: "5555-6666-7777-8888",
      displayName: "The Zuck",
      friendsSince: new Date(1753976226 * 1000),
      profileGradient: ["888888", "000000"],
      username: "markzuck",
      level: 3,
      isBlocked: false
    },
    {
      uuid: "4444-3333-2222-1111",
      displayName: "free robux check profile!!",
      friendsSince: new Date(1747976226 * 1000),
      profileGradient: ["ff00ff", "00ffff"],
      username: "someidiot123",
      level: 5,
      isBlocked: false
    },
    {
      uuid: "3333-2222-1111-0000",
      displayName: "Jeff Amazon",
      friendsSince: new Date(1752976226 * 1000),
      profileGradient: ["0000ff", "00ff00"],
      username: "jeffbezos",
      level: 4,
      isBlocked: false
    },
    {
      uuid: "2222-3333-4444-5555",
      displayName: "Bill Microsoft",
      friendsSince: new Date(1749976226 * 1000),
      profileGradient: ["ff8800", "ffff00"],
      username: "billgates",
      level: 5,
      isBlocked: false
    }
  ];
  userStore.currentHackathons = [
    {
      uuid: "hb87gybrwb98risdughiuds",
      name: "Not HackBU 2026",
      img: "/example-splash/shower.jpg",
      description:
        "Registrations for HackBU 2026 are not open! This 24-hour event in Binghamton's Innovative Technology Complex is not set for March 7th and 8th, when university students will not compete in teams of 1-4 to build the least impressive project within that time. Without a chance to exercise your programming and project management skills, this is a horrible chance to not network with our sponsors and with other students. Our programming does not feature crash-courses for newcomers, team-matching, and an award ceremony with prizes in no categories.",
      startDate: new Date(1769706000 * 1000),
      endDate: new Date(1769792400 * 1000),
      participants: 152,

      team: {
        uuid: "team-1234-5678-9012",
        name: "Masterchefs (we're cooked)",
        createdAt: new Date(1769976226 * 1000),
        members: [
          {
            uuid: "9999-1111-2222-3333",
            displayName: "Joe Biden",
            friendsSince: new Date(1759976226 * 1000),
            profileGradient: ["00ff00", "00ffff"] as [string, string],
            username: "itsjoever",
            level: 3,
            isBlocked: false
          },
          {
            uuid: "8888-4444-5555-6666",
            displayName: "Elongated Muskrat",
            friendsSince: new Date(1758976226 * 1000),
            profileGradient: ["0000ff", "ff0000"] as [string, string],
            username: "therealelonmusk",
            level: 2,
            isBlocked: false
          }
        ]
      }
    },
    {
      uuid: "dug87ewgtegioaf",
      name: "Hack the North 2026",
      img: "/example-splash/grass.jpg",
      description:
        "Hack the North is back! Join us for an epic weekend of coding, creativity, and collaboration at Canada's largest hackathon. Whether you're a seasoned hacker or just starting out, Hack the North offers a welcoming environment to learn new skills, build innovative projects, and connect with like-minded individuals. Don't miss this opportunity to be part of a vibrant tech community and make your mark on the future of technology.",
      startDate: new Date(1772976226 * 1000),
      endDate: new Date(1773976226 * 1000),
      participants: 301
    },
    {
      uuid: "eug78ewtg8egvsdgoiasop",
      name: "2026 Global Hackathon",
      img: "/example-splash/outside.jpg",
      description:
        "The 2026 Global Hackathon is an international event that unites developers, designers, and entrepreneurs from around the world to collaborate on cutting-edge projects. Participants will have the chance to work on innovative solutions to global challenges, network with industry leaders, and gain exposure to new technologies. This hackathon is open to individuals of all skill levels who are passionate about making a difference through technology.",
      startDate: new Date(1781376269 * 1000),
      endDate: new Date(1782376269 * 1000),
      participants: 507
    }
    // {
    //   uuid: "4444-4444-4444-4444",
    //   name: "Startup Weekend 2026",
    //   description:
    //     "Build a startup in 54 hours! Join us for Startup Weekend 2026, where aspiring entrepreneurs, developers, designers, and business enthusiasts come together to pitch ideas, form teams, and launch startups. Over the course of a weekend, participants will have the opportunity to learn from experienced mentors, validate their business concepts, and present their startups to a panel of judges for a chance to win exciting prizes. Whether you're looking to turn your idea into reality or simply want to experience the thrill of startup culture, Startup Weekend is the place to be.",
    //   startDate: new Date(1769976360 * 1000),
    //   endDate: new Date(1770976360 * 1000),
    //   participants: 212
    // },
    // {
    //   uuid: "5555-5555-5555-5555",
    //   name: "Code for Good 2025",
    //   description:
    //     "Code for a Cause is a hackathon dedicated to creating technology solutions for social good. Participants will work in teams to develop projects that address real-world challenges faced by non-profit organizations and communities in need. Whether it's building apps, websites, or other digital tools, this hackathon is all about using coding skills to make a positive impact. Join us to innovate, collaborate, and contribute to meaningful change through technology.",
    //   startDate: new Date(1765976395 * 1000),
    //   endDate: new Date(1766276395 * 1000),
    //   participants: 253
    // },
    // {
    //   uuid: "6666-6666-6666-6666",
    //   name: "AI Innovators Hackathon 2026",
    //   description:
    //     "Innovate with AI at the AI Innovators Hackathon 2026! Join us for a weekend of cutting-edge technology, collaboration, and creativity as we explore the potential of artificial intelligence. Participants will have the opportunity to work on exciting projects, learn from industry experts, and showcase their skills in a supportive environment. Whether you're a seasoned AI developer or just starting out, this hackathon is the perfect place to push the boundaries of what's possible with AI.",
    //   startDate: new Date(1770576421 * 1000),
    //   endDate: new Date(1771576421 * 1000),
    //   participants: 413
    // },
    // {
    //   uuid: "7777-7777-7777-7777",
    //   name: "GreenTech Hackathon 2026",
    //   description:
    //     "Innovate for a sustainable future at the GreenTech Hackathon 2026! Join us for an exciting event focused on developing technology solutions that address environmental challenges. Participants will collaborate to create projects that promote sustainability, conservation, and eco-friendly practices. Whether you're passionate about clean energy, waste reduction, or environmental awareness, this hackathon is the perfect platform to turn your ideas into impactful solutions. Let's work together to make a positive difference for our planet!",
    //   startDate: new Date(1772076492 * 1000),
    //   endDate: new Date(1772576492 * 1000),
    //   participants: 186
    // },
    // {
    //   uuid: "8888-8888-8888-8888",
    //   name: "HealthTech Hackathon 2026",
    //   description:
    //     "Tech for Health is a hackathon dedicated to improving healthcare through technology. Participants will work in teams to develop innovative solutions that address pressing health challenges, from telemedicine to health data management. Join us to collaborate with like-minded individuals, learn from industry experts, and make a positive impact on the future of healthcare.",
    //   startDate: new Date(1767076522 * 1000),
    //   endDate: new Date(1768076522 * 1000),
    //   participants: 229
    // }
  ].sort((a, b) => a.startDate.getTime() - b.startDate.getTime());

  await new Promise((resolve) => setTimeout(resolve, Math.round(Math.random() * 500) + 500));
  await navigateTo("/home");
}
</script>

<style scoped></style>
