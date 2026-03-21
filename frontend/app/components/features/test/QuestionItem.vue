<template>
  <div class="bg-white border border-gray-light rounded-xl p-4" style="box-shadow: 0 2px 12px rgba(20,66,16,0.06);">
    <div class="flex items-start gap-3">
      <span class="BP-B text-green-bright text-sm mt-3 min-w-[24px]">{{ question.order }}.</span>
      <div class="flex-1 flex flex-col gap-3">

        <!-- Текст вопроса -->
        <input
          v-model="question.text"
          type="text"
          placeholder="Текст вопроса"
          class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright"
        />

        <!-- Тип вопроса -->
        <select
          :value="question.type"
          @change="store.setQuestionType(sectionId, question.id, ($event.target as HTMLSelectElement).value as QuestionType)"
          class="px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright"
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

        <!-- Варианты ответов -->
        <div v-if="question.type === 'single_choice' || question.type === 'multiple_choice' || question.type === 'yes_no'" class="flex flex-col gap-2">
          <div v-for="option in question.options" :key="option.id" class="flex flex-col gap-2 border-l-4 border-green-light bg-bg-light rounded-r-lg p-3">
            <div class="flex items-center gap-2">
              <input
                v-model="option.text"
                type="text"
                placeholder="Вариант ответа"
                class="flex-1 px-3 py-2 bg-white border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright"
              />
              <button @click="store.removeOption(sectionId, question.id, option.id)" class="text-bg-red hover:text-red-900 transition">✕</button>
            </div>
            <div class="flex items-center gap-4 pl-1 flex-wrap">
              <div class="flex items-center gap-2">
                <label class="text-xs G-M text-gray-medium">Вес:</label>
                <input v-model.number="option.weight" type="number"
                  class="w-16 px-2 py-1 bg-white border-b-2 border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright text-sm" />
              </div>
              <div v-if="question.type === 'single_choice' || question.type === 'yes_no'" class="flex items-center gap-2">
                <label class="text-xs G-M text-gray-medium">Перейти к вопросу:</label>
                <select v-model="option.next_question_id"
                  class="px-2 py-1 bg-white border-b-2 border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright text-sm">
                  <option :value="null">Следующий по порядку</option>
                  <option v-for="q in allQuestions" :key="q.id" :value="q.id" :disabled="q.id === question.id">
                    {{ q.order }}. {{ q.text || 'Без названия' }}
                  </option>
                </select>
              </div>
            </div>
          </div>
          <button @click="store.addOption(sectionId, question.id)" class="text-sm G-M text-green-bright hover:text-green-dark transition text-left">
            + Добавить вариант
          </button>
        </div>

        <!-- Слайдер / шкала мин-макс -->
        <div v-if="question.type === 'slider' || question.type === 'rating'" class="flex items-center gap-4">
          <div class="flex items-center gap-2">
            <label class="text-xs G-M text-gray-medium">Мин</label>
            <input v-model.number="question.min" type="number"
              class="w-16 px-2 py-1 bg-bg-light border-b-2 border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright" />
          </div>
          <div class="flex items-center gap-2">
            <label class="text-xs G-M text-gray-medium">Макс</label>
            <input v-model.number="question.max" type="number"
              class="w-16 px-2 py-1 bg-bg-light border-b-2 border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright" />
          </div>
        </div>

        <!-- Дата подтип -->
        <div v-if="question.type === 'date'">
          <select v-model="question.date_subtype"
            class="px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright">
            <option value="date">Дата</option>
            <option value="time">Время</option>
            <option value="datetime">Дата и время</option>
          </select>
        </div>

        <!-- Score ranges -->
        <div v-if="question.type === 'slider' || question.type === 'rating' || question.type === 'number'" class="flex flex-col gap-2">
          <label class="text-sm G-M text-gray-medium">Диапазоны весов:</label>
          <div v-for="(range, index) in question.score_ranges" :key="index" class="flex items-center gap-2 bg-bg-light rounded-lg p-2">
            <span class="text-xs G-M text-gray-medium">от</span>
            <input v-model.number="range.from" type="number"
              class="w-16 px-2 py-1 bg-white border-b-2 border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright text-sm" />
            <span class="text-xs G-M text-gray-medium">до</span>
            <input v-model.number="range.to" type="number"
              class="w-16 px-2 py-1 bg-white border-b-2 border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright text-sm" />
            <span class="text-xs G-M text-gray-medium">вес</span>
            <input v-model.number="range.weight" type="number"
              class="w-16 px-2 py-1 bg-white border-b-2 border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright text-sm" />
            <button @click="question.score_ranges!.splice(index, 1)" class="text-bg-red hover:text-red-900 transition">✕</button>
          </div>
          <button @click="question.score_ranges!.push({ from: 0, to: 0, weight: 0 })"
            class="text-sm G-M text-green-bright hover:text-green-dark transition text-left">
            + Добавить диапазон
          </button>
        </div>

        <!-- Чекбоксы -->
        <div class="flex items-center gap-4">
          <label class="flex items-center gap-2 cursor-pointer">
            <input v-model="isOptional" type="checkbox" class="w-4 h-4 accent-green-500" />
            <span class="text-sm G-M text-gray-medium">Необязательный вопрос</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input v-model="question.hidden_by_default" type="checkbox" class="w-4 h-4 accent-green-500" />
            <span class="text-sm G-M text-gray-medium">Скрыт по умолчанию</span>
          </label>
        </div>
      </div>

      <!-- Удалить -->
      <button @click="store.removeQuestion(sectionId, question.id)" class="text-bg-red hover:text-red-900 transition mt-1 text-lg">
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