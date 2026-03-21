<template>
  <div class="min-h-screen bg-dashboard-page bg-gray-50">
    <nav class="bg-white shadow-sm px-6 py-2 z-[3] w-full flex items-center fixed justify-between">
      <div class="flex items-center gap-4">
        <NuxtLink to="/psychologist/tests/create" class="px-4 py-1 text-white rounded bg-green-bright hover:bg-green-bright text-xl BP-B">
          Создать тест
        </NuxtLink>
        <NuxtLink to="/psychologist/tests" class="text-gray-600 text-green-dark hover:text-gray-main ml-4 text-xl BP-B">
          Мои опросники
        </NuxtLink>
        <NuxtLink to="/psychologist" class="text-gray-600 text-green-dark hover:text-gray-main ml-4 text-xl BP-B">
          Профиль
        </NuxtLink>
      </div>
        <NuxtLink to="/psychologist" class="text-gray-600 text-bg-red hover:text-gray-main text-xl BP-B">
          Выйти
        </NuxtLink>
    </nav>
    <main class="container mx-auto mt-12 px-6 py-8 ">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth';
const authStore = useAuthStore()
</script>

<style lang="css" scoped>
.bg-dashboard-page {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: scroll;
  background-color: #144210;
  background-image: url('../assets/images/elements.svg');
  background-attachment: fixed;
  background-size: cover;
}
</style>