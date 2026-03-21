<template>
  <div>
    <div class="flex items-center gap-4 mb-6">
      <NuxtLink to="/psychologist/tests" class="G-M text-gray-medium hover:text-green-dark transition">← Назад</NuxtLink>
      <h1 class="text-3xl BP-B text-green-dark">{{ testTitle }}</h1>
    </div>

    <div class="bg-white rounded-2xl overflow-hidden mb-4" style="box-shadow: 0 4px 32px rgba(20,66,16,0.10);">
      <table class="w-full">
        <thead class="bg-bg-light border-b border-gray-light">
          <tr>
            <th class="text-left px-6 py-4 text-sm G-M text-gray-medium">Имя клиента</th>
            <th class="text-left px-6 py-4 text-sm G-M text-gray-medium">Дата заполнения</th>
            <th class="text-left px-6 py-4 text-sm G-M text-gray-medium">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="submissions.length === 0">
            <td colspan="3" class="text-center py-12 G-M text-gray-light">
              Прохождений пока нет
            </td>
          </tr>
          <tr
            v-for="submission in submissions"
            :key="submission.id"
            class="border-b border-bg-light hover:bg-bg-light transition"
          >
            <td class="px-6 py-4 BP-M text-green-dark">{{ submission.client_name }}</td>
            <td class="px-6 py-4 G-M text-gray-medium">{{ formatDate(submission.created_at) }}</td>
            <td class="px-6 py-4">
              <div class="flex items-center gap-3 flex-wrap">
                <NuxtLink
                  :to="`/psychologist/tests/${route.params.id}/submissions/${submission.id}`"
                  class="text-sm G-M text-green-bright hover:text-green-dark transition"
                >
                  Смотреть результат
                </NuxtLink>
                <button
                  @click="downloadReport(submission.id, 'docx', 'client')"
                  class="text-sm G-M text-gray-medium hover:text-green-dark transition"
                >
                  DOCX клиент
                </button>
                <button
                  @click="downloadReport(submission.id, 'docx', 'psychologist')"
                  class="text-sm G-M text-gray-medium hover:text-green-dark transition"
                >
                  DOCX психолог
                </button>
                <button
                  @click="downloadReport(submission.id, 'html', 'client')"
                  class="text-sm G-M text-gray-medium hover:text-green-dark transition"
                >
                  HTML
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <button
      @click="fetchSubmissions"
      class="px-4 py-2 border-2 border-gray-light text-gray-medium G-M rounded hover:border-green-dark hover:text-green-dark transition"
    >
      Обновить
    </button>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: []
})

const route = useRoute()

interface Submission {
  id: string
  client_name: string
  created_at: string
}

const testTitle = ref('Тест на профориентацию')
const submissions = ref<Submission[]>([
  { id: '1', client_name: 'Иванов Иван', created_at: '2026-03-20T10:00:00' },
  { id: '2', client_name: 'Петрова Мария', created_at: '2026-03-21T12:00:00' }
])

function formatDate(date: string) {
  return new Date(date).toLocaleString('ru-RU')
}

async function fetchSubmissions() {
  // TODO: GET /tests/{id}/submissions
}

async function downloadReport(submissionId: string, format: 'docx' | 'html', type: 'client' | 'psychologist') {
  // TODO: GET /submissions/{id}/report?format=docx&type=client
  console.log('Скачать отчёт:', { submissionId, format, type })
}
</script>