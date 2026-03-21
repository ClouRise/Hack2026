<template>
  <div class="flex flex-col border border-gray-300 rounded-lg">
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
  order: 2;
  border-top: 1px solid #e5e7eb !important;
  border-bottom: none !important;
}
.ql-container {
  order: 1;
  border-bottom: none !important;
}
.ql-editor {
  min-height: 150px;
}
/* скрываем встроенные подсказки яндекса */
.ql-editor * {
  -webkit-user-select: text;
}
</style>