import { useAuthStore } from '../stores/auth'

export default defineNuxtRouteMiddleware(() => {
  const authStore = useAuthStore()
  const route = useRoute()

  if (route.path.startsWith('/admin') && !authStore.isAdmin) {
    return navigateTo('/psychologist')
  }

  if (route.path.startsWith('/psychologist') && !authStore.isPsychologist && !authStore.isAdmin) {
    return navigateTo('/login')
  }
})