<template>
  <div class="border border-gray-200 rounded-xl p-4">
    <div class="flex items-start gap-3">
      <span class="text-gray-400 font-medium text-sm mt-3 min-w-[24px]">{{ question.order }}.</span>
      <div class="flex-1 flex flex-col gap-3">
        <!-- Текст вопроса -->
        <input
          v-model="question.text"
          type="text"
          placeholder="Текст вопроса"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <!-- Тип вопроса -->
        <select
            :value="question.type"
            @change="store.setQuestionType(sectionId, question.id, ($event.target as HTMLSelectElement).value as QuestionType)"
            class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
            <option value="text">Текстовый ответ</option>
            <option value="textarea">Многострочный текст</option>
            <option value="single_choice">Один из списка</option>
            <option value="multiple_choice">Множественный выбор</option>
            <option value="yes_no">Да / Нет</option>
            <option value="number">Числовой ответ</option>
            <option value="slider">Диапазон (Slider)</option>
            <option value="date">Дата / Время</option>
            <option value="rating">Шкала оценки</option>
        </select>

        <!-- Варианты ответов (для single/multiple) -->
        <div v-if="question.type === 'single_choice' || question.type === 'multiple_choice' || question.type === 'yes_no'" class="flex flex-col gap-2">
            <div v-for="option in question.options" :key="option.id" class="flex flex-col gap-1 border border-gray-100 rounded-lg p-3">
                <div class="flex items-center gap-2">
                    <input
                        v-model="option.text"
                        type="text"
                        placeholder="Вариант ответа"
                        class="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button @click="store.removeOption(sectionId, question.id, option.id)" class="text-red-400 hover:text-red-600">
                        ✕
                    </button>
                </div>

                <div class="flex items-center gap-4 pl-1">
                <!-- Вес ответа -->
                <div class="flex items-center gap-2">
                    <label class="text-xs text-gray-500">Вес:</label>
                    <input
                    v-model.number="option.weight"
                    type="number"
                    class="w-16 border border-gray-300 rounded px-2 py-1 text-sm"
                    />
                </div>

                <!-- Ветвление -->
                <div v-if="question.type === 'single_choice'" class="flex items-center gap-2">
                    <label class="text-xs text-gray-500">Перейти к вопросу:</label>
                    <select
                    v-model="option.next_question_id"
                    class="border border-gray-300 rounded px-2 py-1 text-sm"
                    >
                    <option :value="null">Следующий по порядку</option>
                    <option
                        v-for="q in allQuestions"
                        :key="q.id"
                        :value="q.id"
                        :disabled="q.id === question.id"
                    >
                        {{ q.order }}. {{ q.text || 'Без названия' }}
                    </option>
                    </select>
                </div>
                </div>
            </div>
            <button
                @click="store.addOption(sectionId, question.id)"
                class="text-sm text-blue-500 hover:text-blue-700 text-left"
            >
                + Добавить вариант
            </button>
        </div>

        <!-- Настройки слайдера / шкалы -->
        <div v-if="question.type === 'slider' || question.type === 'rating'" class="flex items-center gap-3">
          <div>
            <label class="text-xs text-gray-500">Мин</label>
            <input v-model.number="question.min" type="number" class="w-16 border border-gray-300 rounded px-2 py-1 ml-1" />
          </div>
          <div>
            <label class="text-xs text-gray-500">Макс</label>
            <input v-model.number="question.max" type="number" class="w-16 border border-gray-300 rounded px-2 py-1 ml-1" />
          </div>
        </div>

        <div v-if="question.type === 'date'">
            <select
                v-model="question.date_subtype"
                class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
                <option value="date">Дата</option>
                <option value="time">Время</option>
                <option value="datetime">Дата и время</option>
            </select>
        </div>

        <!-- Score ranges для slider, rating, number -->
<div v-if="question.type === 'slider' || question.type === 'rating' || question.type === 'number'" class="flex flex-col gap-2">
  <label class="text-sm text-gray-500">Диапазоны весов:</label>

  <div v-for="(range, index) in question.score_ranges" :key="index" class="flex items-center gap-2">
    <span class="text-xs text-gray-400">от</span>
    <input
      v-model.number="range.from"
      type="number"
      class="w-16 border border-gray-300 rounded px-2 py-1 text-sm"
    />
    <span class="text-xs text-gray-400">до</span>
    <input
      v-model.number="range.to"
      type="number"
      class="w-16 border border-gray-300 rounded px-2 py-1 text-sm"
    />
    <span class="text-xs text-gray-400">вес</span>
    <input
      v-model.number="range.weight"
      type="number"
      class="w-16 border border-gray-300 rounded px-2 py-1 text-sm"
    />
    <button
      @click="question.score_ranges!.splice(index, 1)"
      class="text-red-400 hover:text-red-600"
    >✕</button>
  </div>

  <button
    @click="question.score_ranges!.push({ from: 0, to: 0, weight: 0 })"
    class="text-sm text-blue-500 hover:text-blue-700 text-left"
  >
    + Добавить диапазон
  </button>
</div>



        

        <div class="flex items-center gap-4">
            <label class="flex items-center gap-2 cursor-pointer">
                <input v-model="isOptional" type="checkbox" class="w-4 h-4" />
                <span class="text-sm text-gray-600">Необязательный вопрос</span>
            </label>

            <label class="flex items-center gap-2 cursor-pointer">
                <input v-model="question.hidden_by_default" type="checkbox" class="w-4 h-4" />
                <span class="text-sm text-gray-600">Скрыт по умолчанию</span>
            </label>
        </div>
      </div>

      <!-- Удалить вопрос -->
      <button @click="store.removeQuestion(sectionId, question.id)" class="text-red-400 hover:text-red-600 mt-1">
        🗑
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '~/stores/testBuilder'
import { useTestBuilderStore } from '~/stores/testBuilder';

const props = defineProps<{
  question: Question
  sectionId: string
}>()

const store = useTestBuilderStore()

const allQuestions = computed(() => {
  return store.sections.flatMap(s => s.questions)
})

const isOptional = computed({
  get: () => !props.question.required,
  set: (val) => store.updateQuestion(props.sectionId, props.question.id, { required: !val })
})

watch(() => props.question.type, (newType) => {
  if (newType === 'slider' || newType === 'rating') {
    store.updateQuestion(props.sectionId, props.question.id, { min: 1, max: 5 })
  } else {
    store.updateQuestion(props.sectionId, props.question.id, { min: undefined, max: undefined })
  }
})

</script>