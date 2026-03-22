<template>
  <div class="max-w-2xl mx-auto">
    <h1 class="text-3xl BP-B text-green-dark mb-6">Личный кабинет</h1>

    <div class="bg-white rounded-lg p-6 mb-4 card-test-shadows" >
      <!-- Фото -->
      <div class="flex items-center gap-6 mb-6">
        <div class="relative">
          <img
            :src="avatar || '/default-avatar.png'"
            class="w-24 h-24 rounded-full object-cover border-2 border-green-light"
          />
          <button
            @click="fileInput?.click()"
            class="absolute bottom-0 right-0 text-white rounded-full w-7 h-7 flex items-center justify-center text-sm bg-green-bright hover:bg-green-bright transition"
          >
            ✎
          </button>
          <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="handleAvatarChange" />
        </div>
        <div>
          <p class="BP-B text-lg text-green-dark">{{ authStore.user?.name }}</p>
          <p class="G-M text-sm text-gray-medium">Психолог</p>
        </div>
      </div>

      <!-- Нередактируемые поля -->
      <div class="flex flex-col gap-3 mb-6">
        <div>
          <label class="block text-[10pt] G-M text-gray-light mb-1">ФИО</label>
          <p class="px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M">{{ authStore.user?.name }}</p>
        </div>
        <div>
          <label class="block text-[10pt] G-M text-gray-light mb-1">Email</label>
          <p class="px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M">{{ authStore.user?.email }}</p>
        </div>
        <div>
          <label class="block text-[10pt] G-M text-gray-light mb-1">Телефон</label>
          <p class="px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M">{{ authStore.user?.phone ?? '—' }}</p>
        </div>
      </div>

      <!-- О себе -->
      <div class="mb-6">
        <label class="block text-[10pt] G-M text-gray-light mb-1">О себе</label>
        <ClientOnly>
          <RichTextEditor v-model="about" />
        </ClientOnly>
      </div>

      <div class="flex items-center justify-between">
        <button
          @click="showBusinessCard = true"
          class="px-4 py-2 text-teal-dark cursor-pointer G-M rounded hover:bg-green-dark hover:text-gray-medium"
        >
          Показать визитку
        </button>
        <button
          @click="handleSave"
          class="px-6 py-1 bg-green-bright cursor-pointer text-lg rounded text-white BP-B hover:bg-green-bright"
        >
          Сохранить
        </button>
      </div>
    </div>
  </div>

  <!-- Модалка визитки -->
  <div v-if="showBusinessCard" class="fixed inset-0 bg-green-dark/70 flex items-center justify-center z-50" @click.self="showBusinessCard = false">
    <div class="bg-white rounded-lg p-8 max-w-sm w-full mx-4 text-center card-test-shadows">
      <img
        :src="avatar || '/default-avatar.png'"
        class="w-20 h-20 rounded-full object-cover mx-auto mb-4 border-2 border-green-light"
      />
      <p class="BP-B text-xl text-green-dark mb-1">{{ authStore.user?.name }}</p>
      <p class="G-M text-gray-medium text-sm mb-4">Психолог</p>
      <div v-html="renderedAbout" class="mb-6 text-left text-green-dark G-M"
        style="font-size: 14px; line-height: 1.6;" />
      <img :src="qrCodeUrl" class="mx-auto mb-4" />
      <p class="text-xs text-gray-light G-M">Отсканируйте для перехода на страницу психолога</p>
      <button @click="showBusinessCard = false" class="mt-4 text-sm G-M text-gray-medium hover:text-green-dark transition">Закрыть</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { marked } from 'marked'
import RichTextEditor from '~/components/ui/RichTextEditor.vue'

definePageMeta({
  middleware: []
})

useHead({
  link: [
    { rel: 'stylesheet', href: 'https://cdn.quilljs.com/1.3.6/quill.snow.css' }
  ]
})

const authStore = useAuthStore()

const about = ref('')
const avatar = ref<string | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const showBusinessCard = ref(false)

let saveTimeout: ReturnType<typeof setTimeout> | null = null

watch(about, () => {
  if (saveTimeout) clearTimeout(saveTimeout)
  saveTimeout = setTimeout(() => {
    handleSave()
  }, 1000)
})

// QR код через бесплатный API
const qrCodeUrl = computed(() => {
  const url = `${window.location.origin}/psychologist/${authStore.user?.id}`
  return `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(url)}`
})

// Простой рендер markdown — жирный и курсив
const renderedAbout = computed(() => {
  return marked(about.value)
})

function handleAvatarChange(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (e) => {
    avatar.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
}

const { api } = useApi()

async function handleSave() {
  try {
    const formData = new FormData()
    formData.append('bio', about.value)
    if (authStore.user?.phone) {
      formData.append('phone', authStore.user.phone)
    }

    // Если есть файл — добавляем
    const file = fileInput.value?.files?.[0]
    if (file) {
      formData.append('photo', file)
    }

    await api('/users/me', {
      method: 'PATCH',
      body: formData
    })
  } catch (e) {
    console.error('Ошибка сохранения:', e)
    alert('Ошибка при сохранении')
  }
}

onMounted(async () => {
  try {
    const profile = await api('/users/me') as any
    about.value = profile.bio ?? ''
    avatar.value = profile.photo_url ?? null
  } catch (e) {
    console.error('Ошибка загрузки профиля:', e)
  }
})
</script>

<style>
.ql-align-center {
  text-align: center;
}
.ql-align-right {
  text-align: right;
}
.ql-align-justify {
  text-align: justify;
}

ol, ul {
  padding-left: 1.5rem;
}
ul {
  list-style-type: disc;
}
ol {
  list-style-type: decimal;
}
</style>