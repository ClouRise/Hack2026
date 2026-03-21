<template>
  <div class="flex flex-col gap-3">
    
   <VueDraggable
  v-model="localBlocks"
  :group="{ name: 'report-blocks', pull: true, put: ['report-blocks'] }"
  :animation="200"
  handle=".drag-handle"
  ghost-class="ghost-report-block"
  class="report-drop-zone flex flex-col gap-3 min-h-[80px] rounded-xl border-2 border-dashed border-gray-light transition-all"
  :class="localBlocks.length > 0 ? 'border-transparent' : ''"
>
  <div
    v-for="(block, index) in localBlocks"
    :key="block.id"
    class="bg-white border border-gray-light rounded-xl p-4"
    style="box-shadow: 0 2px 12px rgba(20,66,16,0.06);"
  >
      >
        <!-- содержимое блоков без изменений -->
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center gap-2">
            <div class="drag-handle cursor-grab active:cursor-grabbing select-none text-gray-light hover:text-green-dark transition">
              <svg width="14" height="22" viewBox="0 0 16 24" fill="currentColor">
                <circle cx="5" cy="6" r="2"/>
                <circle cx="11" cy="6" r="2"/>
                <circle cx="5" cy="12" r="2"/>
                <circle cx="11" cy="12" r="2"/>
                <circle cx="5" cy="18" r="2"/>
                <circle cx="11" cy="18" r="2"/>
              </svg>
            </div>
            <span class="text-sm BP-M text-green-dark">{{ blockLabel(block.type) }}</span>
          </div>
          <button @click="removeBlock(index)" class="text-bg-red hover:text-red-900 transition">✕</button>
        </div>

        <textarea v-if="block.type === 'text'" v-model="block.content" rows="3" placeholder="Введите текст..."
          class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright text-sm" />

        <select v-if="block.type === 'metric'" v-model="block.metric_id"
          class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright text-sm">
          <option value="">Выберите метрику</option>
          <option v-for="metric in store.metrics" :key="metric.id" :value="metric.id">{{ metric.name || 'Без названия' }}</option>
        </select>

        <div v-if="block.type === 'chart'" class="flex flex-col gap-3">
          <select v-model="block.chart_type"
            class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright text-sm">
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

        <div v-if="block.type === 'answers'" class="flex flex-col gap-2">
          <label class="flex items-center gap-2 cursor-pointer mb-2">
            <input type="checkbox" v-model="block.show_all_answers" class="w-4 h-4 accent-green-500" />
            <span class="text-sm G-M text-gray-medium">Показать все ответы</span>
          </label>
          <div v-if="!block.show_all_answers" class="flex flex-col gap-1">
            <label class="text-xs G-M text-gray-medium mb-1">Выберите вопросы:</label>
            <label v-for="question in allQuestions" :key="question.id"
              class="flex items-center gap-2 cursor-pointer hover:bg-bg-light px-2 py-1 rounded transition">
              <input type="checkbox" :value="question.id" v-model="block.question_ids" class="w-4 h-4 accent-green-500" />
              <span class="text-sm G-M text-green-dark">{{ question.order }}. {{ question.text || 'Без названия' }}</span>
            </label>
          </div>
        </div>
      </div>
    </VueDraggable>

    <!-- Зона дропа — видна только когда список пустой И не идёт drag -->

  </div>
</template>

<script setup lang="ts">
import { VueDraggable } from 'vue-draggable-plus'
import type { ReportBlock, ReportBlockType } from '~/stores/testBuilder'

const props = defineProps<{
  blocks: ReportBlock[]
}>()

const emit = defineEmits<{
  update: [blocks: ReportBlock[]]
}>()

const store = useTestBuilderStore()
const isDraggingOver = ref(false)

const localBlocks = computed({
  get: () => props.blocks,
  set: (val) => emit('update', val)
})

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

function removeBlock(index: number) {
  const updated = [...props.blocks]
  updated.splice(index, 1)
  emit('update', updated)
}
</script>

<style>
.report-drop-zone:not(:has(> div))::before {
  content: 'Перетащите блок из палитры';
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 2rem 0;
  color: #9bb299;
  font-size: 14px;
  font-family: 'GothamOffice-medium';
}

.ghost-report-block {
  opacity: 1 !important;
  background: #f1faf0;
  border: 2px dashed #8ed993 !important;
  border-radius: 12px;
  box-shadow: none !important;
}

.ghost-report-block * {
  opacity: 0.3;
}
.report-drop-zone:has(> div) {
  border-color: transparent !important;
}

</style>