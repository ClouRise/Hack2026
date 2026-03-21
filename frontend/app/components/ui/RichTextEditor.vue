<template>
  <div class="flex flex-col border-l-[5px] border-b-[2px] border-gray-light bg-bg-light">
    <QuillEditor
      v-model:content="content"
      content-type="html"
      :options="options"
      style="min-height: 150px"
    />
  </div>
</template>

<script setup lang="ts">
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const content = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const options = {
  theme: 'snow',
  modules: {
    toolbar: [
      ['bold', 'italic', 'underline'],
      [{ header: [1, 2, 3, false] }],
      [{ list: 'ordered' }, { list: 'bullet' }],
      [{ align: [] }],  // добавляем выравнивание
      ['link'],    ]
  }
}
</script>

<style>
.ql-toolbar {
  border: none !important;
  border-top: 1px solid #9BB299 !important;
  order: 2;
  background-color: #F1FAF0;
  font-family: 'GothamOffice-medium', sans-serif;
}
.ql-container {
  border: none !important;
  order: 1;
  background-color: #F1FAF0;
  font-family: 'GothamOffice-medium', sans-serif;
  color: #144210;
}
.ql-editor {
  min-height: 150px;
}
/* скрываем встроенные подсказки яндекса */
.ql-editor * {
  -webkit-user-select: text;
}
</style>