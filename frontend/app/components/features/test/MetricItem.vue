<template>
  <div class="bg-white border border-gray-light rounded-xl p-4 flex flex-col gap-3" style="box-shadow: 0 2px 12px rgba(20,66,16,0.06);">
    <!-- Название метрики -->
    <div class="flex items-center justify-between">
      <input
        v-model="metric.name"
        type="text"
        placeholder="Название метрики (например: Уровень тревожности)"
        class="flex-1 px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright"
      />
      <button @click="store.removeMetric(metric.id)" class="trash-icon bg-red-400 hover:bg-red-500 rounded w-8 h-8 flex items-center justify-center transition cursor-pointer">
      </button>
    </div>

    <div class="flex items-center gap-4 flex-wrap">
      <!-- Операция -->
      <div class="flex items-center gap-2">
        <label class="text-sm G-M text-gray-medium">Операция:</label>
        <select
          v-model="metric.operation"
          class="px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright"
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
        <label class="text-sm G-M text-gray-medium">Коэффициент:</label>
        <input
          v-model.number="metric.coefficient"
          type="number"
          step="0.1"
          class="w-20 px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright"
        />
      </div>
    </div>

    <!-- Выбор вопросов -->
    <div>
      <label class="text-sm G-M text-gray-medium mb-2 block">Вопросы участвующие в формуле:</label>
      <div class="flex flex-col gap-1 max-h-40 overflow-y-auto">
        <label
          v-for="question in allQuestions"
          :key="question.id"
          class="flex items-center gap-2 cursor-pointer hover:bg-bg-light px-2 py-1 rounded transition"
        >
          <input
            type="checkbox"
            :value="question.id"
            v-model="metric.question_ids"
            class="w-4 h-4 accent-green-500"
          />
          <span class="text-sm G-M text-green-dark">{{ question.order }}. {{ question.text || 'Без названия' }}</span>
        </label>
      </div>
    </div>

    <!-- Описание -->
    <input
      v-model="metric.description"
      type="text"
      placeholder="Описание метрики для отчёта"
      class="px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright"
    />

    <!-- Превью формулы -->
    <p class="text-xs G-M text-gray-medium bg-bg-light px-3 py-2 rounded">
      Формула:
      <span v-if="metric.operation === 'percent'" class="text-green-bright">
        сумма({{ metric.question_ids.length }} вопросов) / макс × 100 × {{ metric.coefficient }}
      </span>
      <span v-else class="text-green-bright">
        {{ metric.operation }}({{ metric.question_ids.length }} вопросов) × {{ metric.coefficient }}
      </span>
    </p>

    <!-- Интерпретации -->
    <div class="flex flex-col gap-2">
      <label class="text-sm G-M text-gray-medium">Интерпретации результата:</label>

      <div v-for="(interp, index) in metric.interpretations" :key="index" class="border-l-4 border-green-light bg-bg-light rounded-r-lg p-3 flex flex-col gap-2">
        <div class="flex items-center gap-2 flex-wrap">
          <span class="text-xs G-M text-gray-medium">от</span>
          <input v-model.number="interp.from" type="number"
            class="w-16 px-2 py-1 bg-white border-b-2 border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright text-sm" />
          <span class="text-xs G-M text-gray-medium">до</span>
          <input v-model.number="interp.to" type="number"
            class="w-16 px-2 py-1 bg-white border-b-2 border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright text-sm" />
          <button @click="metric.interpretations.splice(index, 1)" class="text-bg-red hover:text-red-900 transition">✕</button>
        </div>
        <textarea
          v-model="interp.description"
          placeholder="Текст для отчёта при этом результате..."
          rows="2"
          class="w-full px-2 py-1 bg-white border-b-2 border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright text-sm"
        />
      </div>

      <button
        @click="metric.interpretations.push({ from: 0, to: 0, description: '' })"
        class="text-sm G-M text-green-bright hover:text-green-dark transition text-left"
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