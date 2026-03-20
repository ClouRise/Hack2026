<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm px-6 py-4 flex items-center justify-between">
      <span class="font-bold text-xl">ПрофДНК</span>
      <div class="flex items-center gap-4">
        <NuxtLink to="/psychologist" class="text-gray-600 hover:text-gray-900">Мои тесты</NuxtLink>
        <NuxtLink to="/psychologist/profile" class="text-gray-600 hover:text-gray-900">Профиль</NuxtLink>
        <button @click="authStore.logout()" class="text-red-500 hover:text-red-700">Выйти</button>
      </div>
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