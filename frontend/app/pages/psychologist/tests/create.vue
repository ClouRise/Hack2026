<template>
  <div class="flex gap-6 items-start">

    <!-- ЛЕВАЯ ПАНЕЛЬ — аккордеон -->
    <div class="w-52 flex-shrink-0 sticky top-20 flex flex-col gap-2">
      <!-- Секция: Вопросы -->
      <div class="bg-white rounded-2xl card-test-shadows overflow-hidden">
        <button
          @click="toggleQuestions"
          class="w-full flex items-center justify-between px-4 py-3 G-M text-gray-medium hover:text-green-dark transition"
        >
          <span class="text-xs uppercase tracking-wider">Вопросы</span>
          <span class="text-xs">{{ openQuestions ? '▼' : '►' }}</span>
        </button>

        <div v-show="openQuestions" class="px-4 pb-4">
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

      <!-- Секция: Блоки отчёта -->
      <!-- Секция: Блоки отчёта -->
<div class="bg-white rounded-2xl card-test-shadows overflow-hidden">
  <button
    @click="toggleReportBlocks"
    class="w-full flex items-center justify-between px-4 py-3 G-M text-gray-medium hover:text-green-dark transition"
  >
    <span class="text-xs uppercase tracking-wider">Блоки отчёта</span>
    <span class="text-xs">{{ openReportBlocks ? '▼' : '►' }}</span>
  </button>

  <div v-show="openReportBlocks" class="px-4 pb-4 flex flex-col gap-3">

    <!-- Статичные блоки -->
    <VueDraggable
      v-model="reportBlockTypes"
      :group="{ name: 'report-blocks', pull: 'clone', put: false }"
      :sort="false"
      :clone="cloneBlock"
      class="flex flex-col gap-2"
    >
      <div
        v-for="type in reportBlockTypes"
        :key="type.value"
        class="flex items-center gap-2 px-3 py-2 rounded-lg border border-gray-light
               hover:border-green-bright hover:text-green-dark transition G-M text-gray-medium text-sm
               cursor-grab active:cursor-grabbing select-none"
      >
        <span>{{ type.icon }}</span>
        <span>{{ type.label }}</span>
      </div>
    </VueDraggable>

    <!-- Метрики — динамические -->
    <div v-if="store.metrics.length > 0">
  <p class="text-xs G-M text-gray-medium mb-2 uppercase tracking-wider">Метрики</p>
  <div class="max-h-48 overflow-y-auto pr-1">
    <VueDraggable
      v-model="store.metrics"
      :group="{ name: 'report-blocks', pull: 'clone', put: false }"
      :sort="false"
      :clone="cloneMetricBlock"
      class="flex flex-col gap-2"
    >
        <div
          v-for="metric in store.metrics"
          :key="metric.id"
          class="flex items-center gap-2 px-3 py-2 rounded-lg border border-green-light bg-bg-light
                 hover:border-green-bright hover:text-green-dark transition G-M text-green-dark text-sm
                 cursor-grab active:cursor-grabbing select-none"
        >
          <span>📊</span>
          <span class="truncate">{{ metric.name || 'Без названия' }}</span>
        </div>
      </VueDraggable>
    </div>
 </div>

    <p v-else class="text-xs G-M text-gray-light italic">
      Создайте метрики чтобы добавить их в отчёт
    </p>

  </div>
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
import type { QuestionType, ReportBlock, ReportBlockType } from '~/stores/testBuilder'

definePageMeta({ middleware: [] })

const store = useTestBuilderStore()
const builderRef = ref<InstanceType<typeof TestBuilder> | null>(null)



const openQuestions = ref(true)
const openReportBlocks = ref(false)

function toggleQuestions() {
  openQuestions.value = !openQuestions.value
  if (openQuestions.value) openReportBlocks.value = false
}

function toggleReportBlocks() {
  openReportBlocks.value = !openReportBlocks.value
  if (openReportBlocks.value) openQuestions.value = false
}

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

const reportBlockTypes = shallowRef([
  { value: 'text',    icon: '📝', label: 'Текст' },
  { value: 'metric',  icon: '📊', label: 'Метрика' },
  { value: 'chart',   icon: '📈', label: 'График' },
  { value: 'answers', icon: '📋', label: 'Ответы' },
])

function cloneQuestion(item: { value: string }) {
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

function cloneBlock(item: { value: string }): ReportBlock {
  return {
    id: crypto.randomUUID(),
    type: item.value as ReportBlockType,
    content: '',
    metric_id: '',
    chart_type: 'bar',
    metric_ids: [],
    question_ids: [],
    show_all_answers: false
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

function cloneMetricBlock(metric: { id: string; name: string }): ReportBlock {
  return {
    id: crypto.randomUUID(),
    type: 'metric',
    content: '',
    metric_id: metric.id,  // сразу привязываем id метрики
    chart_type: 'bar',
    metric_ids: [],
    question_ids: [],
    show_all_answers: false
  }
}

</script>