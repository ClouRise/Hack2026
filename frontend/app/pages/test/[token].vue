<template>
  <div>
    <Teleport to="body">
      <div v-if="isTest" class="fixed top-0 left-0 right-0 z-50 flex flex-col items-center">
        <div class="w-full h-[3px] bg-gray-200">
          <div class="h-[3px] bg-green-bright transition-all duration-500" :style="{ width: progress + '%' }"></div>
        </div>
        <div class="bg-white px-5 py-1 rounded-b-2xl flex items-center gap-2" style="box-shadow: 0 4px 16px rgba(20,66,16,0.10);">
          <span class="text-xs G-M text-gray-medium">Пройдено</span>
          <span class="text-sm BP-B text-green-dark">{{ progress }}%</span>
        </div>
      </div>
    </Teleport>

    <div class="text-xs text-green-light">Тест:</div>
    <div class="text-4xl BP-B text-green-dark leading-[0.9] mt-0">{{ testTitle }}</div>

    <div class="flex justify-center my-4">
      <div :style="isDarkTheme ? 'opacity: 0.1' : ''" class="w-80 h-px bg-gray-light"></div>
    </div>

    <div v-if="!isCanTouchContinue">
      <div class="text-[10pt] leading-[1.1] text-gray-medium G-M mb-6">
        Перед началом выполнения теста, вы должны заполнить информацию о себе.
      </div>

      <div class="space-y-4">
        <div>
          <label class="block text-[10pt] text-gray-light G-M mb-1">Ваше ФИО</label>
          <input @input="checkMainLabels" v-model="form.fio" type="text"
            class="w-full px-3 py-2 text-green-dark bg-bg-light border-l-[5px] border-b-[2px] border-gray-light focus:outline-none focus:border-green-bright G-M" />
        </div>
        <div>
          <label class="block text-[10pt] text-gray-light G-M mb-1">Ваша почта</label>
          <input @input="checkMainLabels" v-model="form.email" type="email"
            class="w-full px-3 py-2 text-green-dark bg-bg-light border-l-[5px] border-b-[2px] border-gray-light focus:outline-none focus:border-green-bright G-M" />
        </div>
      </div>

      <div v-if="dynamicFields?.length" class="space-y-4 mt-4">
        <div v-for="(field, index) in dynamicFields" :key="index">
          <label class="block text-[10pt] text-gray-light G-M mb-1">{{ field.label }}</label>
          <input v-if="field.type === 'email'" type="email" v-model="form[field.label]"
            class="w-full px-3 py-2 text-green-dark bg-bg-light border-l-[5px] border-b-[2px] border-gray-light focus:outline-none focus:border-green-bright G-M" />
          <input v-else-if="field.type === 'number'" type="number" v-model="form[field.label]"
            class="w-full px-3 py-2 text-green-dark bg-bg-light border-l-[5px] border-b-[2px] border-gray-light focus:outline-none focus:border-green-bright G-M" />
          <input v-else-if="field.type === 'color'" type="color" v-model="form[field.label]" />
          <input v-else type="text" v-model="form[field.label]"
            class="w-full px-3 py-2 text-green-dark bg-bg-light border-l-[5px] border-b-[2px] border-gray-light focus:outline-none focus:border-green-bright G-M" />
        </div>
      </div>

      <Button @click="checkForm"
        class="bg-green-bright hover:bg-green-bright mt-8 w-full px-4 py-2 text-white rounded hover:bg-green-600 text-xl BP-B">
        {{ button_text }}
      </Button>

      <p v-if="!isCanTouchContinue && firstTouchButton" class="text-center text-rose-400 relative top-[10px] text-sm">
        {{ error_message }}
      </p>
    </div>

    <div v-if="isTest">
      <div v-for="(currentSection, index_section) in testData.sections" :key="currentSection.id">
        <div class="my-3">
          <div :class="index_section == 0 ? 'mt-0 mb-3 text-right' : 'mt-12 mb-3 text-right'">
            <label class="text-[17pt] BP-B text-green-dark leading-[0.9] mt-0">{{ currentSection.title }}.</label>
          </div>

          <div v-for="(question, index_question) in currentSection.questions.filter(q => visibleQuestions.has(q.id))"
            :key="question.id">
            <label class="G-M text-gray-medium text-[13pt] leading-[1.1] block">
              <span class="G-Bold text-gray-main mr-1 leading-[1.1] inline-block">
                № {{ index_section + 1 }}.{{ index_question + 1 }}.
              </span>
              {{ question.text }} <span class="text-rose-300">{{ question.required ? '*' : '' }}</span>
            </label>

            <p class="G-Book text-[10pt] text-gray-medium opacity-[0.5]" v-if="question.type == 'single_choice'">Выберите <span class="underline">один</span> вариант ответа.</p>
            <p class="G-Book text-[10pt] text-gray-medium opacity-[0.5]" v-if="question.type == 'multiple_choice'">Выберите <span class="underline">несколько</span> вариантов ответа.</p>
            <p class="G-Book text-[10pt] text-gray-medium opacity-[0.5]" v-if="question.type == 'raiting'"><span class="underline">Перетяните</span> ползунок, где {{ question.min }} - не про меня; {{ question.max }} - это я!.</p>
            <p class="G-Book text-[10pt] text-gray-medium opacity-[0.5]" v-if="question.type == 'text'">Введите текст.</p>
            <p class="G-Book text-[10pt] text-gray-medium opacity-[0.5]" v-if="question.type == 'textarea'"><span class="underline">Развернуто</span> ответьте на вопрос.</p>
            <p class="G-Book text-[10pt] text-gray-medium opacity-[0.5]" v-if="question.type == 'number'">Введите число.</p>
            <p class="G-Book text-[10pt] text-gray-medium opacity-[0.5]" v-if="question.type == 'slider'">Выберите диапазон ползунками.</p>
            <p class="G-Book text-[10pt] text-gray-medium opacity-[0.5]" v-if="question.type == 'yes_no'">Выберите вариант ответа.</p>
            <p class="G-Book text-[10pt] text-gray-medium opacity-[0.5]" v-if="question.type == 'date'">Выберите дату.</p>

            <p class="G-Bold text-gray-main text-[11pt] mb-2">Ответ: {{ question.type == "rating" ? form[question.id] : '' }}</p>

            <QuestionInput v-model="form[question.id]" :type="question.type"
              :options="question.options.map(opt => opt.text)" :min="question.min" :max="question.max" />

            <div v-if="question.type === 'rating'" class="flex justify-between text-[10pt] text-gray-medium G-M mt-1">
              <span>{{ question.min }}</span>
              <span>{{ question.max }}</span>
            </div>

            <div v-if="currentSection.questions.length != index_question + 1" class="flex justify-center my-5">
              <div :style="isDarkTheme ? 'opacity: 0.1' : ''" class="w-full h-px bg-gray-200"></div>
            </div>
          </div>
        </div>
      </div>

      <Button @click="checkFormTest"
        class="bg-green-bright hover:bg-green-bright mt-8 w-full px-4 py-2 text-white rounded hover:bg-green-600 text-xl BP-B">
        {{ button_text }}
      </Button>
      <p v-if="!isCanTouchContinueTest && firstTouchButtonEndTest"
        class="text-center text-rose-400 relative top-[10px] text-sm">Пожалуйста, ответьте на все вопросы со значком "*"
      </p>
    </div>

    <div v-if="downloadReport" class="flex flex-col items-center">
      <div class="image-done-test"></div>
      <h1 class="text-4xl BP-B text-green-dark2 leading-[0.9] mb-6">Тест пройден!</h1>
      <p class="G-M text-gray-medium leading-[1.1] text-sm text-left mb-4">
        Спасибо за прохождение теста! Психолог в скором времени пришлет результаты вам на почту.
        А пока можете ознакомиться с <span class="underline G-Bold">предварительным</span> результатом от ИИ:
      </p>
      <div class="w-full bg-bg-light border-l-[5px] border-green-dark2 p-4 mb-6">
        <p class="BP-M text-sm text-gray-main leading-[0.9]">
          На основе ваших ответов не было выявлено выраженных индикаторов, характерных для острых клинических состояний, требующих немедленного вмешательства. Показатели находятся в диапазоне, который часто связывают с нормативными колебаниями психоэмоционального фона (адаптационная усталость, ситуативный стресс.<br/><br/>
          <span class="font-bold">Важно помнить:</span> Данный тест не является медицинским диагнозом. Он отражает ваше состояние только в момент прохождения.<br/><br/>
          <span class="font-bold">Рекомендация:</span> Для поддержания эмоционального баланса мы рекомендуем обратить внимание на режим сна и физической активности. Если вы замечаете, что усталость накапливается, консультация психолога (даже профилактическая) поможет подобрать инструменты для восстановления.
        </p>
      </div>
      <button @click="downloadReportTest"
        class="bg-green-bright hover:bg-green-bright mt-8 w-full px-4 py-2 text-white rounded hover:bg-green-600 text-xl BP-B">
        Скачать результат
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'empty'
})

const route = useRoute()
const testId = route.params.id

import { ref } from 'vue'
import { useThemeStore } from '~/stores/theme'
import { storeToRefs } from 'pinia'
const themeStore = useThemeStore()
const { currentTheme, isLightTheme, isDarkTheme } = storeToRefs(themeStore)

const testData = ref({
  "title": "Тест на выявление уровня агрессии",
  "description": "олватплоы выалп вылт аивылт вл  лвы лв",
  "show_report_to_client": false,
  "client_fields": [],
  "report_template": {
    "client": [],
    "psychologist": []
  },
  "sections": [
    {
      "id": "8d1d476c-b2c1-4850-a7ef-0cb20bfa32bf",
      "order": 1,
      "title": "Раздел 1",
      "questions": [
        {
          "id": "4fd9c7a3-4c8d-4069-b734-8290d1b603fa",
          "section_id": "8d1d476c-b2c1-4850-a7ef-0cb20bfa32bf",
          "order": 1,
          "text": "Нравятся ли вам игры в жанре 'шутер'?",
          "type": "single_choice",
          "required": true,
          "hidden_by_default": false,
          "options": [
            {
              "id": "a66a0963-ff3d-43fb-84a9-183532bf789a",
              "text": "Да",
              "weight": 0,
              "next_question_id": "8595a568-985a-4346-b01b-6de16453e47d"
            },
            {
              "id": "030f17c9-c39b-43ca-b022-00f5e5d6e656",
              "text": "Нет",
              "weight": 0,
              "next_question_id": "abe1b74d-5269-40a2-9485-8241a4f5fc5c"
            }
          ],
          "score_ranges": []
        },
        {
          "id": "8595a568-985a-4346-b01b-6de16453e47d",
          "section_id": "8d1d476c-b2c1-4850-a7ef-0cb20bfa32bf",
          "order": 2,
          "text": "Оцените средний уровень своего состояния под конец дня",
          "type": "rating",
          "required": true,
          "hidden_by_default": true,
          "options": [],
          "score_ranges": [
            {
              "from": 1,
              "to": 2,
              "weight": 10
            },
            {
              "from": 3,
              "to": 6,
              "weight": 0.5
            }
          ],
          "min": 1,
          "max": 10
        },
        {
          "id": "abe1b74d-5269-40a2-9485-8241a4f5fc5c",
          "section_id": "8d1d476c-b2c1-4850-a7ef-0cb20bfa32bf",
          "order": 3,
          "text": "Это вопрос 3",
          "type": "single_choice",
          "required": true,
          "hidden_by_default": true,
          "options": [
            {
              "id": "a16d9bc9-b8b0-472b-a36c-8685487f1864",
              "text": "в конец",
              "weight": 0,
              "next_question_id": "47c2cfbc-5087-4f02-93e7-5da832b970ca"
            },
            {
              "id": "c9649b4b-3f81-492b-947e-8992c683a145",
              "text": "kmlok",
              "weight": 0,
              "next_question_id": null
            }
          ],
          "score_ranges": []
        },
        {
          "id": "47c2cfbc-5087-4f02-93e7-5da832b970ca",
          "section_id": "8d1d476c-b2c1-4850-a7ef-0cb20bfa32bf",
          "order": 4,
          "text": "Напишите ваши увлечения (кратко)",
          "type": "text",
          "required": true,
          "hidden_by_default": false,
          "options": [],
          "score_ranges": []
        }
      ]
    }
  ],
  "metrics": []
})

const form = ref<Record<string, any>>({})
const answers = ref([])
const button_text = ref('Начать прохождение')
const error_message = ref('Пожалуйста, заполните все поля')
const testTitle = ref(testData.value.title)
const isCanTouchContinue = ref(false)
const firstTouchButton = ref(false)
const isTest = ref(false)

const visibleQuestions = ref<Set<string>>(new Set())



const flatQuestions = computed(() => {
  return testData.value.sections.flatMap(section => section.questions)
})

const recomputeVisibility = () => {
  const visible = new Set<string>()
  const questions = flatQuestions.value

  let i = 0

  while (i < questions.length) {
    const q = questions[i]
    if (!q) break

    // показываем если не скрыт или уже открыт
    if (!q.hidden_by_default || visible.has(q.id)) {
      visible.add(q.id)
    }

    const answer = form.value[q.id]

    if (!answer) {
      i++
      continue
    }

    // SINGLE
    if (q.type === 'single_choice') {
      const opt = q.options.find(o => o.text === answer)

      if (opt?.next_question_id) {
        const jumpIndex = questions.findIndex(x => x.id === opt.next_question_id)

        if (jumpIndex !== -1) {
          visible.add(opt.next_question_id)
          i = jumpIndex
          continue
        }
      }
    }

    // YES_NO
    if (q.type === 'yes_no') {
      const mappedAnswer = answer === 'yes' ? 'Да' : 'Нет'
      const opt = q.options.find(o => o.text === mappedAnswer)

      if (opt?.next_question_id) {
        const jumpIndex = questions.findIndex(x => x.id === opt.next_question_id)

        if (jumpIndex !== -1) {
          visible.add(opt.next_question_id)
          i = jumpIndex
          continue
        }
      }
    }

    // MULTIPLE
    if (q.type === 'multiple_choice') {
      let jumped = false

      for (const ans of answer) {
        const opt = q.options.find(o => o.text === ans)

        if (opt?.next_question_id) {
          const jumpIndex = questions.findIndex(x => x.id === opt.next_question_id)

          if (jumpIndex !== -1) {
            visible.add(opt.next_question_id)
            i = jumpIndex
            jumped = true
            break
          }
        }
      }

      if (jumped) continue
    }

    i++
  }

  visibleQuestions.value = visible
}

watch(
  () => form.value,
  () => {
    recomputeVisibility()
  },
  { deep: true, immediate: true }
)

const initForm = () => {
  const answers: Record<string, any> = {}
  answers['fio'] = ''
  answers['email'] = ''

  testData.value.client_fields.forEach(field => {
    answers[field.label] = ''
  })

  testData.value.sections.forEach(section => {
    section.questions.forEach(question => {
      // Инициализация в зависимости от типа
      if (question.type === 'single_choice') {
        answers[question.id] = null
      } else if (question.type === 'yes_no') {
        answers[question.id] = null
      } else if (question.type === 'number') {
        answers[question.id] = null
      } else if (question.type === 'text') {
        answers[question.id] = ''
      } else if (question.type === 'multiple_choice') {
        answers[question.id] = []
      } else if (question.type === 'range') {
        answers[question.id] = {}
      }
    })
  })

  form.value = answers
}

initForm()

const checkForm = () => {
  firstTouchButton.value = true
  
  const requiredDynamic = testData.value.client_fields
    .filter(f => f.required)
    .every(f => form.value[f.label]?.toString().trim())

  if (form.value.fio?.trim() && form.value.email?.trim() && requiredDynamic) {
    button_text.value = 'Закончить тест'
    isCanTouchContinue.value = true
    isTest.value = true
  }
}

const checkRequiredQuestions = () => {
  let allFilled = true

  for (const section of testData.value.sections) {
    for (const question of section.questions) {

      if (!visibleQuestions.value.has(question.id)) continue

      if (question.required) {
        const answer = form.value[question.id]

        if (question.type === 'multiple_choice') {
          if (!answer || answer.length === 0) allFilled = false
        } else if (question.type === 'slider') {
          if (answer === null || answer === undefined) allFilled = false
        } else {
          if (
            answer === null ||
            answer === undefined ||
            (typeof answer === 'string' && answer.trim() === '')
          ) {
            allFilled = false
          }
        }
      }
    }
  }

  return allFilled
}

const firstTouchButtonEndTest = ref(false)
const isCanTouchContinueTest = ref(false)
const downloadReport = ref(false)


function downloadReportTest(){

  console.log('FINAL RESULT:')
  const finalAnswers = getFinalAnswers()

  console.log('FINAL RESULT:', finalAnswers)

  if (downloadReport.value) {
    console.log(getFinalAnswers());

  }
}


const checkFormTest = () => {
  firstTouchButtonEndTest.value = true

  if (!checkRequiredQuestions()) {
    return
  }

  isCanTouchContinueTest.value = true
  isTest.value = false
  downloadReport.value = true

  // Собираем только видимые вопросы с текстами
  const finalAnswers: Record<string, any> = {}
  
  visibleQuestions.value.forEach(id => {
    const question = flatQuestions.value.find(q => q.id === id)
    if (!question) return
    
    finalAnswers[question.text] = form.value[id]
  })

  console.log('=== ОТВЕТЫ КЛИЕНТА ===')
  console.log('ФИО:', form.value.fio)
  console.log('Email:', form.value.email)
  testData.value.client_fields.forEach(f => {
    console.log(`${f.label}:`, form.value[f.label])
  })
  console.log('--- Ответы на вопросы ---')
  Object.entries(finalAnswers).forEach(([question, answer]) => {
    console.log(`${question}:`, answer)
  })
}



const checkMainLabels = () => {
  if (form.value.fio.trim() && form.value.email.trim()) {
    error_message.value = ''
    return
  }
  if (form.value.fio == '' && form.value.email == '') {
    error_message.value = 'Пожалуйста, заполните все поля'
    isCanTouchContinue.value = false
    return
  }
  if (form.value.fio.trim()) {
    isCanTouchContinue.value = false
    error_message.value = "Пожалуйста, заполните email"
    return
  }
  if (form.value.email.trim()) {
    isCanTouchContinue.value = false
    error_message.value = "Пожалуйста, заполните ФИО"
    return
  }
}


const dynamicForm = ref<Record<string, any>>({})
const result: Record<string, any> = {}
const getFinalAnswers = () => {
  const answers: { question_id: string; answer: any }[] = []

  visibleQuestions.value.forEach(id => {
    answers.push({
      question_id: id,
      answer: form.value[id]
    })
  })

  const guest_info: { field_label: string; value: any }[] = [
    { field_label: 'ФИО', value: form.value.fio },
    { field_label: 'Email', value: form.value.email },
    ...testData.value.client_fields.map(f => ({
      field_label: f.label,
      value: form.value[f.label]
    }))
  ]

  return { answers, guest_info }
}

// const dynamicFields = ref([
//   { label: "Ваш возраст: ", type: "number_select" },
//   { label: "Ваш любимый цвет", type: "color_select" }
// ])
const dynamicFields = testData.value.client_fields

const progress = computed(() => {
  const total = visibleQuestions.value.size
  if (total === 0) return 0
  const answered = [...visibleQuestions.value].filter(id => {
    const val = form.value[id]
    if (Array.isArray(val)) return val.length > 0
    return val !== null && val !== undefined && val !== ''
  }).length
  return Math.round((answered / total) * 100)
})


</script>
