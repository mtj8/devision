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
  await navigateTo("/home");
}
</script>

<style scoped></style>
