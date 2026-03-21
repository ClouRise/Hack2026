<template>
  <div>
    <div class="flex items-center gap-3">
        <button
            @click="fileInput?.click()"
            class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
        >
            Импорт JSON
        </button>
        <NuxtLink
            to="/psychologist/tests/create"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
            + Создать тест
        </NuxtLink>
    </div>

    <!-- Таблица тестов -->
    <div class="bg-white rounded-2xl shadow-sm overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">Название</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">Заполнили</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">Последнее заполнение</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">Статус</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="tests.length === 0">
            <td colspan="5" class="text-center py-12 text-gray-400">
              Тестов пока нет. Создайте первый!
            </td>
          </tr>
          <tr
            v-for="test in tests"
            :key="test.id"
            class="border-b border-gray-100 hover:bg-gray-50"
          >
            <td class="px-6 py-4">
              <p class="font-medium text-gray-800">{{ test.title }}</p>
            </td>
            <td class="px-6 py-4 text-gray-600">{{ test.submissions_count }}</td>
            <td class="px-6 py-4 text-gray-600">{{ test.last_submission_at ? formatDate(test.last_submission_at) : '—' }}</td>
            <td class="px-6 py-4">
              <span
                :class="test.status === 'published' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'"
                class="px-2 py-1 rounded-full text-xs font-medium"
              >
                {{ test.status === 'published' ? 'Опубликован' : 'Черновик' }}
              </span>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center gap-2">
                <button
                  @click="copyLink(test)"
                  class="text-sm text-blue-500 hover:text-blue-700"
                >
                  Скопировать ссылку
                </button>
                <NuxtLink
                  :to="`/psychologist/tests/${test.id}/submissions`"
                  class="text-sm text-gray-500 hover:text-gray-700"
                >
                  Результаты
                </NuxtLink>
                <NuxtLink
                  :to="`/psychologist/tests/${test.id}/edit`"
                  class="text-sm text-gray-500 hover:text-gray-700"
                >
                  Редактировать
                </NuxtLink>
                <button
                  @click="deleteTest(test.id)"
                  class="text-sm text-red-400 hover:text-red-600"
                >
                  Удалить
                </button>
                <button
                @click="exportTest(test)"
                class="text-sm text-gray-500 hover:text-gray-700"
                >
                Экспорт
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