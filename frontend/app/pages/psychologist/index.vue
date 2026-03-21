<template>
  <div class="max-w-2xl mx-auto">
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Личный кабинет</h1>

    <div class="bg-white rounded-2xl shadow-sm p-6 mb-4">
      <!-- Фото -->
      <div class="flex items-center gap-6 mb-6">
        <div class="relative">
          <img
            :src="avatar || '/default-avatar.png'"
            class="w-24 h-24 rounded-full object-cover border border-gray-200"
          />
          <button
            @click="fileInput?.click()"
            class="absolute bottom-0 right-0 bg-blue-600 text-white rounded-full w-7 h-7 flex items-center justify-center text-sm hover:bg-blue-700"
          >
            ✎
          </button>
          <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="handleAvatarChange" />
        </div>
        <div>
          <p class="font-semibold text-lg text-gray-800">{{ authStore.user?.name }}</p>
          <p class="text-sm text-gray-500">Психолог</p>
        </div>
      </div>

      <!-- Нередактируемые поля -->
      <div class="flex flex-col gap-3 mb-6">
        <div>
          <label class="block text-sm font-medium text-gray-500 mb-1">ФИО</label>
          <p class="px-4 py-2 bg-gray-50 rounded-lg text-gray-700">{{ authStore.user?.name }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-500 mb-1">Email</label>
          <p class="px-4 py-2 bg-gray-50 rounded-lg text-gray-700">{{ authStore.user?.email }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-500 mb-1">Телефон</label>
          <p class="px-4 py-2 bg-gray-50 rounded-lg text-gray-700">{{ authStore.user?.phone ?? '—' }}</p>
        </div>
      </div>

      <!-- О себе -->
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-1">О себе</label>
        <p class="text-xs text-gray-400 mb-2">Поддерживается Markdown: **жирный**, *курсив*, # заголовок</p>
        <ClientOnly>
          <RichTextEditor v-model="about" />
        </ClientOnly>
      </div>

      <div class="flex items-center justify-between">
        <button
          @click="showBusinessCard = true"
          class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
        >
          Показать визитку
        </button>
        <button
          @click="handleSave"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Сохранить
        </button>
      </div>
    </div>
  </div>

  <!-- Модалка визитки -->
  <div v-if="showBusinessCard" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showBusinessCard = false">
    <div class="bg-white rounded-2xl p-8 max-w-sm w-full mx-4 text-center">
      <img
        :src="avatar || '/default-avatar.png'"
        class="w-20 h-20 rounded-full object-cover mx-auto mb-4 border border-gray-200"
      />
      <p class="font-bold text-xl mb-1">{{ authStore.user?.name }}</p>
      <p class="text-gray-500 text-sm mb-4">Психолог</p>
      <div v-html="renderedAbout" class="mb-6 text-left"
      style="font-size: 14px; line-height: 1.6;"/>   
       <!-- QR код -->
      <img :src="qrCodeUrl" class="mx-auto mb-4" />
      <p class="text-xs text-gray-400">Отсканируйте для перехода на страницу психолога</p>
      <button @click="showBusinessCard = false" class="mt-4 text-sm text-gray-500 hover:text-gray-700">Закрыть</button>
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

async function handleSave() {
  console.log('Сохраняем профиль:', { about: about.value, avatar: avatar.value })
  // TODO: подключить API
  alert('Профиль сохранён!')
}
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