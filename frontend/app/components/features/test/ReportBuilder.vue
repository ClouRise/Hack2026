<template>
  <div class="bg-white rounded-2xl p-6 mb-4 card-test-shadows">
    <h2 class="text-xl BP-B text-green-dark mb-6">Конструктор отчётов</h2>

    <div class="grid grid-cols-2 gap-6">
      <div>
        <h3 class="BP-M text-green-dark mb-3">Отчёт для клиента</h3>
        <ReportTemplateEditor
          :blocks="store.meta.report_template.client"
          @update="store.meta.report_template.client = $event"
        />
      </div>
      <div>
        <h3 class="BP-M text-green-dark mb-3">Отчёт для психолога</h3>
        <ReportTemplateEditor
          :blocks="store.meta.report_template.psychologist"
          @update="store.meta.report_template.psychologist = $event"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import ReportTemplateEditor from './ReportTemplateEditor.vue';
const store = useTestBuilderStore()
</script>