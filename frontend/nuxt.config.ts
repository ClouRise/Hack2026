// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [tailwindcss()]
  },
  modules: ['@pinia/nuxt'],
  typescript: {
    strict: true
  },
  runtimeConfig: {
  public: {
    apiBase: 'http://localhost:8000'
  }
  },
  srcDir: 'app/',
  nitro: {
    prerender: {
      failOnError: false
    }
  }
})
