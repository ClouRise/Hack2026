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
          <option value="percent">Процент (сумма / макс × 100)</option>
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
        Формула: 
        <span v-if="metric.operation === 'percent'">
            сумма({{ metric.question_ids.length }} вопросов) / макс × 100 × {{ metric.coefficient }}
        </span>
        <span v-else>
            {{ metric.operation }}({{ metric.question_ids.length }} вопросов) × {{ metric.coefficient }}
        </span>
    </p>

    <!-- Интерпретации -->
    <div class="flex flex-col gap-2">
        <label class="text-sm text-gray-500">Интерпретации результата:</label>

        <div v-for="(interp, index) in metric.interpretations" :key="index" class="border border-gray-100 rounded-lg p-3 flex flex-col gap-2">
            <div class="flex items-center gap-2">
            <span class="text-xs text-gray-400">от</span>
            <input v-model.number="interp.from" type="number" class="w-16 border border-gray-300 rounded px-2 py-1 text-sm" />
            <span class="text-xs text-gray-400">до</span>
            <input v-model.number="interp.to" type="number" class="w-16 border border-gray-300 rounded px-2 py-1 text-sm" />
            <button @click="metric.interpretations.splice(index, 1)" class="text-red-400 hover:text-red-600">✕</button>
            </div>
            <textarea
            v-model="interp.description"
            placeholder="Текст для отчёта при этом результате..."
            rows="2"
            class="w-full border border-gray-300 rounded px-2 py-1 text-sm"
            />
        </div>

        <button
            @click="metric.interpretations.push({ from: 0, to: 0, description: '' })"
            class="text-sm text-blue-500 hover:text-blue-700 text-left"
        >
            + Добавить интерпретацию
        </button>
    </div>
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