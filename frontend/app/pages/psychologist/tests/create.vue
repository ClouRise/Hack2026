<template>
    
  <div>
    <div class="flex items-center justify-between mb-6 max-w-4xl mx-auto">
      <h1 class="text-2xl font-bold text-gray-800">Новый тест</h1>
      <div class="flex gap-3">
        <button @click="builderRef?.fileInput?.click()"
          class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50">
          Импорт JSON
        </button>
        <button @click="handleExport"
          class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50">
          Экспорт JSON
        </button>
        <button @click="handleSave('draft')"
          class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50">
          Сохранить черновик
        </button>
        <button @click="handleSave('published')"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          Опубликовать
        </button>
      </div>
    </div>

    <TestBuilder ref="builderRef" />
  </div>
</template>

<script setup lang="ts">
import TestBuilder from '~/components/features/test/TestBuilder.vue'

definePageMeta({ middleware: [] })

const store = useTestBuilderStore()
const builderRef = ref<InstanceType<typeof TestBuilder> | null>(null)

onMounted(() => {
  if (!store.meta.title && store.sections.length === 0) {
    store.reset()
  }
})

function handleExport() {
  const payload = store.buildPayload()
  const json = JSON.stringify(payload, null, 2)
  const blob = new Blob([json], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${store.meta.title || 'test'}.json`
  a.click()
  URL.revokeObjectURL(url)
}

async function handleSave(status: 'draft' | 'published') {
  const payload = store.buildPayload()
  console.log('Сохраняем:', { ...payload, status })
  // TODO: подключить API
}
</script>