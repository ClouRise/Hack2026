import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const token = useCookie('token')
  const user = ref<{
    id: string
    name: string
    role: 'ADMIN' | 'PSYCHOLOGIST'  // бек возвращает uppercase
    email: string
    phone?: string
    access_until?: string | null
    is_blocked?: boolean
  } | null>(null)
  const config = useRuntimeConfig()

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role?.toLowerCase() === 'admin')
  const isPsychologist = computed(() => user.value?.role?.toLowerCase() === 'psychologist')

  async function login(email: string, password: string) {
    const formData = new FormData()
    formData.append('username', email)  // бек ждёт form-data
    formData.append('password', password)

    const response = await $fetch<{ access_token: string }>('/users/token', {
      baseURL: config.public.apiBase as string,
      method: 'POST',
      body: formData,
      credentials: 'include'  // для cookie refresh_token
    })

    token.value = response.access_token
    await fetchProfile()

    return user.value?.role
  }

  async function fetchProfile() {
    user.value = await $fetch<typeof user.value>('/users/me', {
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