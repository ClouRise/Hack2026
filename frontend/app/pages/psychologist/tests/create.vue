<template>
  <div class="flex gap-6 items-start">

    <!-- ЛЕВАЯ ПАНЕЛЬ — палитра -->
    <div class="w-52 flex-shrink-0 sticky top-6">
      <div class="bg-white rounded-2xl p-4 card-test-shadows">
        <p class="text-xs G-M text-gray-medium mb-3 uppercase tracking-wider">Типы вопросов</p>
        
        <VueDraggable
          v-model="questionTypes"
          :group="{ name: 'questions', pull: 'clone', put: false }"
          :sort="false"
          :clone="cloneQuestion"
          class="flex flex-col gap-2"
        >
          <div
            v-for="type in questionTypes"
            :key="type.value"
            class="flex items-center gap-2 px-3 py-2 rounded-lg border border-gray-light
                   hover:border-green-bright hover:text-green-dark transition G-M text-gray-medium text-sm
                   cursor-grab active:cursor-grabbing select-none"
          >
            <span>{{ type.icon }}</span>
            <span>{{ type.label }}</span>
          </div>
        </VueDraggable>

      </div>
    </div>

    <!-- ПРАВАЯ ПАНЕЛЬ — конструктор -->
    <div class="flex-1 min-w-0">
      <div class="flex items-center justify-between mb-6">
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
            class="px-4 py-2 border-2 border-gray-light G-M text-gray-medium rounded hover:border-green-dark hover:text-green-dark transition">
            Сохранить черновик
          </button>
          <button @click="handleSave('published')"
            class="px-6 text-lg py-2 bg-green-bright hover:bg-green-dark text-white BP-B rounded transition">
            Опубликовать
          </button>
        </div>
      </div>

      <TestBuilder ref="builderRef" />
    </div>

  </div>
</template>

<script setup lang="ts">
import { VueDraggable } from 'vue-draggable-plus'
import TestBuilder from '~/components/features/test/TestBuilder.vue'
import type { QuestionType } from '~/stores/testBuilder'

definePageMeta({ middleware: [] })

const store = useTestBuilderStore()
const builderRef = ref<InstanceType<typeof TestBuilder> | null>(null)

const questionTypes = shallowRef([
  { value: 'text',            icon: '📝', label: 'Текст' },
  { value: 'textarea',        icon: '📄', label: 'Многострочный' },
  { value: 'single_choice',   icon: '🔘', label: 'Один из списка' },
  { value: 'multiple_choice', icon: '☑️', label: 'Несколько' },
  { value: 'yes_no',          icon: '✅', label: 'Да / Нет' },
  { value: 'number',          icon: '🔢', label: 'Число' },
  { value: 'slider',          icon: '🎚️', label: 'Слайдер' },
  { value: 'date',            icon: '📅', label: 'Дата' },
  { value: 'rating',          icon: '⭐', label: 'Рейтинг' },
])

// Создаём новый вопрос при drop
function cloneQuestion(item: { value: string; icon: string; label: string }) {
  return {
    id: crypto.randomUUID(),
    section_id: '',
    order: 0,
    text: '',
    type: item.value as QuestionType,
    required: true,
    hidden_by_default: false,
    options: item.value === 'yes_no' ? [
      { id: crypto.randomUUID(), text: 'Да', weight: 0, next_question_id: null },
      { id: crypto.randomUUID(), text: 'Нет', weight: 0, next_question_id: null },
    ] : [],
    score_ranges: [],
    min: (item.value === 'slider' || item.value === 'rating') ? 1 : undefined,
    max: (item.value === 'slider' || item.value === 'rating') ? 5 : undefined,
  }
}

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
}
</script>