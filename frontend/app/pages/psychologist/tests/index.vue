<template>
  <div>
    <p class="text-sm G-M text-gray-medium mb-4">
      Доступ до: <span class="text-green-dark text-lg BP-M">{{ authStore.user?.access_until ?? 'не ограничен' }}</span>
    </p>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl BP-B text-green-dark">Мои опросники</h1>
      <div class="flex items-center gap-3">
        <button @click="fileInput?.click()"
          class="px-4 py-2 border-2 border-gray-light bg-white text-gray-medium G-M rounded hover:border-green-dark hover:text-green-dark transition">
          Импорт JSON
        </button>
        <NuxtLink to="/psychologist/tests/create"
          class="px-6 py-2 text-white text-xl BP-B rounded bg-green-bright hover:bg-green-bright transition">
          + Создать тест
        </NuxtLink>
      </div>
    </div>

    <div class="bg-white rounded-lg overflow-hidden card-test-shadows">
      <table class="w-full">
        <thead class="bg-bg-light border-b border-gray-light">
          <tr>
            <th class="text-left px-6 py-3 leading-[1.1] w-48 text-lg G-M text-gray-medium">Название</th>
            <th class="text-left px-6 py-3 leading-[1.1] w-32 text-sm G-M text-gray-medium">Прошли</th>
            <th class="text-left px-6 py-3 leading-[1.1] w-48 text-sm G-M text-gray-medium">Последнее заполнение</th>
            <th class="text-left px-6 py-3 leading-[1.1] text-sm G-M text-gray-medium">Статус</th>
            <th class="text-left px-6 py-3 leading-[1.1] text-sm G-M text-gray-medium">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="tests.length === 0">
            <td colspan="5" class="text-center py-12 G-M text-gray-light">
              Тестов пока нет. Создайте первый!
            </td>
          </tr>
          <tr v-for="test in tests" :key="test.id" class="border-b border-bg-light hover:bg-bg-light transition">
            <td class="px-6 py-4">
              <p class="BP-B leading-[1.1] text-lg text-green-dark">{{ test.title }}</p>
            </td>
            <td class="px-6 py-4 G-M text-gray-medium">{{ test.submissions_count }}</td>
            <td class="px-6 py-4 G-M text-gray-medium">{{ test.last_submission_at ? formatDate(test.last_submission_at)
              : '—' }}</td>
            <td class="px-6 py-4">
              <span
                :class="test.status === 'published' ? 'bg-bg-light border-l-[5px] border-green-bright text-green-dark2' : 'bg-bg-light border-l-[5px] border-gray-light text-gray-medium'"
                class="px-3 py-2 text-xs G-M">
                {{ test.status === 'published' ? 'Опубликован' : 'Черновик' }}
              </span>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center justify-between gap-4">
                <!-- Левая часть - текстовые ссылки -->
                <div class="flex items-center gap-3">
                  <button @click="copyLink(test)"
                    class="text-sm G-M cursor-pointer text-green-bright hover:text-green-dark transition whitespace-nowrap">
                    Скопировать ссылку
                  </button>
                  <NuxtLink :to="`/psychologist/tests/${test.id}/submissions`"
                    class="text-sm G-M text-gray-medium hover:text-green-dark transition whitespace-nowrap">
                    Результаты
                  </NuxtLink>
                </div>

                <!-- Правая часть - иконки -->
                <div class="flex items-center gap-2">
                  <NuxtLink :to="`/psychologist/tests/${test.id}/edit`"
                    class="edit-icon bg-gray-light rounded w-8 h-8 flex items-center justify-center hover:bg-gray-200 transition">
                  </NuxtLink>
                  <button @click="exportTest(test)"
                    class="export-icon bg-gray-light rounded w-8 h-8 flex items-center justify-center hover:bg-gray-200 transition cursor-pointer">
                  </button>
                  <button @click="deleteTest(test.id)"
                    class="trash-icon bg-red-400 hover:bg-red-500 rounded w-8 h-8 flex items-center justify-center transition cursor-pointer">
                  </button>
                </div>
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