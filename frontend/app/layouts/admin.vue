<template>
  <div class="min-h-screen bg-dashboard-page bg-gray-50">
    <main class="container relative mx-auto mt-6 px-6 py-8 ">
        <button @click="toggleTheme" class="bg-white px-4 py-2 fixed mt-14 top-[0px] right-[15px] cursor-pointer rounded-md transition-colors toggle-theme"
      :class="isDarkTheme ? 'sun' : 'moon'">
      
    </button>
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth';
const authStore = useAuthStore()

import { useThemeStore } from '~/stores/theme'
import { storeToRefs } from 'pinia'

const themeStore = useThemeStore()

const { currentTheme, isLightTheme, isDarkTheme } = storeToRefs(themeStore)
const { toggleTheme } = themeStore

watch(currentTheme, (newTheme) => {
  if (process.client) {
    document.body.className = newTheme
  }
}, { immediate: true })
</script>
