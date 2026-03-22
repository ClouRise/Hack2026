<template>
  <div>
    <!-- Шапка -->
    <div class="mb-6">
      <NuxtLink to="/psychologist/tests" class="G-M text-gray-medium hover:text-green-dark transition text-sm">
        ← Назад
      </NuxtLink>
      <h1 class="text-2xl sm:text-3xl BP-B text-green-dark mt-1">{{ testTitle }}</h1>
    </div>

    <!-- ДЕСКТОП (md+): таблица -->
    <div class="hidden md:block bg-white rounded-2xl overflow-hidden mb-4"
      style="box-shadow: 0 4px 32px rgba(20,66,16,0.10);">
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
          <tr v-for="submission in submissions" :key="submission.id"
            class="border-b border-bg-light hover:bg-bg-light transition">
            <td class="px-6 py-4 BP-M text-green-dark text-lg">{{ submission.client_name }}</td>
            <td class="px-6 py-4 G-M text-gray-medium">{{ formatDate(submission.created_at) }}</td>
            <td class="px-6 py-4">
              <div class="flex items-center gap-3 flex-wrap">
                <NuxtLink :to="`/psychologist/tests/${route.params.id}/submissions/${submission.id}`"
                  class="text-sm cursor-pointer G-M text-green-bright hover:text-green-dark transition">
                  Смотреть результат
                </NuxtLink>
                <button @click="downloadReport(submission.id, 'docx', 'client')"
                  class="text-sm cursor-pointer G-M text-gray-medium hover:text-green-dark transition">
                  DOCX клиент
                </button>
                <button @click="downloadReport(submission.id, 'docx', 'psychologist')"
                  class="text-sm G-M cursor-pointer text-gray-medium hover:text-green-dark transition">
                  DOCX психолог
                </button>
                <button @click="downloadReport(submission.id, 'html', 'client')"
                  class="text-sm G-M cursor-pointer text-gray-medium hover:text-green-dark transition">
                  HTML
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- МОБИЛЬНЫЙ + ПЛАНШЕТ (< md): карточки -->
    <div class="md:hidden flex flex-col gap-3 mb-4">
      <div v-if="submissions.length === 0"
        class="bg-white rounded-2xl p-8 text-center G-M text-gray-light"
        style="box-shadow: 0 4px 32px rgba(20,66,16,0.10);">
        Прохождений пока нет
      </div>

      <div v-for="submission in submissions" :key="submission.id"
        class="bg-white rounded-2xl p-3 flex flex-col gap-3"
        style="box-shadow: 0 4px 32px rgba(20,66,16,0.10);">

        <!-- Имя + дата -->
        <div class="flex items-start justify-between gap-2">
          <p class="BP-M text-base text-green-dark leading-[1.2]">{{ submission.client_name }}</p>
          <span class="flex-shrink-0 text-xs G-M text-gray-medium">
            {{ formatDate(submission.created_at) }}
          </span>
        </div>

        <!-- Действия -->
        <div class="flex flex-col gap-2 border-t border-bg-light pt-2">
          <NuxtLink :to="`/psychologist/tests/${route.params.id}/submissions/${submission.id}`"
            class="text-sm cursor-pointer G-M text-green-bright hover:text-green-dark transition">
            Смотреть результат
          </NuxtLink>
          <div class="flex items-center gap-3">
            <button @click="downloadReport(submission.id, 'docx', 'client')"
              class="text-xs cursor-pointer G-M text-gray-medium hover:text-green-dark transition">
              DOCX клиент
            </button>
            <button @click="downloadReport(submission.id, 'docx', 'psychologist')"
              class="text-xs G-M cursor-pointer text-gray-medium hover:text-green-dark transition">
              DOCX психолог
            </button>
            <button @click="downloadReport(submission.id, 'html', 'client')"
              class="text-xs G-M cursor-pointer text-gray-medium hover:text-green-dark transition">
              HTML
            </button>
          </div>
        </div>
      </div>
    </div>

    <button @click="fetchSubmissions"
      class="px-4 py-2 border-2 border-gray-light bg-white text-gray-medium G-M rounded hover:border-green-dark hover:text-green-dark transition text-sm">
      Обновить
    </button>
  </div>
</template>
<script setup lang="ts">
definePageMeta({
  middleware: ['auth']
})
const route = useRoute()

interface Submission {
  id: string
  client_name: string
  created_at: string
}

const testTitle = ref('')
const submissions = ref<Submission[]>([])

function formatDate(date: string) {
  return new Date(date).toLocaleString('ru-RU')
}

const { api } = useApi()
const authStore = useAuthStore()

onMounted(async () => {
  await authStore.fetchProfile()
  await fetchSubmissions()
})

async function fetchSubmissions() {
  try {
    const result = await api(`/users/my_tests/${authStore.user?.id}`) as any
    const test = result.мои_опросники.find((t: any) => t.id === route.params.id)
    
    if (test) {
      testTitle.value = test.название
      submissions.value = test.список_прошедших.map((s: any) => ({
        id: s.id_session,
        client_name: s.фио,
        created_at: s.дата_заполнения ?? new Date().toISOString()
      }))
    }
  } catch (e) {
    console.error('Ошибка загрузки:', e)
  }
}
async function downloadReport(submissionId: string, format: 'docx' | 'html', type: 'client' | 'psychologist') {
  try {
    const endpoint = type === 'client'
      ? `/guest/sessions/${submissionId}/report`
      : `/psychologist/sessions/${submissionId}/report`

    const baseURL = useRuntimeConfig().public.apiBase as string
    const response = await fetch(`${baseURL}${endpoint}`, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })

    const blob = await response.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `report_${type}.docx`
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    console.error('Ошибка скачивания:', e)
    alert('Ошибка при скачивании отчёта')
  }
}
</script>