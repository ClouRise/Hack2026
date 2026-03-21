<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm px-6 py-4 flex items-center justify-between">
      <div class="flex items-center gap-4">
        <NuxtLink to="/psychologist/tests/create" class="bg-green-500 px-4 py-1 text-white rounded hover:bg-green-600 text-xl BP-B">
          Создать тест
        </NuxtLink>
        <NuxtLink to="/psychologist/tests" class="text-gray-600 text-green-dark hover:text-gray-main ml-4 text-xl BP-B">
          Мои опросники
        </NuxtLink>
      </div>
        <NuxtLink to="/psychologist" class="text-gray-600 text-bg-red hover:text-gray-main text-xl BP-B">
          Выйти
        </NuxtLink>
    </nav>
    <main class="container mx-auto px-6 py-8">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth';
const authStore = useAuthStore()
</script>