<template>
  <div class="min-h-screen bg-dashboard-page bg-gray-50">
    <nav class="bg-white shadow-sm px-4 sm:px-6 py-2 z-[3] w-full flex items-center fixed justify-between">

      <!-- Десктоп навигация -->
      <div class="hidden sm:flex items-center gap-4">
        <NuxtLink to="/psychologist/tests/create"
          class="px-4 py-1 text-white rounded bg-green-bright hover:bg-green-bright text-xl BP-B">
          Создать тест
        </NuxtLink>
        <NuxtLink to="/psychologist/tests" class="text-green-dark hover:text-gray-medium ml-4 text-xl BP-B">
          Мои опросники
        </NuxtLink>
        <NuxtLink to="/psychologist" class="text-green-dark hover:text-gray-medium ml-4 text-xl BP-B">
          Профиль
        </NuxtLink>
      </div>

      <!-- Мобильный логотип / название -->
      <div class="sm:hidden">
        <NuxtLink to="/psychologist/tests/create"
          class="px-3 py-1 text-white rounded bg-green-bright text-base BP-B">
          Создать тест
        </NuxtLink>
      </div>

      <!-- Правая часть -->
      <div class="flex items-center gap-2">
        <button @click="toggleTheme"
          class="bg-white px-3 py-2 cursor-pointer rounded-md transition-colors toggle-theme"
          :class="isDarkTheme ? 'sun' : 'moon'">
        </button>

        <!-- Десктоп: Выйти -->
        <NuxtLink to="/psychologist" class="hidden sm:block text-red-800 hover:text-red-600 text-xl BP-B ml-4">
          Выйти
        </NuxtLink>

        <!-- Мобильный бургер -->
        <button @click="mobileNavOpen = !mobileNavOpen"
          class="sm:hidden flex flex-col justify-center items-center w-9 h-9 gap-[5px] rounded-md border border-gray-light">
          <span class="block w-5 h-[2px] bg-gray-medium transition-all"
            :class="mobileNavOpen ? 'rotate-45 translate-y-[7px]' : ''"></span>
          <span class="block w-5 h-[2px] bg-gray-medium transition-all"
            :class="mobileNavOpen ? 'opacity-0' : ''"></span>
          <span class="block w-5 h-[2px] bg-gray-medium transition-all"
            :class="mobileNavOpen ? '-rotate-45 -translate-y-[7px]' : ''"></span>
        </button>
      </div>
    </nav>

    <!-- Мобильное выпадающее меню -->
    <div v-if="mobileNavOpen"
      class="sm:hidden fixed top-[60px] left-0 right-0 z-[50] bg-white border-b border-gray-light shadow-md flex flex-col">
      <NuxtLink to="/psychologist/tests" @click="mobileNavOpen = false"
        class="px-6 py-4 text-green-dark BP-B text-base border-b border-gray-light hover:bg-bg-light">
        Мои опросники
      </NuxtLink>
      <NuxtLink to="/psychologist" @click="mobileNavOpen = false"
        class="px-6 py-4 text-green-dark BP-B text-base border-b border-gray-light hover:bg-bg-light">
        Профиль
      </NuxtLink>
      <NuxtLink to="/psychologist" @click="mobileNavOpen = false"
        class="px-6 py-4 text-red-800 BP-B text-base hover:bg-bg-light">
        Выйти
      </NuxtLink>
    </div>

    <main class="container mx-auto mt-12 px-4 sm:px-6 py-8">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
const authStore = useAuthStore()
import { useThemeStore } from '~/stores/theme'
import { storeToRefs } from 'pinia'

const themeStore = useThemeStore()
const { currentTheme, isLightTheme, isDarkTheme } = storeToRefs(themeStore)
const { toggleTheme } = themeStore

const mobileNavOpen = ref(false)

// Закрывать меню при смене роута
const route = useRoute()
watch(() => route.path, () => { mobileNavOpen.value = false })

watch(currentTheme, (newTheme) => {
  if (process.client) {
    document.body.className = newTheme
  }
}, { immediate: true })
</script>