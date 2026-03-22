<template>
  <div v-if="submission" class="max-w-4xl mx-auto">
    <div class="flex items-center gap-4 mb-6">
      <NuxtLink :to="`/psychologist/tests/${route.params.id}/submissions`" class="G-M text-gray-medium hover:text-green-dark transition">← Назад</NuxtLink>
      <h1 class="text-3xl BP-B text-green-dark">Результат: {{ submission.client_name }}</h1>
    </div>

    <!-- Кнопки отчётов — в колонку на мобилке -->
    <div class="flex flex-col sm:flex-row gap-2 sm:gap-3 mb-6">
      <button @click="downloadReport('docx', 'client')"
        class="px-4 sm:px-6 text-base sm:text-xl py-2 cursor-pointer bg-green-bright text-white BP-B rounded hover:bg-green-dark transition">
        Скачать DOCX (клиент)
      </button>
      <button @click="downloadReport('docx', 'psychologist')"
        class="px-4 sm:px-6 text-base sm:text-xl py-2 cursor-pointer bg-green-bright text-white BP-B rounded hover:bg-green-dark transition">
        Скачать DOCX (психолог)
      </button>
      <button @click="downloadReport('html', 'client')"
        class="px-4 sm:px-6 py-2 cursor-pointer bg-white border-2 border-gray-light text-gray-medium G-M rounded hover:border-green-dark hover:text-green-dark transition text-sm sm:text-base">
        Открыть HTML отчёт
      </button>
    </div>

    <!-- Данные клиента -->
    <div class="bg-white rounded-2xl p-4 sm:p-6 mb-4 sm:mb-7 card-test-shadows">
      <h2 class="text-xl BP-B text-green-dark mb-4">Данные клиента</h2>
      <div class="flex flex-col gap-3">
        <div class="flex gap-2 sm:gap-4">
          <span class="G-M text-gray-medium w-24 sm:w-32 flex-shrink-0 text-sm">ФИО</span>
          <span class="G-M text-green-dark text-sm">{{ submission.client_name }}</span>
        </div>
        <div v-for="(value, key) in submission?.client_name" :key="key" class="flex gap-4">
          <span class="G-M text-gray-medium w-32">{{ key }}</span>
          <span class="G-M text-green-dark">{{ value }}</span>
        </div>
        <div class="flex gap-4">
          <span class="G-M text-gray-medium w-32">Дата</span>
          <span class="G-M text-green-dark">{{ formatDate(submission.completed_at) }}</span>
        </div>
      </div>
    </div>

    <!-- Метрики -->
    <div class="bg-white rounded-2xl p-4 sm:p-6 mb-4 sm:mb-7 card-test-shadows">
      <h2 class="text-xl BP-B text-green-dark mb-4">Результаты метрик</h2>
      <div class="flex flex-col gap-4">
        <div v-for="(metric, key) in submission?.metrics" :key="key" class="border rounded-md border-gray-light p-4">
          <div class="flex items-center justify-between mb-2">
            <span class="BP-M text-green-dark">{{ metric.name }}</span>
            <span class="text-2xl BP-B text-green-bright">{{ metric.value }}</span>
          </div>
          <div class="bg-bg-light p-3 border-l-4 border-green-bright">
            <p class="text-sm G-M text-green-dark">{{ metric.interpretation }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Ответы клиента -->
    <div class="bg-white rounded-2xl p-4 sm:p-6 mb-4 sm:mb-7 card-test-shadows">
      <h2 class="text-xl BP-B text-green-dark mb-4">Ответы на вопросы</h2>
      <div class="flex flex-col gap-4">
        <div v-for="answer in submission.answers" :key="answer.question_id"
          class="border-b border-bg-light pb-4">
          <p class="text-sm G-M text-gray-medium mb-1">{{ answer.question_text }}</p>
          <p class="G-M text-green-dark">{{ formatAnswer(answer.answer_value.answer) }}</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: []
})

const route = useRoute()
const { api } = useApi()

interface Metric {
  name: string
  value: number
  interpretation: string
}

interface Answer {
  question_id: string
  question_text: string
  question_type: string
  answer_value: { answer: any }
  answered_at: string
}

interface Submission {
  session_id: string
  client_name: string
  test_id: string
  completed_at: string | null
  progress: number
  metrics: Record<string, Metric>
  answers: Answer[]
}

const submission = ref<Submission | null>(null)
const testTitle = ref('')

onMounted(async () => {
  try {
    const data = await api(`/users/sessions/${route.params.submissionsId}/answers`) as Submission
    submission.value = data
  } catch (e) {
    console.error('Ошибка загрузки результата:', e)
  }
})

function formatDate(date: string | null) {
  if (!date) return '—'
  return new Date(date).toLocaleString('ru-RU')
}

function formatAnswer(value: any) {
  if (Array.isArray(value)) return value.join(', ')
  return String(value)
}

async function downloadReport(format: 'docx' | 'html', type: 'client' | 'psychologist') {
  console.log('Скачать:', { format, type })
  // TODO: подключить API
}
</script>