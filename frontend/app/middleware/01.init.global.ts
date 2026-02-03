export default defineNuxtRouteMiddleware(async (to) => {
  const nuxtApp = useNuxtApp();
  const userStore = useUserStore();

  if (userStore.isAuth && to.meta.redirectIfAuth) return await navigateTo(`/home`, { redirectCode: 301 });

  // * only run on initial page load
  // https://nuxt.com/docs/guide/directory-structure/middleware#when-middleware-runs
  if (!import.meta.client || !nuxtApp.isHydrating || !nuxtApp.payload.serverRendered) return;

  // TODO: add init call
  await fetchEndpoint("init");

  if (!userStore.isAuth && to.meta.requiresAuth) return await navigateTo("/login", { redirectCode: 301 });
  else if (userStore.isAuth && to.meta.redirectIfAuth) return await navigateTo("/home", { redirectCode: 301 });
});
