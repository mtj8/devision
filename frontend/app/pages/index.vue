<template>
  <div class="fixed top-0 left-0 flex h-dvh w-dvw items-center justify-center">
    <img
      v-for="(part, i) in parts"
      :key="part.src"
      :src="part.src"
      aria-hidden="true"
      class="h-20 sm:h-36 md:h-44 lg:h-62 xl:h-80"
      :class="{ float: animationDone, 'bounce-in': part.isVisible, 'opacity-0': !part.isVisible }"
      :style="{ animationDelay: `${animationDone ? i * 150 : 0}ms` }"
    />

    <div class="fixed bottom-10 left-1/2 flex -translate-x-1/2 items-center justify-center gap-10">
      <Transition>
        <NuxtLink
          v-show="animationDone"
          to="/login"
          class="rounded-full border-2 border-neutral-400/50 px-12 py-3 text-2xl font-medium transition hover:border-neutral-300 hover:bg-neutral-300 hover:text-neutral-800"
          >Login</NuxtLink
        >
      </Transition>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  requiresAuth: false,
  redirectIfAuth: true
});

const parts = ref([
  {
    src: "/logo/dev.svg",
    isVisible: false
  },
  {
    src: "/logo/dot.svg",
    isVisible: false
  },
  {
    src: "/logo/ision.svg",
    isVisible: false
  }
]);

const animationDone = ref(false);

onMounted(async () => {
  await new Promise((resolve) => setTimeout(resolve, 500));

  for (let i = 0; i < parts.value.length; i++) {
    setTimeout(() => {
      const part = parts.value[i];
      if (!part) return;

      part.isVisible = true;
      if (i === parts.value.length - 1) setTimeout(() => (animationDone.value = true), 1000);
    }, i * 1000);
  }
});
</script>

<style scoped>
.v-enter-active {
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
}

.v-enter-from {
  opacity: 0;
  transform: translateY(5rem);
}

@keyframes bounce-in {
  0% {
    opacity: 0;
    transform: translateY(100lvh);
  }
  70% {
    transform: translateY(-5lvh);
  }
  85% {
    transform: translateY(5lvh);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.bounce-in {
  animation: bounce-in 1s forwards;
}

@keyframes float {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10lvh);
  }
  100% {
    transform: translateY(0);
  }
}

.float {
  animation: float 6s ease-in-out infinite;
}
</style>
