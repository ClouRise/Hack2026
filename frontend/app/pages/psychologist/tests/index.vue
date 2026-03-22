<template>
  <div>
    <p class="text-sm G-M text-gray-medium mb-4">
      Доступ до: <span class="text-green-dark text-lg BP-M">{{ authStore.user?.access_until ?? 'не ограничен' }}</span>
    </p>

    <!-- Шапка -->
    <div class="mb-6">
      <h1 class="text-2xl sm:text-3xl BP-B text-green-dark mb-3">Мои опросники</h1>
      <div class="flex items-center gap-2">
        <button @click="fileInput?.click()"
          class="px-3 py-2 border-2 border-gray-light bg-white text-gray-medium G-M rounded hover:border-green-dark hover:text-green-dark transition text-sm">
          Импорт JSON
        </button>
        <NuxtLink to="/psychologist/tests/create"
          class="px-4 py-2 text-white text-sm sm:text-base BP-B rounded bg-green-bright hover:bg-green-bright transition">
          + Создать тест
        </NuxtLink>
      </div>
    </div>

    <!-- ДЕСКТОП (md+): таблица -->
    <div class="hidden md:block bg-white rounded-lg overflow-hidden card-test-shadows">
      <table class="w-full">
        <thead class="bg-bg-light border-b border-gray-light">
          <tr>
            <th class="text-left px-6 py-3 leading-[1.1] w-48 text-lg G-M text-gray-medium">Название</th>
            <th class="text-left px-6 py-3 leading-[1.1] w-32 text-sm G-M text-gray-medium">Прошли</th>
            <th class="text-left px-6 py-3 leading-[1.1] text-sm G-M text-gray-medium">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="tests.length === 0">
            <td colspan="5" class="text-center py-12 G-M text-gray-light">
              Тестов пока нет. Создайте первый!
            </td>
          </tr>
          <tr v-for="test in tests" :key="test.id"
            class="border-b border-bg-light hover:bg-bg-light transition">
            <td class="px-6 py-4">
              <p class="BP-B leading-[1.1] text-lg text-green-dark">{{ test.title }}</p>
            </td>
            <td class="px-6 py-4 G-M text-gray-medium">{{ test.submissions_count }}</td>
            <td class="px-6 py-4">
              <div class="flex items-center justify-between gap-4">
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
                <div class="flex items-center gap-2">
                  <button @click="exportTest(test)"
                    class="export-icon bg-gray-light rounded w-8 h-8 flex items-center justify-center hover:bg-gray-200 transition cursor-pointer">
                  </button>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- МОБИЛЬНЫЙ + ПЛАНШЕТ (< md): карточки -->
    <div class="md:hidden flex flex-col gap-3">

      <div v-if="tests.length === 0"
        class="bg-white rounded-lg p-8 text-center G-M text-gray-light card-test-shadows">
        Тестов пока нет. Создайте первый!
      </div>

      <div v-for="test in tests" :key="test.id"
        class="bg-white rounded-lg p-3 sm:p-4 card-test-shadows flex flex-col gap-3">

        <!-- Название + счётчик -->
        <div class="flex items-start justify-between gap-2">
          <p class="BP-B text-base sm:text-lg text-green-dark leading-[1.2]">{{ test.title }}</p>
          <span class="flex-shrink-0 text-xs G-M text-gray-medium bg-bg-light px-2 py-1 rounded-full whitespace-nowrap">
            {{ test.submissions_count }} прошли
          </span>
        </div>

        <!-- Действия -->
        <div class="flex items-center border-t border-bg-light pt-2 gap-2">
          <!-- Ссылки -->
          <div class="flex flex-col gap-1 min-w-0">
            <button @click="copyLink(test)"
              class="text-xs G-M cursor-pointer text-green-bright hover:text-green-dark transition text-left truncate">
              Скопировать ссылку
            </button>
            <NuxtLink :to="`/psychologist/tests/${test.id}/submissions`"
              class="text-xs G-M text-gray-medium hover:text-green-dark transition">
              Результаты
            </NuxtLink>
          </div>

          <!-- Иконки -->
          <div class="flex items-center gap-1 ml-auto flex-shrink-0">
            <button @click="exportTest(test)"
              class="export-icon bg-gray-light rounded w-8 h-8 flex items-center justify-center hover:bg-gray-200 transition cursor-pointer">
            </button>
          </div>
        </div>

      </div>
    </div>

  </div>
  <input ref="fileInput" type="file" accept=".json" class="hidden" @change="handleFileImport" />
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ['auth']
})

interface Test {
  id: string
  title: string
  submissions_count: number
  token: string | null
}

const authStore = useAuthStore()
const fileInput = ref<HTMLInputElement | null>(null)
const tests = ref<Test[]>([])
  const { api } = useApi()

  onMounted(async () => {
  await authStore.fetchProfile()
  
  try {
    const result = await api(`/users/my_tests/${authStore.user?.id}`) as any
    tests.value = result.мои_опросники.map((t: any) => ({
      id: t.id,
      title: t.название,
      submissions_count: t.прошли,
      token: t.ссылка ?? null
    }))
  } catch (e) {
    console.error('Ошибка загрузки тестов:', e)
  }
})


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