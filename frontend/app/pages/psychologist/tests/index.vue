<template>
  <div>
    <p class="text-sm G-M text-gray-medium mb-4">
      Доступ до: <span class="text-green-dark BP-M">{{ authStore.user?.access_until ?? 'не ограничен' }}</span>
    </p>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl BP-B text-green-dark">Мои опросники</h1>
      <div class="flex items-center gap-3">
        <button
          @click="fileInput?.click()"
          class="px-4 py-2 border-2 border-gray-light text-gray-medium G-M rounded hover:border-green-dark hover:text-green-dark transition"
        >
          Импорт JSON
        </button>
        <NuxtLink
          to="/psychologist/tests/create"
          class="px-6 py-2 bg-green-bright text-white BP-B rounded hover:bg-green-dark transition"
        >
          + Создать тест
        </NuxtLink>
      </div>
    </div>

    <div class="bg-white rounded-2xl overflow-hidden" style="box-shadow: 0 4px 32px rgba(20,66,16,0.10);">
      <table class="w-full">
        <thead class="bg-bg-light border-b border-gray-light">
          <tr>
            <th class="text-left px-6 py-4 text-sm G-M text-gray-medium">Название</th>
            <th class="text-left px-6 py-4 text-sm G-M text-gray-medium">Заполнили</th>
            <th class="text-left px-6 py-4 text-sm G-M text-gray-medium">Последнее заполнение</th>
            <th class="text-left px-6 py-4 text-sm G-M text-gray-medium">Статус</th>
            <th class="text-left px-6 py-4 text-sm G-M text-gray-medium">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="tests.length === 0">
            <td colspan="5" class="text-center py-12 G-M text-gray-light">
              Тестов пока нет. Создайте первый!
            </td>
          </tr>
          <tr
            v-for="test in tests"
            :key="test.id"
            class="border-b border-bg-light hover:bg-bg-light transition"
          >
            <td class="px-6 py-4">
              <p class="BP-M text-green-dark">{{ test.title }}</p>
            </td>
            <td class="px-6 py-4 G-M text-gray-medium">{{ test.submissions_count }}</td>
            <td class="px-6 py-4 G-M text-gray-medium">{{ test.last_submission_at ? formatDate(test.last_submission_at) : '—' }}</td>
            <td class="px-6 py-4">
              <span
                :class="test.status === 'published' ? 'bg-green-light text-green-dark' : 'bg-bg-light text-gray-medium'"
                class="px-3 py-1 rounded-full text-xs G-M"
              >
                {{ test.status === 'published' ? 'Опубликован' : 'Черновик' }}
              </span>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center gap-3 flex-wrap">
                <button @click="copyLink(test)" class="text-sm G-M text-green-bright hover:text-green-dark transition">
                  Скопировать ссылку
                </button>
                <NuxtLink :to="`/psychologist/tests/${test.id}/submissions`" class="text-sm G-M text-gray-medium hover:text-green-dark transition">
                  Результаты
                </NuxtLink>
                <NuxtLink :to="`/psychologist/tests/${test.id}/edit`" class="text-sm G-M text-gray-medium hover:text-green-dark transition">
                  Редактировать
                </NuxtLink>
                <button @click="exportTest(test)" class="text-sm G-M text-gray-medium hover:text-green-dark transition">
                  Экспорт
                </button>
                <button @click="deleteTest(test.id)" class="text-sm G-M text-bg-red hover:text-red-900 transition">
                  Удалить
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <input ref="fileInput" type="file" accept=".json" class="hidden" @change="handleFileImport" />
</template>

<script setup lang="ts">
definePageMeta({
  middleware: []
})

const authStore = useAuthStore()
const fileInput = ref<HTMLInputElement | null>(null)


interface Test {
  id: string
  title: string
  status: 'draft' | 'published'
  submissions_count: number
  last_submission_at: string | null
  token: string | null
}

// Моковые данные пока бэк не готов
const tests = ref<Test[]>([
  {
    id: '1',
    title: 'Тест на профориентацию',
    status: 'published',
    submissions_count: 12,
    last_submission_at: '2026-03-20T10:00:00',

    token: 'abc123'
  },
  {
    id: '2',
    title: 'Тест на тревожность',
    status: 'draft',
    submissions_count: 0,
    last_submission_at: null,
    token: null
  }
])

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('ru-RU')
}

async function copyLink(test: Test) {
  if (!test.token) {
    alert('Сначала опубликуйте тест')
    return
  }
  const link = `${window.location.origin}/test/${test.token}`
  await navigator.clipboard.writeText(link)
  alert('Ссылка скопирована!')
}

async function deleteTest(id: string) {
  if (!confirm('Удалить тест?')) return
  tests.value = tests.value.filter(t => t.id !== id)
  // TODO: подключить API
}

function exportTest(test: Test) {
  // TODO: когда бэк будет готов — загрузить полный тест и экспортировать
  // пока просто экспортируем то что есть
  const json = JSON.stringify(test, null, 2)
  const blob = new Blob([json], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${test.title}.json`
  a.click()
  URL.revokeObjectURL(url)
}

function handleFileImport(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const data = JSON.parse(e.target?.result as string)
      // редиректим на create и загружаем данные
      const store = useTestBuilderStore()
      store.loadFromJson(data)
      navigateTo('/psychologist/tests/create')
    } catch {
      alert('Неверный формат файла')
    }
  }
  reader.readAsText(file)
}

</script>