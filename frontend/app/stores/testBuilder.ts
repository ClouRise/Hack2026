import { defineStore } from 'pinia'

export type QuestionType =
  | 'text'
  | 'textarea'
  | 'single_choice'
  | 'multiple_choice'
  | 'yes_no'
  | 'number'
  | 'slider'
  | 'date'
  | 'rating'

export interface QuestionOption {
  id: string
  text: string
  weight: number
  next_question_id: string | null
}

export interface BranchingCondition {
  if_options_selected: string[]
  next_question_id: string | null
}

export interface Branching {
  conditions: BranchingCondition[]
  default_next: string | null
}

export interface ScoreRange {
  from: number
  to: number
  weight: number
}

export interface Question {
  id: string
  section_id: string
  order: number
  text: string
  type: QuestionType
  required: boolean
  hidden_by_default: boolean
  options: QuestionOption[]       // для single_choice, multiple_choice
  min?: number                     // для slider, rating
  max?: number                     // для slider, rating
  branching: Branching | null
  date_subtype?: 'date' | 'time' | 'datetime'
  score_ranges?: ScoreRange[]
}

export interface Section {
  id: string
  order: number
  title: string
  questions: Question[]
}

export interface ClientField {
  label: string
  type: 'text' | 'email' | 'number' | 'color'
  required: boolean
}

export interface TestMeta {
  title: string
  description: string
  show_report_to_client: boolean
  client_fields: ClientField[]         // доп. поля которые клиент заполняет перед тестом
}

export interface Metric {
  id: string
  name: string
  operation: 'sum' | 'avg' | 'min' | 'max'
  question_ids: string[]
  coefficient: number
  description: string
}

export const useTestBuilderStore = defineStore('testBuilder', () => {
  const meta = ref<TestMeta>({
    title: '',
    description: '',
    show_report_to_client: false,
    client_fields: []
  })

  const sections = ref<Section[]>([])

  // Добавить секцию
  function addSection() {
    sections.value.push({
      id: crypto.randomUUID(),
      order: sections.value.length + 1,
      title: `Раздел ${sections.value.length + 1}`,
      questions: []
    })
  }

  // Удалить секцию
  function removeSection(sectionId: string) {
    sections.value = sections.value.filter(s => s.id !== sectionId)
  }

  // Добавить вопрос в секцию
  function addQuestion(sectionId: string) {
    const section = sections.value.find(s => s.id === sectionId)
    if (!section) return

    section.questions.push({
      id: crypto.randomUUID(),
      section_id: sectionId,
      order: section.questions.length + 1,
      text: '',
      type: 'text',
      required: true,
      hidden_by_default: false,
      options: [],
      branching: null,
      score_ranges: []   
    })
  }

  function setQuestionType(sectionId: string, questionId: string, type: QuestionType) {
  const section = sections.value.find(s => s.id === sectionId)
  const question = section?.questions.find(q => q.id === questionId)
  if (!question) return

  question.type = type
  question.options = []
  question.score_ranges = []

  if (type === 'yes_no') {
    question.options = [
      { id: crypto.randomUUID(), text: 'Да', weight: 0, next_question_id: null },
      { id: crypto.randomUUID(), text: 'Нет', weight: 0, next_question_id: null }
    ]
  }
}

  // Удалить вопрос
  function removeQuestion(sectionId: string, questionId: string) {
    const section = sections.value.find(s => s.id === sectionId)
    if (!section) return
    section.questions = section.questions.filter(q => q.id !== questionId)
  }

  // Обновить вопрос
  function updateQuestion(sectionId: string, questionId: string, data: Partial<Question>) {
    const section = sections.value.find(s => s.id === sectionId)
    if (!section) return
    const question = section.questions.find(q => q.id === questionId)
    if (!question) return
    Object.assign(question, data)
  }

  // Добавить вариант ответа
  function addOption(sectionId: string, questionId: string) {
    const section = sections.value.find(s => s.id === sectionId)
    const question = section?.questions.find(q => q.id === questionId)
    if (!question) return

    question.options.push({
      id: crypto.randomUUID(),
      text: '',
      weight: 0,
      next_question_id: null
    })
  }

  // Удалить вариант ответа
  function removeOption(sectionId: string, questionId: string, optionId: string) {
    const section = sections.value.find(s => s.id === sectionId)
    const question = section?.questions.find(q => q.id === questionId)
    if (!question) return
    question.options = question.options.filter(o => o.id !== optionId)
  }

  const metrics = ref<Metric[]>([])

  function addMetric() {
    metrics.value.push({
        id: crypto.randomUUID(),
        name: '',
        operation: 'sum',
        question_ids: [],
        coefficient: 1,
        description: ''
    })
    }

  function removeMetric(metricId: string) {
    metrics.value = metrics.value.filter(m => m.id !== metricId)
    }

  // Собрать финальный объект для отправки на бэк
  function buildPayload() {
    return {
      ...meta.value,
      sections: sections.value.map(s => ({
        ...s,
        questions: s.questions.map(q => ({ ...q }))
      })),
       metrics: metrics.value
    }
  }

  // Сбросить стор (после сохранения)
  function reset() {
    meta.value = {
      title: '',
      description: '',
      show_report_to_client: false,
      client_fields: []
    }
    sections.value = []
    metrics.value = []
  }

  function loadFromJson(data: any) {
  meta.value = {
    title: data.title || '',
    description: data.description || '',
    show_report_to_client: data.show_report_to_client || false,
    client_fields: data.client_fields || []
  }
  sections.value = data.sections || []
  metrics.value = data.metrics || []
}

  

  return {
    meta,
    sections,
    metrics,
    addMetric,
    removeMetric,
    addSection,
    removeSection,
    addQuestion,
    removeQuestion,
    updateQuestion,
    setQuestionType,
    addOption,
    removeOption,
    buildPayload,
    reset,
    loadFromJson
  }
})