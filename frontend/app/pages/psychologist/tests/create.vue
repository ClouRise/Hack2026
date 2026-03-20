<template>
  <div class="max-w-4xl mx-auto">
    <!-- Заголовок -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Новый тест</h1>
      <div class="flex gap-3">
        <button
            @click="handleImport"
            class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
        >
            Импорт JSON
        </button>
        <button
            @click="handleExport"
            class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
        >
            Экспорт JSON
        </button>
        <button
          @click="handleSave('draft')"
          class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
        >
          Сохранить черновик
        </button>
        <button
          @click="handleSave('published')"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Опубликовать
        </button>
      </div>
    </div>

    <!-- Мета-информация -->
    <div class="bg-white rounded-2xl shadow-sm p-6 mb-4">
      <h2 class="text-lg font-semibold mb-4">Основная информация</h2>
      <div class="flex flex-col gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Название теста</label>
          <input
            v-model="store.meta.title"
            type="text"
            placeholder="Введите название"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Описание</label>
          <textarea
            v-model="store.meta.description"
            placeholder="Введите описание"
            rows="3"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <label class="flex items-center gap-2 cursor-pointer">
          <input v-model="store.meta.show_report_to_client" type="checkbox" class="w-4 h-4" />
          <span class="text-sm text-gray-700">Показывать отчёт клиенту после прохождения</span>
        </label>
      </div>
    </div>

    <!-- Поля клиента -->
    <div class="bg-white rounded-2xl shadow-sm p-6 mb-4">
        <h2 class="text-lg font-semibold mb-4">Данные клиента перед тестом</h2>
        <p class="text-sm text-gray-500 mb-4">ФИО — обязательное поле, всегда присутствует.</p>

        <div class="flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-lg mb-3">
            <span class="text-sm text-gray-700">ФИО</span>
            <span class="text-xs text-gray-400 ml-auto">Обязательное</span>
        </div>

        <div v-for="(field, index) in store.meta.client_fields" :key="index" class="flex items-center gap-2 mb-2">
            <input
            v-model="field.label"
            type="text"
            placeholder="Название поля"
            class="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <select
            v-model="field.type"
            class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
            <option value="text">Текст</option>
            <option value="email">Email</option>
            <option value="number">Число</option>
            <option value="color">Цвет</option>
            </select>
            <label class="flex items-center gap-1 text-sm text-gray-600 cursor-pointer">
            <input v-model="field.required" type="checkbox" class="w-4 h-4" />
            Обяз.
            </label>
            <button @click="store.meta.client_fields.splice(index, 1)" class="text-red-400 hover:text-red-600">✕</button>
        </div>

        <button
            @click="store.meta.client_fields.push({ label: '', type: 'text', required: false })"
            class="mt-2 text-sm text-blue-500 hover:text-blue-700"
        >
            + Добавить поле
        </button>
    </div>

    <!-- Секции -->
    <div v-for="section in store.sections" :key="section.id" class="bg-white rounded-2xl shadow-sm p-6 mb-4">
      <!-- Заголовок секции -->
      <div class="flex items-center justify-between mb-4">
        <input
          v-model="section.title"
          type="text"
          class="text-lg font-semibold border-none outline-none bg-transparent w-full"
          placeholder="Название раздела"
        />
        <button @click="store.removeSection(section.id)" class="text-red-400 hover:text-red-600 ml-2">
          Удалить раздел
        </button>
      </div>

      <!-- Вопросы -->
      <div class="flex flex-col gap-4">
        <QuestionItem
          v-for="question in section.questions"
          :key="question.id"
          :question="question"
          :section-id="section.id"
        />
      </div>

      <button
        @click="store.addQuestion(section.id)"
        class="mt-4 w-full border-2 border-dashed border-gray-300 rounded-lg py-3 text-gray-500 hover:border-blue-400 hover:text-blue-500 transition"
      >
        + Добавить вопрос
      </button>
    </div>

    

    <!-- Добавить секцию -->
    <button
      @click="store.addSection()"
      class="w-full border-2 border-dashed border-gray-300 rounded-xl py-4 text-gray-500 hover:border-blue-400 hover:text-blue-500 transition"
    >
      + Добавить раздел
    </button>

    <!-- Метрики -->
    <div class="bg-white rounded-2xl shadow-sm p-6 mb-4">
        <h2 class="text-lg font-semibold mb-4">Формулы и метрики</h2>

        <div class="flex flex-col gap-4">
            <MetricItem
            v-for="metric in store.metrics"
            :key="metric.id"
            :metric="metric"
            />
        </div>

        <button
            @click="store.addMetric()"
            class="mt-4 w-full border-2 border-dashed border-gray-300 rounded-lg py-3 text-gray-500 hover:border-blue-400 hover:text-blue-500 transition"
        >
            + Добавить метрику
        </button>
    </div>
    <input ref="fileInput" type="file" accept=".json" class="hidden" @change="handleFileChange" />
  </div>
</template>

<script setup lang="ts">
import { useTestBuilderStore } from '~/stores/testBuilder'
import QuestionItem from '~/components/features/test/QuestionItem.vue'
import MetricItem from '~/components/features/test/MetricItem.vue'

definePageMeta({
  middleware: []
})

const store = useTestBuilderStore()

onMounted(() => {
  store.reset()
})

async function handleSave(status: 'draft' | 'published') {
  const payload = store.buildPayload()
  console.log('Сохраняем:', { ...payload, status })
  // TODO: подключить API когда бэк будет готов
}

const fileInput = ref<HTMLInputElement | null>(null)

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

function handleImport() {
  fileInput.value?.click()
}

function handleFileChange(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const data = JSON.parse(e.target?.result as string)
      store.loadFromJson(data)
    } catch {
      alert('Неверный формат файла')
    }
  }
  reader.readAsText(file)
}

</script>