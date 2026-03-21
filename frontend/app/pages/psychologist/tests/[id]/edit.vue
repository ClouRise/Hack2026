<template>
  <div>
    <div class="flex items-center justify-between mb-6 max-w-4xl mx-auto">
      <h1 class="text-3xl BP-B text-green-dark">Редактировать тест</h1>
      <div class="flex gap-3">
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

    <TestBuilder />
  </div>
</template>

<script setup lang="ts">
import TestBuilder from '~/components/features/test/TestBuilder.vue'

definePageMeta({ middleware: [] })

const route = useRoute()
const store = useTestBuilderStore()

onMounted(async () => {
  // TODO: загрузить тест по route.params.id
  // const data = await api(`/tests/${route.params.id}`)
  // store.loadFromJson(data)
})

async function handleSave(status: 'draft' | 'published') {
  const payload = store.buildPayload()
  console.log('Обновляем:', { ...payload, status })
  // TODO: подключить API PUT /tests/${route.params.id}
}
</script>