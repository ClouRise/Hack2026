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
      <div class="w-80 h-px bg-gray-300"></div>
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
              <div class="w-full h-px bg-gray-200"></div>
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
        <p class="BP-M text-sm text-gray-800 leading-[0.9]">
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

const testData = ref({
  "title": "тест миши",
  "description": "Приве",
  "show_report_to_client": true,
  "client_fields": [
    {
      "label": "Введите ЭМАИЛ",
      "type": "email",
      "required": true
    },
    {
      "label": "ВВЕДИТЕ Во з раст",
      "type": "number",
      "required": true
    },
    {
      "label": "укажите ваш кольор",
      "type": "color",
      "required": false
    },
    {
      "label": "скок у вас IQ?",
      "type": "number",
      "required": false
    }
  ],
  "sections": [
    {
      "id": "553b2a89-6d8f-43be-86cb-7f4c6de591c6",
      "order": 1,
      "title": "Раздел 1",
      "questions": [
        {
          "id": "914a89ec-02ec-46c0-b349-0e546e9f3552",
          "section_id": "553b2a89-6d8f-43be-86cb-7f4c6de591c6",
          "order": 1,
          "text": "Как вы любите проводить свободное время?",
          "type": "textarea",
          "required": true,
          "hidden_by_default": true,
          "options": [],
          "score_ranges": []
        },
        {
          "id": "6a96cc0e-4f4c-45a1-a89b-3b3023222312",
          "section_id": "553b2a89-6d8f-43be-86cb-7f4c6de591c6",
          "order": 2,
          "text": "Каким фреймворком пользуетесь?",
          "type": "single_choice",
          "required": false,
          "hidden_by_default": false,
          "options": [
            {
              "id": "112a7178-6ea8-46b6-a624-b7f34a0f3d21",
              "text": "vue",
              "weight": 3,
              "next_question_id": null
            },
            {
              "id": "5c3e00e5-5425-4872-bf38-c5f6824daa6d",
              "text": "nuxt",
              "weight": 5,
              "next_question_id": null
            },
            {
              "id": "d8e4fa5e-5c30-4ea3-82a0-0a01cbe8b821",
              "text": "react",
              "weight": 3,
              "next_question_id": null
            }
          ],
          "score_ranges": []
        },
        {
          "id": "e8752be0-08d6-449b-963b-9b91297b8514",
          "section_id": "553b2a89-6d8f-43be-86cb-7f4c6de591c6",
          "order": 3,
          "text": "какие ЯП знаете?",
          "type": "multiple_choice",
          "required": true,
          "hidden_by_default": false,
          "options": [
            {
              "id": "84b69737-aa1f-4061-9643-6313f1fc1fb6",
              "text": "c++",
              "weight": 10,
              "next_question_id": null
            },
            {
              "id": "45282192-a9af-49d9-89f5-22bab6c18d1b",
              "text": "python",
              "weight": 6,
              "next_question_id": null
            },
            {
              "id": "f2bdeec6-831f-42b5-ba8b-cfc3d96de90e",
              "text": "js",
              "weight": 5,
              "next_question_id": null
            }
          ],
          "score_ranges": []
        },
        {
          "id": "9b90ecde-a680-4c53-864d-31bbb5f9996e",
          "section_id": "553b2a89-6d8f-43be-86cb-7f4c6de591c6",
          "order": 4,
          "text": "вы любите мишу?",
          "type": "single_choice",
          "required": true,
          "hidden_by_default": false,
          "options": [
            {
              "id": "d21af319-7ddd-4e62-8b67-84ca5472b842",
              "text": "Да",
              "weight": 100,
              "next_question_id": null
            },
            {
              "id": "4fde9c4b-3688-4a6b-ad5e-e910959a6486",
              "text": "НЕ",
              "weight": -100,
              "next_question_id": "fb3fd394-530a-43c5-9c5a-30df044f5c87"
            },
            {
              "id": "f524310a-a818-4baf-b897-35076d51839c",
              "text": "не знаю",
              "weight": 0,
              "next_question_id": "0139427b-811b-4cf8-a994-27ad2d22f299"
            }
          ],
          "score_ranges": []
        },
        {
          "id": "0139427b-811b-4cf8-a994-27ad2d22f299",
          "section_id": "553b2a89-6d8f-43be-86cb-7f4c6de591c6",
          "order": 5,
          "text": "сколько вам лет?",
          "type": "number",
          "required": true,
          "hidden_by_default": true,
          "options": [],
          "score_ranges": []
        },
        {
          "id": "85c06565-9a89-41c4-bb12-174e957dde47",
          "section_id": "553b2a89-6d8f-43be-86cb-7f4c6de591c6",
          "order": 6,
          "text": "в какое время вы обычно активничаете?",
          "type": "slider",
          "required": true,
          "hidden_by_default": false,
          "options": [],
          "score_ranges": [
            {
              "from": 6,
              "to": 10,
              "weight": 10
            },
            {
              "from": 10,
              "to": 16,
              "weight": 5
            },
            {
              "from": 16,
              "to": 24,
              "weight": 3
            }
          ],
          "min": 6,
          "max": 24
        },
        {
          "id": "2a0224dd-7170-48ac-a8bf-7117556e27a7",
          "section_id": "553b2a89-6d8f-43be-86cb-7f4c6de591c6",
          "order": 7,
          "text": "Когда вы узнали о своем рождении?",
          "type": "date",
          "required": true,
          "hidden_by_default": false,
          "options": [],
          "score_ranges": [],
          "date_subtype": "datetime"
        },
        {
          "id": "9aa2714e-2fa3-41e6-8f23-04192b5ee78f",
          "section_id": "553b2a89-6d8f-43be-86cb-7f4c6de591c6",
          "order": 8,
          "text": "Оцените тест",
          "type": "rating",
          "required": true,
          "hidden_by_default": false,
          "options": [],
          "score_ranges": [
            {
              "from": 1,
              "to": 3,
              "weight": -100
            },
            {
              "from": 3,
              "to": 7,
              "weight": 0
            },
            {
              "from": 7,
              "to": 10,
              "weight": 100
            }
          ],
          "min": 1,
          "max": 10
        },
        {
          "id": "fb3fd394-530a-43c5-9c5a-30df044f5c87",
          "section_id": "553b2a89-6d8f-43be-86cb-7f4c6de591c6",
          "order": 9,
          "text": "пошел тогда нафиг дебил",
          "type": "text",
          "required": true,
          "hidden_by_default": true,
          "options": [],
          "score_ranges": []
        },
        {
          "id": "7deb8347-f2e8-4a21-a79e-812d85633046",
          "section_id": "553b2a89-6d8f-43be-86cb-7f4c6de591c6",
          "order": 10,
          "text": "Вам понравился тест?",
          "type": "yes_no",
          "required": true,
          "hidden_by_default": false,
          "options": [
            {
              "id": "1abe52c1-4191-4984-805c-2f739b44660d",
              "text": "Да",
              "weight": 100,
              "next_question_id": null
            },
            {
              "id": "2e7ea408-a5a3-43a3-b416-b38b2cf69bdb",
              "text": "Нет",
              "weight": -100,
              "next_question_id": null
            }
          ],
          "score_ranges": []
        },
        {
          "id": "ace64d9f-d972-4001-b852-fa7ddf7e5b79",
          "section_id": "553b2a89-6d8f-43be-86cb-7f4c6de591c6",
          "order": 11,
          "text": "Еще раз ответьте",
          "type": "single_choice",
          "required": true,
          "hidden_by_default": false,
          "options": [
            {
              "id": "33f46791-672e-46e1-948b-e73ffc71a750",
              "text": "Да",
              "weight": 0,
              "next_question_id": "4bec3b50-f608-4a74-bf43-1552b834c048"
            },
            {
              "id": "259d46fc-2b53-4970-9795-6beece899b46",
              "text": "Нет",
              "weight": 0,
              "next_question_id": "f1780c1d-e61f-4d10-85af-c10937f77b74"
            }
          ],
          "score_ranges": []
        }
      ]
    },
    {
      "id": "03ea1ba5-8211-49d8-938b-569cd6f1f2e6",
      "order": 2,
      "title": "Раздел 2",
      "questions": [
        {
          "id": "444bdad2-f7a9-4c95-9a79-62c8ba4907da",
          "section_id": "03ea1ba5-8211-49d8-938b-569cd6f1f2e6",
          "order": 1,
          "text": "Опишите свои ощущения от теста.",
          "type": "textarea",
          "required": true,
          "hidden_by_default": false,
          "options": [],
          "score_ranges": []
        },
        {
          "id": "4bec3b50-f608-4a74-bf43-1552b834c048",
          "section_id": "03ea1ba5-8211-49d8-938b-569cd6f1f2e6",
          "order": 2,
          "text": "Скажите чем понравился тест",
          "type": "textarea",
          "required": true,
          "hidden_by_default": true,
          "options": [],
          "score_ranges": []
        },
        {
          "id": "f1780c1d-e61f-4d10-85af-c10937f77b74",
          "section_id": "03ea1ba5-8211-49d8-938b-569cd6f1f2e6",
          "order": 3,
          "text": "Скажите чем не понравился тест",
          "type": "textarea",
          "required": true,
          "hidden_by_default": true,
          "options": [],
          "score_ranges": []
        }
      ]
    }
  ],
  "metrics": [
    {
      "id": "8cb27342-d3e5-4b10-980a-a0312215913d",
      "name": "уровень iq",
      "operation": "sum",
      "question_ids": [
        "9b90ecde-a680-4c53-864d-31bbb5f9996e",
        "9aa2714e-2fa3-41e6-8f23-04192b5ee78f",
        "0139427b-811b-4cf8-a994-27ad2d22f299"
      ],
      "coefficient": 1,
      "description": "Метрика по определению уровня интеллекта",
      "interpretations": [
        {
          "from": -200,
          "to": 0,
          "description": "вы дебил тупой"
        },
        {
          "from": 0,
          "to": 1000,
          "description": "вы красавчик и умный"
        }
      ]
    },
    {
      "id": "0c42e89a-fccf-468c-a179-00ceab0d9b8b",
      "name": "уровень психоза",
      "operation": "sum",
      "question_ids": [
        "7deb8347-f2e8-4a21-a79e-812d85633046",
        "6a96cc0e-4f4c-45a1-a89b-3b3023222312",
        "85c06565-9a89-41c4-bb12-174e957dde47"
      ],
      "coefficient": 1,
      "description": "Метрика считает шото и определяет ответ",
      "interpretations": [
        {
          "from": -200,
          "to": 0,
          "description": "пипец ты дурак нафиг"
        },
        {
          "from": 0,
          "to": 1000,
          "description": "все отлично, удачи!"
        }
      ]
    }
  ]
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
