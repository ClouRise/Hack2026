<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl BP-B text-green-dark">Психологи</h1>
      <button
        @click="showCreateModal = true"
        class="px-6 cursor-pointer py-2 text-white text-xl BP-B rounded bg-green-bright hover:bg-green-bright transition"
      >
        + Создать психолога
      </button>
    </div>

    <div class="bg-white rounded-lg overflow-hidden card-test-shadows">
      <table class="w-full">
        <thead class="bg-bg-light border-b border-gray-light">
          <tr>
            <th class="text-left px-6 py-3 leading-[1.1] text-lg G-M text-gray-medium">ФИО</th>
            <th class="text-left px-6 py-3 leading-[1.1] text-sm G-M text-gray-medium">Email</th>
            <th class="text-left px-6 py-3 leading-[1.1] text-sm G-M text-gray-medium">Дата регистрации</th>
            <th class="text-left px-6 py-3 leading-[1.1] text-sm G-M text-gray-medium">Доступ до</th>
            <th class="text-left px-6 py-3 leading-[1.1] text-sm G-M text-gray-medium">Статус</th>
            <th class="text-left px-6 py-3 leading-[1.1] text-sm G-M text-gray-medium">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="psychologist in psychologists"
            :key="psychologist.id"
            class="border-b border-bg-light hover:bg-bg-light transition"
          >
            <td class="px-6 py-4">
              <p class="BP-B leading-[1.1] text-green-dark">{{ psychologist.name }}</p>
            </td>
            <td class="px-6 py-4 G-M text-gray-medium">{{ psychologist.email }}</td>
            <td class="px-6 py-4 G-M text-gray-medium">{{ formatDate(psychologist.created_at) }}</td>
            <td class="px-6 py-4 G-M text-gray-medium">{{ psychologist.access_until ?? 'Не ограничен' }}</td>
            <td class="px-6 py-4">
              <span
                :class="psychologist.is_active ? 'bg-bg-light border-l-[5px] border-green-bright text-green-dark2' : 'border-l-[5px] text-bg-red bg-color-red-user blocked-user'"
                class="px-3 py-2 text-xs G-M"
              >
                {{ psychologist.is_active ? 'Активен' : 'Заблокирован' }}
              </span>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center gap-3">
                <button
                  @click="openEditModal(psychologist)"
                  class="text-sm G-M cursor-pointer text-green-600 hover:text-green-800 whitespace-nowrap"
                >
                  Редактировать
                </button>
                <button
                  @click="toggleBlock(psychologist)"
                  class="text-sm G-M whitespace-nowrap cursor-pointer text-gray-600 hover:text-gray-400"
                >
                  {{ psychologist.is_active ? 'Заблокировать' : 'Разблокировать' }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модалка -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-green-dark/70 flex items-center justify-center z-50" @click.self="closeModals">
      <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4 card-test-shadows">
        <h2 class="text-xl BP-B text-green-dark mb-6">{{ showEditModal ? 'Редактировать психолога' : 'Создать психолога' }}</h2>

        <div class="flex flex-col gap-4">
          <div>
            <label class="block text-[10pt] G-M text-gray-light mb-1">ФИО</label>
            <input v-model="form.name" type="text" placeholder="Иванов Иван Иванович"
              class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright" />
          </div>
          <div>
            <label class="block text-[10pt] G-M text-gray-light mb-1">Email</label>
            <input v-model="form.email" type="email" placeholder="ivan@example.com"
              class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright" />
          </div>
          <div>
            <label class="block text-[10pt] G-M text-gray-light mb-1">Телефон</label>
            <input v-model="form.phone" type="text" placeholder="+7 999 999 99 99"
              class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright" />
          </div>
          <div v-if="!showEditModal">
            <label class="block text-[10pt] G-M text-gray-light mb-1">Пароль</label>
            <input v-model="form.password" type="password" placeholder="Придумайте пароль"
              class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright" />
          </div>
          <div>
            <label class="block text-[10pt] G-M text-gray-light mb-1">Доступ до</label>
            <input v-model="form.access_until" type="date"
              class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright" />
          </div>
        </div>

        <div class="flex gap-3 mt-6">
          <button @click="closeModals" class="flex-1 px-4 py-2 border-2 border-gray-light text-gray-medium G-M rounded hover:border-green-dark hover:text-green-dark transition">
            Отмена
          </button>
          <button @click="handleSubmit" class="flex-1 px-4 py-2 bg-green-bright text-white BP-B rounded hover:bg-green-dark transition">
            {{ showEditModal ? 'Сохранить' : 'Создать' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

definePageMeta({
  middleware: [],
  layout: "admin"
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

<style lang="css" scoped>
.blocked-user{
  border-color: #754444;
}
</style>