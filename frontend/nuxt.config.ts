import tailwindcss from "@tailwindcss/vite";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  modules: ["@pinia/nuxt"],
  css: ["~/assets/main.css"],
  vite: {
    plugins: [tailwindcss()]
  },
  runtimeConfig: {
    public: {
      baseUrl: "",
      backend: ""
    }
  },
  app: {
    head: {
      title: "Devision",
      meta: [
        { charset: "UTF-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1.0" },
        { name: "mobile-web-app-capable", content: "yes" },
        { property: "og:title", content: "Devision" },
        { property: "og:site_name", content: "Devision" },
        { property: "og:type", content: "website" },
        { name: "description", content: "this is NOT discord" },
        { property: "og:description", content: "this is NOT discord" }
      ],
      link: [{ rel: "icon", type: "image/png", href: "/devision-small.png" }],
      htmlAttrs: {
        lang: "en"
      }
    }
  }
});
