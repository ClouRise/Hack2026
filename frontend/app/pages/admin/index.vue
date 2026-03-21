<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Психологи</h1>
      <button
        @click="showCreateModal = true"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        + Создать психолога
      </button>
    </div>

    <div class="bg-white rounded-2xl shadow-sm overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">ФИО</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">Email</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">Дата регистрации</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">Доступ до</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">Статус</th>
            <th class="text-left px-6 py-4 text-sm font-medium text-gray-500">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="psychologist in psychologists"
            :key="psychologist.id"
            class="border-b border-gray-100 hover:bg-gray-50"
          >
            <td class="px-6 py-4 font-medium text-gray-800">{{ psychologist.name }}</td>
            <td class="px-6 py-4 text-gray-600">{{ psychologist.email }}</td>
            <td class="px-6 py-4 text-gray-600">{{ formatDate(psychologist.created_at) }}</td>
            <td class="px-6 py-4 text-gray-600">{{ psychologist.access_until ?? 'Не ограничен' }}</td>
            <td class="px-6 py-4">
              <span
                :class="psychologist.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'"
                class="px-2 py-1 rounded-full text-xs font-medium"
              >
                {{ psychologist.is_active ? 'Активен' : 'Заблокирован' }}
              </span>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center gap-3">
                <button
                  @click="openEditModal(psychologist)"
                  class="text-sm text-blue-500 hover:text-blue-700"
                >
                  Редактировать
                </button>
                <button
                  @click="toggleBlock(psychologist)"
                  :class="psychologist.is_active ? 'text-red-400 hover:text-red-600' : 'text-green-500 hover:text-green-700'"
                  class="text-sm"
                >
                  {{ psychologist.is_active ? 'Заблокировать' : 'Разблокировать' }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модалка создания/редактирования -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="closeModals">
      <div class="bg-white rounded-2xl p-6 w-full max-w-md mx-4">
        <h2 class="text-lg font-semibold mb-4">{{ showEditModal ? 'Редактировать психолога' : 'Создать психолога' }}</h2>

        <div class="flex flex-col gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">ФИО</label>
            <input v-model="form.name" type="text" placeholder="Иванов Иван Иванович"
              class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input v-model="form.email" type="email" placeholder="ivan@example.com"
              class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Телефон</label>
            <input v-model="form.phone" type="text" placeholder="+7 999 999 99 99"
              class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div v-if="!showEditModal">
            <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
            <input v-model="form.password" type="password" placeholder="Придумайте пароль"
              class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Доступ до</label>
            <input v-model="form.access_until" type="date"
              class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
        </div>

        <div class="flex gap-3 mt-6">
          <button @click="closeModals" class="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50">
            Отмена
          </button>
          <button @click="handleSubmit" class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            {{ showEditModal ? 'Сохранить' : 'Создать' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: []
})

interface Psychologist {
  id: string
  name: string
  email: string
  phone?: string
  created_at: string
  access_until: string | null
  is_active: boolean
}

const psychologists = ref<Psychologist[]>([
  {
    id: '1',
    name: 'Иванова Мария Петровна',
    email: 'ivanova@example.com',
    created_at: '2026-01-15T10:00:00',
    access_until: '2026-12-31',
    is_active: true
  },
  {
    id: '2',
    name: 'Петров Алексей Сергеевич',
    email: 'petrov@example.com',
    created_at: '2026-02-20T10:00:00',
    access_until: null,
    is_active: false
  }
])

const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingId = ref<string | null>(null)

const form = reactive({
  name: '',
  email: '',
  phone: '',
  password: '',
  access_until: ''
})

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('ru-RU')
}

function openEditModal(psychologist: Psychologist) {
  form.name = psychologist.name
  form.email = psychologist.email
  form.phone = psychologist.phone ?? ''
  form.access_until = psychologist.access_until ?? ''
  editingId.value = psychologist.id
  showEditModal.value = true
}

function closeModals() {
  showCreateModal.value = false
  showEditModal.value = false
  editingId.value = null
  Object.assign(form, { name: '', email: '', phone: '', password: '', access_until: '' })
}

function toggleBlock(psychologist: Psychologist) {
  psychologist.is_active = !psychologist.is_active
  // TODO: подключить API
}

function handleSubmit() {
  if (showEditModal.value) {
    const p = psychologists.value.find(p => p.id === editingId.value)
    if (p) {
      p.name = form.name
      p.email = form.email
      p.phone = form.phone
      p.access_until = form.access_until || null
    }
  } else {
    psychologists.value.push({
      id: crypto.randomUUID(),
      name: form.name,
      email: form.email,
      phone: form.phone,
      created_at: new Date().toISOString(),
      access_until: form.access_until || null,
      is_active: true
    })
  }
  closeModals()
  // TODO: подключить API
}
</script>