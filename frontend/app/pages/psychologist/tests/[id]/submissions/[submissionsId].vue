<template>
  <div class="max-w-4xl mx-auto">
    <div class="flex items-center gap-4 mb-6">
      <NuxtLink :to="`/psychologist/tests/${route.params.id}/submissions`" class="G-M text-gray-medium hover:text-green-dark transition">← Назад</NuxtLink>
      <h1 class="text-3xl BP-B text-green-dark">Результат: {{ submission.client_name }}</h1>
    </div>

    <!-- Кнопки отчётов -->
    <div class="flex gap-3 mb-6 flex-wrap">
      <button @click="downloadReport('docx', 'client')" class="px-6 text-xl py-2 cursor-pointer bg-green-bright text-white BP-B rounded hover:bg-green-dark transition">
        Скачать DOCX (клиент)
      </button>
      <button @click="downloadReport('docx', 'psychologist')" class="px-6 text-xl cursor-pointer py-2 bg-green-bright text-white BP-B rounded hover:bg-green-dark transition">
        Скачать DOCX (психолог)
      </button>
      <button @click="downloadReport('html', 'client')" class="px-6 bg-white py-2 cursor-pointer border-2 border-gray-light text-gray-medium G-M rounded hover:border-green-dark hover:text-green-dark transition">
        Открыть HTML отчёт
      </button>
    </div>

    <!-- Данные клиента -->
    <div class="bg-white rounded-2xl p-6 mb-7 card-test-shadows">
      <h2 class="text-xl BP-B text-green-dark mb-4">Данные клиента</h2>
      <div class="flex flex-col gap-3">
        <div class="flex gap-4">
          <span class="G-M text-gray-medium w-32">ФИО</span>
          <span class="G-M text-green-dark">{{ submission.client_name }}</span>
        </div>
        <div v-for="(value, key) in submission.client_data" :key="key" class="flex gap-4">
          <span class="G-M text-gray-medium w-32">{{ key }}</span>
          <span class="G-M text-green-dark">{{ value }}</span>
        </div>
        <div class="flex gap-4">
          <span class="G-M text-gray-medium w-32">Дата</span>
          <span class="G-M text-green-dark">{{ formatDate(submission.created_at) }}</span>
        </div>
      </div>
    </div>

    <!-- Метрики -->
    <div class="bg-white rounded-2xl p-6 mb-7 card-test-shadows">
      <h2 class="text-xl BP-B text-green-dark mb-4">Результаты метрик</h2>
      <div class="flex flex-col gap-4">
        <div v-for="metric in submission.metrics" :key="metric.name" class="border rounded-md border-gray-light p-4">
          <div class="flex items-center justify-between mb-2">
            <span class="BP-M text-green-dark">{{ metric.name }}</span>
            <span class="text-2xl BP-B text-green-bright">{{ metric.value }}</span>
          </div>
          <div v-if="metric.interpretation" class="bg-bg-light p-3 border-l-4 border-green-bright">
            <p class="text-sm G-M text-green-dark">{{ metric.interpretation.label }}</p>
            <p class="text-sm G-Book text-gray-medium mt-1">{{ metric.interpretation.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Ответы клиента -->
    <div class="bg-white rounded-2xl p-6 mb-7 card-test-shadows">
      <h2 class="text-xl BP-B text-green-dark mb-4">Ответы на вопросы</h2>
      <div class="flex flex-col gap-4">
        <div v-for="answer in submission.answers" :key="answer.question_id" class="border-b border-bg-light pb-4">
          <p class="text-sm G-M text-gray-medium mb-1">{{ answer.question_text }}</p>
          <p class="G-M text-green-dark">{{ formatAnswer(answer.value) }}</p>
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

interface MetricResult {
  name: string
  value: number
  interpretation: {
    label: string
    description: string
  } | null
}

interface Answer {
  question_id: string
  question_text: string
  value: string | string[] | number
}

interface Submission {
  id: string
  client_name: string
  client_data: Record<string, string>
  created_at: string
  metrics: MetricResult[]
  answers: Answer[]
}

const submission = ref<Submission>({
  id: '1',
  client_name: 'Иванов Иван',
  client_data: { email: 'ivan@example.com' },
  created_at: '2026-03-21T10:00:00',
  metrics: [
    {
      name: 'Уровень тревожности',
      value: 15,
      interpretation: {
        label: 'Высокий уровень',
        description: 'Рекомендуется обратиться к специалисту.'
      }
    },
    {
      name: 'Энергичность',
      value: 8,
      interpretation: {
        label: 'Средний уровень',
        description: 'Всё в норме, поддерживайте режим.'
      }
    }
  ],
  answers: [
    { question_id: '1', question_text: 'Как вы себя чувствуете?', value: 'Хорошо' },
    { question_id: '2', question_text: 'Оцените уровень стресса', value: 7 },
    { question_id: '3', question_text: 'Выберите подходящее', value: ['Вариант А', 'Вариант Б'] }
  ]
})

function formatDate(date: string) {
  return new Date(date).toLocaleString('ru-RU')
}

function formatAnswer(value: string | string[] | number) {
  if (Array.isArray(value)) return value.join(', ')
  return String(value)
}

async function downloadReport(format: 'docx' | 'html', type: 'client' | 'psychologist') {
  console.log('Скачать:', { format, type })
  // TODO: подключить API
}
</script>