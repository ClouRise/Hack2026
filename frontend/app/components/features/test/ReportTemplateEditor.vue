<template>
  <div class="flex flex-col gap-3">
    <!-- Блоки -->
    <div v-for="(block, index) in blocks" :key="block.id" class="bg-white border border-gray-light rounded-xl p-4" style="box-shadow: 0 2px 12px rgba(20,66,16,0.06);">
      <div class="flex items-center justify-between mb-3">
        <span class="text-sm BP-M text-green-dark">
          {{ blockLabel(block.type) }}
        </span>
        <div class="flex items-center gap-2">
          <button @click="moveUp(index)" :disabled="index === 0" class="G-M text-gray-medium hover:text-green-dark disabled:opacity-30 transition">↑</button>
          <button @click="moveDown(index)" :disabled="index === blocks.length - 1" class="G-M text-gray-medium hover:text-green-dark disabled:opacity-30 transition">↓</button>
          <button @click="removeBlock(index)" class="text-bg-red hover:text-red-900 transition">✕</button>
        </div>
      </div>

      <!-- Текстовый блок -->
      <textarea
        v-if="block.type === 'text'"
        v-model="block.content"
        rows="3"
        placeholder="Введите текст..."
        class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright text-sm"
      />

      <!-- Блок метрики -->
      <select
        v-if="block.type === 'metric'"
        v-model="block.metric_id"
        class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright text-sm"
      >
        <option value="">Выберите метрику</option>
        <option v-for="metric in store.metrics" :key="metric.id" :value="metric.id">
          {{ metric.name || 'Без названия' }}
        </option>
      </select>

      <!-- Блок графика -->
      <div v-if="block.type === 'chart'" class="flex flex-col gap-3">
        <select
          v-model="block.chart_type"
          class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright text-sm"
        >
          <option value="bar">Столбчатый</option>
          <option value="radar">Радар</option>
          <option value="pie">Круговой</option>
        </select>
        <div class="flex flex-col gap-1">
          <label class="text-xs G-M text-gray-medium mb-1">Метрики для графика:</label>
          <label v-for="metric in store.metrics" :key="metric.id" class="flex items-center gap-2 cursor-pointer hover:bg-bg-light px-2 py-1 rounded transition">
            <input type="checkbox" :value="metric.id" v-model="block.metric_ids" class="w-4 h-4 accent-green-500" />
            <span class="text-sm G-M text-green-dark">{{ metric.name || 'Без названия' }}</span>
          </label>
        </div>
      </div>

      <!-- Блок ответов -->
      <div v-if="block.type === 'answers'" class="flex flex-col gap-2">
        <label class="flex items-center gap-2 cursor-pointer mb-2">
          <input type="checkbox" v-model="block.show_all_answers" class="w-4 h-4 accent-green-500" />
          <span class="text-sm G-M text-gray-medium">Показать все ответы</span>
        </label>
        <div v-if="!block.show_all_answers" class="flex flex-col gap-1">
          <label class="text-xs G-M text-gray-medium mb-1">Выберите вопросы:</label>
          <label
            v-for="question in allQuestions"
            :key="question.id"
            class="flex items-center gap-2 cursor-pointer hover:bg-bg-light px-2 py-1 rounded transition"
          >
            <input type="checkbox" :value="question.id" v-model="block.question_ids" class="w-4 h-4 accent-green-500" />
            <span class="text-sm G-M text-green-dark">{{ question.order }}. {{ question.text || 'Без названия' }}</span>
          </label>
        </div>
      </div>
    </div>

    <!-- Добавить блок -->
    <div class="flex gap-2 flex-wrap">
      <button @click="addBlock('text')" class="px-3 py-2 border-2 border-dashed border-gray-light rounded-lg text-sm G-M text-gray-medium hover:border-green-bright hover:text-green-bright transition">
        + Текст
      </button>
      <button @click="addBlock('metric')" class="px-3 py-2 border-2 border-dashed border-gray-light rounded-lg text-sm G-M text-gray-medium hover:border-green-bright hover:text-green-bright transition">
        + Метрика
      </button>
      <button @click="addBlock('chart')" class="px-3 py-2 border-2 border-dashed border-gray-light rounded-lg text-sm G-M text-gray-medium hover:border-green-bright hover:text-green-bright transition">
        + График
      </button>
      <button @click="addBlock('answers')" class="px-3 py-2 border-2 border-dashed border-gray-light rounded-lg text-sm G-M text-gray-medium hover:border-green-bright hover:text-green-bright transition">
        + Ответы
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ReportBlock, ReportBlockType } from '~/stores/testBuilder'

const props = defineProps<{
  blocks: ReportBlock[]
}>()

const emit = defineEmits<{
  update: [blocks: ReportBlock[]]
}>()

const store = useTestBuilderStore()

const allQuestions = computed(() =>
  store.sections.flatMap(s => s.questions)
)

function blockLabel(type: ReportBlockType) {
  const labels = {
    text: '📝 Текст',
    metric: '📊 Метрика',
    answers: '📋 Ответы клиента',
    chart: '📈 График'
  }
  return labels[type]
}

function addBlock(type: ReportBlockType) {
  const newBlock: ReportBlock = {
    id: crypto.randomUUID(),
    type,
    content: '',
    metric_id: '',
    chart_type: 'bar',
    metric_ids: [],
    question_ids: [],  
    show_all_answers: false
  }
  emit('update', [...props.blocks, newBlock])
}

function removeBlock(index: number) {
  const updated = [...props.blocks]
  updated.splice(index, 1)
  emit('update', updated)
}

function moveUp(index: number) {
  if (index === 0) return
  const updated = [...props.blocks]
  const temp = updated[index - 1]!
  updated[index - 1] = updated[index]!
  updated[index] = temp
  emit('update', updated)
}

function moveDown(index: number) {
  if (index === props.blocks.length - 1) return
  const updated = [...props.blocks]
  const temp = updated[index + 1]!
  updated[index + 1] = updated[index]!
  updated[index] = temp
  emit('update', updated)
}
</script>