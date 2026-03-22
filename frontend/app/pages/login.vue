<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center" :class="isDarkTheme ? 'dark-theme bg-dark' : 'light-theme bg-light'">
    <div class="bg-white rounded-2xl shadow-md p-8 w-full max-w-md card-test-shadows">
            <button @click="toggleTheme"
              class="bg-white px-4 py-2 fixed right-[15px] top-[15px] cursor-pointer rounded-md transition-colors toggle-theme"
              :class="isDarkTheme ? 'sun white-shadow' : 'moon dark-shadow'">
            </button>
      <div class="text-2xl font-bold text-gray-800 mb-6 text-center text-green-dark">
        <img style="clip-path: inset(0 80% 0 0)" class="w-[200px] h-[40px] absolute" src="https://titan-it.pro/wp-content/uploads/2025/03/logo.svg" alt="">
        <img class="w-[200px] h-[40px]" style="clip-path: inset(0 0 0 20%)" :style="isDarkTheme ? '' : 'filter: invert(1);'" src="https://titan-it.pro/wp-content/uploads/2025/03/logo.svg" alt="">
      </div>

      <div class="space-y-4">
        <div>
          <label class="block text-[10pt] text-gray-light G-M mb-1">Логин</label>
          <input
            v-model="form.username"
            type="text"
            placeholder="Введите логин"
            class="w-full px-3 py-2 text-green-dark bg-bg-light border-l-[5px] border-b-[2px] border-gray-light focus:outline-none focus:border-green-bright G-M"
          />
        </div>

        <div>
          <label class="block text-[10pt] text-gray-light G-M mb-1">Пароль</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="Введите пароль"
            class="w-full px-3 py-2 text-green-dark bg-bg-light border-l-[5px] border-b-[2px] border-gray-light focus:outline-none focus:border-green-bright G-M"
          />
        </div>

        <p v-if="error" class="text-rose-400 text-sm text-center">{{ error }}</p>

        <button
          @click="handleLogin"
          :disabled="loading"
          class="bg-green-bright hover:bg-green-bright w-full px-4 py-2 text-white rounded hover:bg-green-600 text-xl BP-B transition disabled:opacity-50"
        >
          {{ loading ? 'Входим...' : 'Войти' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
import { useThemeStore } from '~/stores/theme'
import { storeToRefs } from 'pinia'

const themeStore = useThemeStore()

const { currentTheme, isLightTheme, isDarkTheme } = storeToRefs(themeStore)
const { toggleTheme } = themeStore

definePageMeta({
  layout: false // не используем default layout
})

const authStore = useAuthStore()
const router = useRouter()

const form = reactive({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

async function handleLogin() {
  error.value = ''
  loading.value = true

  try {
    const role = await authStore.login(form.username, form.password)

    if (role === 'admin') {
      router.push('/admin')
    } else {
      router.push('/psychologist')
    }
  } catch (e) {
    error.value = 'Неверный логин или пароль'
  } finally {
    loading.value = false
  }
}
</script>

<style lang="css" scoped>
.dark-shadow{
  box-shadow: 0 0 20px 0 #0000002b;
}
.white-shadow{
  box-shadow: 0 0 20px 0 #ffffff2b;
}
</style>