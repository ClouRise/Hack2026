<template>
          <!-- Заголовок -->
          <div class="text-xs text-green-light">Тест:</div>
          <div class="text-3xl BP-B text-green-dark leading-[0.9] mt-0">{{ testTitle }}</div>

          <!-- Разделитель -->
          <div class="flex justify-center my-4">
            <div class="w-80 h-px bg-gray-300"></div>
          </div>

        <div v-if="!isCanTouchContinue">

          <!-- Описание -->
          <div class="text-[10pt] leading-[1.1] text-gray-medium G-M mb-6">
            Перед началом выполнения теста, вы должны заполнить информацию о себе.
          </div>

          <!-- Инпуты -->
          <div class="space-y-4">
            <div>
              <label class="block text-[10pt] text-gray-light G-M mb-1">Ваше ФИО</label>
              <input 
                @input="checkMainLabels"
                v-model="form.fio" 
                type="text" 
                class="w-full px-3 py-2 text-green-dark bg-bg-light border-l-[5px] border-b-[2px] border-gray-light focus:outline-none focus:border-green-bright G-M"
              />
            </div>
            
            <div>
              <label class="block text-[10pt] text-gray-light G-M  mb-1">Ваша почта</label>
              <input 
                @input="checkMainLabels"
                v-model="form.email" 
                type="email" 
                class="w-full px-3 py-2 text-green-dark bg-bg-light border-l-[5px] border-b-[2px] border-gray-light focus:outline-none focus:border-green-bright G-M"
              />
            </div>
          </div>

          <!-- Динамические поля из JSON -->
          <div v-if="dynamicFields === null" class="space-y-4 mt-4">
            <div v-for="(field, index) in dynamicFields" :key="index">
              <label class="block text-[10pt] text-gray-light G-M  mb-1">{{ field.label }}</label>
              <select 
                v-if="field.type === 'number_select'" 
                v-model="dynamicForm[field.label]"
                class="w-full px-3 py-2 text-green-dark bg-bg-light border-l-[5px] border-b-[2px] border-gray-light focus:outline-none focus:border-green-bright G-M"
              >
                <option v-for="n in 100" :key="n" :value="n">{{ n }}</option>
              </select>
              
              <input 
                v-else-if="field.type === 'color_select'" 
                type="color"
                v-model="dynamicForm[field.label]"
                class=""
              />
            </div>
          </div>

        </div>
          <Button @click="checkForm" class="bg-green-bright hover:bg-green-bright mt-8 w-full px-4 py-2 text-white rounded hover:bg-green-600 text-xl BP-B">
            {{ button_text }}
          </Button>

          <p v-if="!isCanTouchContinue && firstTouchButton" class="text-center text-rose-400 relative top-[10px] text-sm">{{ error_message }}</p>

</template>

<script setup lang="ts">
definePageMeta({
  layout: 'empty'
})
const route = useRoute()
const testId = route.params.id 

import { ref } from 'vue'

const button_text = ref('Начать прохождение')
const error_message = ref('Пожалуйста, заполните все поля')
const testTitle = ref('Название теста')
const isCanTouchContinue = ref(false)
const firstTouchButton = ref(false)
const isTest = ref(false)

const form = ref({
  fio: '',
  email: ''
})

const checkForm = () => {
  firstTouchButton.value = true
  if (form.value.fio.trim() && form.value.email.trim()) {
    button_text.value = 'Закончить тест'
    isCanTouchContinue.value = true
    isTest.value = true
  }
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

// const dynamicFields = ref([
//   { label: "Ваш возраст: ", type: "number_select" },
//   { label: "Ваш любимый цвет", type: "color_select" }
// ])
const dynamicFields = null
</script>