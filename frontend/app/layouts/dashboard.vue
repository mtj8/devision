<template>
  <div class="flex h-dvh w-dvw flex-col items-center justify-start">
    <AppHeader />

    <div class="flex h-full w-full items-center justify-between overflow-hidden">
      <Sidebar />

      <div class="h-full w-full overflow-y-scroll">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>
