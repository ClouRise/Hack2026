<template>
  <div class="max-w-4xl ">
    <!-- Мета-информация -->
    <div class="bg-white rounded-2xl p-6 mb-4 card-test-shadows">
      <h2 class="text-xl BP-B text-green-dark mb-4">Основная информация</h2>
      <div class="flex flex-col gap-4">
        <div>
          <label class="block text-[10pt] G-M text-gray-light mb-1">Название теста</label>
          <input
            v-model="store.meta.title"
            type="text"
            placeholder="Введите название"
            class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright"
          />
        </div>
        <div>
          <label class="block text-[10pt] G-M text-gray-light mb-1">Описание</label>
          <textarea
            v-model="store.meta.description"
            placeholder="Введите описание"
            rows="3"
            class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright"
          />
        </div>
        <label class="flex items-center gap-2 cursor-pointer">
          <input v-model="store.meta.show_report_to_client" type="checkbox" class="w-4 h-4 accent-green-500" />
          <span class="text-sm G-M text-gray-medium">Показывать отчёт клиенту после прохождения</span>
        </label>
      </div>
    </div>

    <!-- Поля клиента -->
    <div class="bg-white rounded-2xl p-6 mb-4 card-test-shadows">
      <h2 class="text-xl BP-B text-green-dark mb-4">Данные клиента перед тестом</h2>
      <p class="text-sm G-M text-gray-medium mb-4">ФИО — обязательное поле, всегда присутствует.</p>
      <div class="flex items-center gap-2 px-3 py-2 bg-bg-light border-l-4 border-green-light rounded-r-lg mb-3">
        <span class="text-sm G-M text-green-dark">ФИО</span>
        <span class="text-xs G-M text-gray-medium ml-auto">Обязательное</span>
      </div>
      <div v-for="(field, index) in store.meta.client_fields" :key="index" class="flex items-center gap-2 mb-2">
        <input v-model="field.label" type="text" placeholder="Название поля"
          class="flex-1 px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright" />
        <select v-model="field.type"
          class="px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright">
          <option value="text">Текст</option>
          <option value="email">Email</option>
          <option value="number">Число</option>
          <option value="color">Цвет</option>
        </select>
        <label class="flex items-center gap-1 text-sm G-M text-gray-medium cursor-pointer">
          <input v-model="field.required" type="checkbox" class="w-4 h-4 accent-green-500" />
          Обяз.
        </label>
        <button @click="store.meta.client_fields.splice(index, 1)" class="text-bg-red hover:text-red-900 transition">✕</button>
      </div>
      <button @click="store.meta.client_fields.push({ label: '', type: 'text', required: false })"
        class="mt-2 text-sm G-M text-green-bright hover:text-green-dark transition">
        + Добавить поле
      </button>
    </div>

   <!-- Секции -->
<div v-for="section in store.sections" :key="section.id" class="bg-white rounded-2xl p-6 mb-4" style="box-shadow: 0 4px 32px rgba(20,66,16,0.10);">
  <div class="flex items-center justify-between mb-4">
    <input v-model="section.title" type="text"
      class="text-xl BP-B text-green-dark border-none outline-none bg-transparent w-full"
      placeholder="Название раздела" />
    <button @click="store.removeSection(section.id)" class="text-sm G-M text-red-400 hover:text-red-900 w-[200px] ml-2">
      Удалить раздел
    </button>
  </div>

  <!-- ВОТ ЭТО МЕНЯЕМ -->
  <VueDraggable
  v-model="section.questions"
  :group="{ name: 'questions', pull: true, put: ['questions'] }"
  :animation="200"
  handle=".drag-handle"
  ghost-class="ghost-question"
  class="questions-drop-zone flex flex-col gap-4 min-h-[80px] rounded-xl border-2 border-dashed transition-all"
  :class="section.questions.length > 0 ? 'border-transparent' : 'border-gray-light'"
  @update="() => recalcOrder(section.id)"
  @add="() => recalcOrder(section.id)"
>
  <QuestionItem
    v-for="question in section.questions"
    :key="question.id"
    :question="question"
    :section-id="section.id"
  />
</VueDraggable>

  <button @click="store.addQuestion(section.id)"
    class="mt-4 w-full border-2 border-dashed border-green-light text-green-dark rounded-lg py-3 G-M hover:border-green-bright hover:text-green-bright transition">
    + Добавить вопрос
  </button>
</div>

    <button @click="store.addSection()"
      class="w-full border-2 border-dashed border-green-light bg-opacity-darken rounded-xl py-4 G-M text-gray-medium hover:border-green-bright hover:text-green-bright transition mb-4">
      + Добавить раздел
    </button>

    <!-- Метрики -->
    <div class="bg-white rounded-2xl p-6 mb-4 card-test-shadows">
      <h2 class="text-xl BP-B text-green-dark mb-4">Формулы и метрики</h2>
      <div class="flex flex-col gap-4">
        <MetricItem v-for="metric in store.metrics" :key="metric.id" :metric="metric" />
      </div>
      <button @click="store.addMetric()"
        class="mt-4 w-full border-2 border-dashed border-green-light rounded-lg py-3 G-M text-gray-medium hover:border-green-bright hover:text-green-bright transition">
        + Добавить метрику
      </button>
    </div>

    <ReportBuilder />

    <input ref="fileInput" type="file" accept=".json" class="hidden" @change="handleFileChange" />
  </div>
</template>

<script setup lang="ts">
import { VueDraggable } from 'vue-draggable-plus'
import QuestionItem from '~/components/features/test/QuestionItem.vue'
import MetricItem from '~/components/features/test/MetricItem.vue'
import ReportBuilder from './ReportBuilder.vue'

const store = useTestBuilderStore()
const fileInput = ref<HTMLInputElement | null>(null)

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

function recalcOrder(sectionId: string) {
  const section = store.sections.find(s => s.id === sectionId)
  if (!section) return
  section.questions.forEach((q, index) => {
    q.order = index + 1
    q.section_id = sectionId // фиксим section_id для элементов из палитры
  })
}


defineExpose({ fileInput })
</script>

<style>
.ghost-question {
  opacity: 1 !important;
  background: #f1faf0;
  border: 2px dashed #8ed993 !important;
  border-radius: 12px;
  box-shadow: none !important;
}

.ghost-question * {
  opacity: 0.3;
}
.questions-drop-zone:not(:has(> div))::before {
  content: 'Перетащите вопрос из палитры';
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 2rem 0;
  color: #9bb299;
  font-size: 14px;
  font-family: 'GothamOffice-medium';
}

.questions-drop-zone:has(> div) {
  border-color: transparent !important;
}
</style>