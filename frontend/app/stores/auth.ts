import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const token = useCookie('token')
  const user = ref<{ id: number; name: string; role: 'admin' | 'psychologist'; email: string; phone?: string; access_until?: string | null } | null>(null)
  const config = useRuntimeConfig()

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isPsychologist = computed(() => user.value?.role === 'psychologist')

  async function login(username: string, password: string) {
    const response = await $fetch<{ access_token: string; role: string }>('/auth/login', {
      baseURL: config.public.apiBase as string,
      method: 'POST',
      body: { username, password }
    })

    token.value = response.access_token
    await fetchProfile()

    return user.value?.role
  }

  async function fetchProfile() {
    user.value = await $fetch<{ id: number; name: string; role: 'admin' | 'psychologist'; email: string; phone?: string; access_until?: string | null }>('/profile', {
    baseURL: config.public.apiBase as string,
    headers: { Authorization: `Bearer ${token.value}` }
  })
}

  function logout() {
    token.value = null
    user.value = null
    navigateTo('/login')
  }

  return { token, user, isAuthenticated, isAdmin, isPsychologist, login, fetchProfile, logout }
})