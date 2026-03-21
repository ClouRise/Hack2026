export const useApi = () => {
  const config = useRuntimeConfig()
  const token = useCookie('token')

  const api = $fetch.create({
    baseURL: config.public.apiBase as string,
    headers: {
      ...(token.value && { Authorization: `Bearer ${token.value}` })
    },
    onResponseError({ response }) {
      if (response.status === 401) {
        token.value = null
        navigateTo('/login')
      }
    }
  })

  return { api }
}