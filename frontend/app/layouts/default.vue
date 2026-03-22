<template>
  <div class="min-h-screen bg-dashboard-page bg-gray-50">
    <nav class="bg-white shadow-sm px-6 py-2 z-[3] w-full flex items-center fixed justify-between">
      <div class="flex items-center gap-4">
        <NuxtLink to="/psychologist/tests/create"
          class="px-4 py-1 text-white rounded bg-green-bright hover:bg-green-bright text-xl BP-B">
          Создать тест
        </NuxtLink>
        <NuxtLink to="/psychologist/tests" class=" text-green-dark hover:text-gray-medium ml-4 text-xl BP-B">
          Мои опросники
        </NuxtLink>
        <NuxtLink to="/psychologist" class=" text-green-dark hover:text-gray-medium ml-4 text-xl BP-B">
          Профиль
        </NuxtLink>
      </div>
      <div class="flex items-center">
        <button @click="toggleTheme" class="bg-white px-4 py-2 mr-6 cursor-pointer rounded-md transition-colors toggle-theme"
          :class="isDarkTheme ? 'sun' : 'moon'">

        </button>
        <NuxtLink to="/psychologist" class="text-red-800 hover:text-red-600 text-xl BP-B">
          Выйти
        </NuxtLink>
      </div>

    </nav>
    <main class="container mx-auto mt-12 px-6 py-8 ">
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
