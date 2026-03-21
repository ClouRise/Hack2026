<template>
  <div>
    <div class="flex items-center justify-between mb-6 max-w-4xl mx-auto">
      <h1 class="text-3xl BP-B text-green-dark">Новый тест</h1>
      <div class="flex gap-3">
        <button @click="builderRef?.fileInput?.click()"
          class="px-4 py-2 border-2 border-gray-light G-M text-gray-medium rounded hover:border-green-dark hover:text-green-dark transition">
          Импорт JSON
        </button>
        <button @click="handleExport"
          class="px-4 py-2 border-2 border-gray-light G-M text-gray-medium rounded hover:border-green-dark hover:text-green-dark transition">
          Экспорт JSON
        </button>
        <button @click="handleSave('draft')"
          class="px-4 py-2 border-2 border-green-dark G-M text-green-dark rounded hover:bg-green-dark hover:text-bg-light transition">
          Сохранить черновик
        </button>
        <button @click="handleSave('published')"
          class="px-6 py-2 bg-green-bright text-white BP-B rounded hover:bg-green-dark transition">
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