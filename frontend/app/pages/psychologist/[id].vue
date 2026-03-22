<template>
  <div class="max-w-2xl mx-auto">
    <div class="bg-white rounded-lg p-6 mb-4 card-test-shadows">
      <!-- Фото -->
      <div class="flex items-center gap-6 mb-6">
        <div class="relative">
          <img
                :src="getAvatarUrl(profile?.photo_url)"
                class="w-24 h-24 rounded-full object-cover border-2 border-green-light"
            />
        </div>
        <div>
          <p class="BP-B text-lg text-green-dark">{{ profile?.name }}</p>
          <p class="G-M text-sm text-gray-medium">Психолог</p>
        </div>
      </div>

      <!-- Поля -->
      <div class="flex flex-col gap-3 mb-6">
        <div>
          <label class="block text-[10pt] G-M text-gray-light mb-1">ФИО</label>
          <p class="px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M">{{ profile?.name }}</p>
        </div>
        <div>
          <label class="block text-[10pt] G-M text-gray-light mb-1">Email</label>
          <p class="px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M">{{ profile?.email }}</p>
        </div>
        <div>
          <label class="block text-[10pt] G-M text-gray-light mb-1">Телефон</label>
          <p class="px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M">{{ profile?.phone ?? '—' }}</p>
        </div>
      </div>

      <!-- О себе -->
      <div class="mb-6">
        <label class="block text-[10pt] G-M text-gray-light mb-1">О себе</label>
        <div v-html="renderedAbout" class="px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M"
          style="font-size: 14px; line-height: 1.6;" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { marked } from 'marked'

definePageMeta({
  layout: 'empty'
})

const route = useRoute()
const config = useRuntimeConfig()

const profile = ref<any>(null)

onMounted(async () => {
  try {
    profile.value = await $fetch(`/users/${route.params.id}/profile`, {
      baseURL: config.public.apiBase as string
    })
  } catch (e) {
    console.error('Ошибка загрузки профиля:', e)
  }
})

const renderedAbout = computed(() => {
  return marked(profile.value?.bio ?? '')
})
function getAvatarUrl(url: string | null) {
  if (!url) return '/default-avatar.png'
  if (url.startsWith('http')) return url
  return `${config.public.apiBase}${url}`
}

</script>