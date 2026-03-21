<template>
  <NuxtLayout :class="isDarkTheme ? 'dark-theme bg-dark' : 'light-theme bg-light'">
    <button @click="toggleTheme" class="bg-white px-4 py-2 fixed top-[70px] right-[15px] cursor-pointer rounded-md transition-colors toggle-theme"
      :class="isDarkTheme ? 'sun' : 'moon'">
      
    </button>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup>
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

<style>
.bg-light {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: scroll;
  background-color: #144210;
  background-image: url('./assets/images/elements.svg');
  background-attachment: fixed;
  background-size: cover;
}
.bg-dark {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: scroll;
  background-color: #144210;
  background-image: url('./assets/images/bg-dark.svg');
  background-attachment: fixed;
  background-size: cover;
}
.sun{
  background-image: url('./assets/images/sun.svg');
}
.moon{
  background-image: url('./assets/images/moon.svg');
}
.toggle-theme{
  background-size: 70%;
  background-position: center;
  width: 50px;
  height: 50px;
  background-repeat: no-repeat;
  border: 2px solid var(--color-bg-light);
}
</style>
