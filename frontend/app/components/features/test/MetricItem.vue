<template>
  <div class="border border-gray-200 rounded-xl p-4 flex flex-col gap-3">
    <!-- Название метрики -->
    <div class="flex items-center justify-between">
      <input
        v-model="metric.name"
        type="text"
        placeholder="Название метрики (например: Уровень тревожности)"
        class="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button @click="store.removeMetric(metric.id)" class="text-red-400 hover:text-red-600 ml-2">
        🗑
      </button>
    </div>

    <div class="flex items-center gap-4 flex-wrap">
      <!-- Операция -->
      <div class="flex items-center gap-2">
        <label class="text-sm text-gray-500">Операция:</label>
        <select
          v-model="metric.operation"
          class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="sum">Сумма</option>
          <option value="avg">Среднее</option>
          <option value="min">Минимум</option>
          <option value="max">Максимум</option>
        </select>
      </div>

      <!-- Коэффициент -->
      <div class="flex items-center gap-2">
        <label class="text-sm text-gray-500">Коэффициент:</label>
        <input
          v-model.number="metric.coefficient"
          type="number"
          step="0.1"
          class="w-20 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
    </div>

    <!-- Выбор вопросов -->
    <div>
      <label class="text-sm text-gray-500 mb-2 block">Вопросы участвующие в формуле:</label>
      <div class="flex flex-col gap-1 max-h-40 overflow-y-auto">
        <label
          v-for="question in allQuestions"
          :key="question.id"
          class="flex items-center gap-2 cursor-pointer hover:bg-gray-50 px-2 py-1 rounded"
        >
          <input
            type="checkbox"
            :value="question.id"
            v-model="metric.question_ids"
            class="w-4 h-4"
          />
          <span class="text-sm">{{ question.order }}. {{ question.text || 'Без названия' }}</span>
        </label>
      </div>
    </div>

    <!-- Описание -->
    <input
      v-model="metric.description"
      type="text"
      placeholder="Описание метрики для отчёта"
      class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
    />

    <!-- Превью формулы -->
    <p class="text-xs text-gray-400">
      Формула: {{ metric.operation }}({{ metric.question_ids.length }} вопросов) × {{ metric.coefficient }}
    </p>
  </div>
</template>

<script setup lang="ts">
import type { Metric } from '~/stores/testBuilder'

defineProps<{
  metric: Metric
}>()

const store = useTestBuilderStore()

const WEIGHTED_TYPES = ['single_choice', 'multiple_choice', 'yes_no', 'slider', 'rating', 'number']

const allQuestions = computed(() =>
  store.sections
    .flatMap(s => s.questions)
    .filter(q => WEIGHTED_TYPES.includes(q.type))
)

</script>