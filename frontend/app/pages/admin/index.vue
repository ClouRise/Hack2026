<template>
  <div>
    <!-- Шапка -->
    <div class="mb-6">
      <h1 class="text-2xl sm:text-3xl BP-B text-green-dark mb-3">Психологи</h1>
      <button
        @click="showCreateModal = true"
        class="px-4 py-2 cursor-pointer text-white text-sm sm:text-xl BP-B rounded bg-green-bright hover:bg-green-bright transition"
      >
        + Создать психолога
      </button>
    </div>

    <!-- ДЕСКТОП (md+): таблица -->
    <div class="hidden md:block bg-white rounded-lg overflow-hidden card-test-shadows">
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
                :class="!psychologist.is_blocked ? 'bg-bg-light border-l-[5px] border-green-bright text-green-dark2' : 'border-l-[5px] text-bg-red bg-color-red-user blocked-user'"
                class="px-3 py-2 text-xs G-M"
              >
                {{ !psychologist.is_blocked ? 'Активен' : 'Заблокирован' }}
              </span>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center gap-3">
                <button
                  @click="toggleBlock(psychologist)"
                  class="text-sm G-M whitespace-nowrap cursor-pointer text-gray-600 hover:text-gray-400"
                >
                  {{ !psychologist.is_blocked ? 'Заблокировать' : 'Разблокировать' }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- МОБИЛЬНЫЙ + ПЛАНШЕТ (< md): карточки -->
    <div class="md:hidden flex flex-col gap-3">
      <div v-for="psychologist in psychologists" :key="psychologist.id"
        class="bg-white rounded-lg p-3 card-test-shadows flex flex-col gap-3">

        <!-- Имя + статус -->
        <div class="flex items-start justify-between gap-2">
          <p class="BP-B text-base text-green-dark leading-[1.2]">{{ psychologist.name }}</p>
          <span
            :class="!psychologist.is_blocked ? 'bg-bg-light border-l-[5px] border-green-bright text-green-dark2' : 'border-l-[5px] text-bg-red bg-color-red-user blocked-user'"
            class="flex-shrink-0 px-2 py-1 text-xs G-M"
          >
            {{ !psychologist.is_blocked ? 'Активен' : 'Заблокирован' }}
          </span>
        </div>

        <!-- Детали -->
        <div class="flex flex-col gap-1">
          <p class="text-xs G-M text-gray-medium truncate">{{ psychologist.email }}</p>
          <div class="flex items-center gap-3">
            <p class="text-xs G-M text-gray-medium">
              Рег: {{ formatDate(psychologist.created_at) }}
            </p>
            <p class="text-xs G-M text-gray-medium">
              Доступ: {{ psychologist.access_until ?? 'Не ограничен' }}
            </p>
          </div>
        </div>

        <!-- Действия -->
        <div class="flex items-center gap-3 border-t border-bg-light pt-2">
          <button @click="openEditModal(psychologist)"
            class="text-xs G-M cursor-pointer text-green-600 hover:text-green-800">
            Редактировать
          </button>
          <button @click="toggleBlock(psychologist)"
            class="text-xs G-M cursor-pointer text-gray-600 hover:text-gray-400">
            {{ !psychologist.is_blocked ? 'Заблокировать' : 'Разблокировать' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Модалка — без изменений, уже адаптивная через max-w-md mx-4 -->
    <div v-if="showCreateModal || showEditModal"
      class="fixed inset-0 bg-green-dark/70 flex items-center justify-center z-50"
      @click.self="closeModals">
      <div class="bg-white rounded-xl p-5 sm:p-6 w-full max-w-md mx-4 card-test-shadows">
        <h2 class="text-xl BP-B text-green-dark mb-6">
          {{ showEditModal ? 'Редактировать психолога' : 'Создать психолога' }}
        </h2>

        <div class="flex flex-col gap-4">
          <div>
            <label class="block text-[10pt] G-M text-gray-light mb-1">ФИО</label>
            <input v-model="form.name" type="text" placeholder="Иванов Иван Иванович"
              :class="errors.name ? 'border-rose-400' : 'border-gray-light'"
              class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] text-green-dark G-M focus:outline-none focus:border-green-bright" />
            <p v-if="errors.name" class="text-rose-400 text-[9pt] G-M mt-1">{{ errors.name }}</p>
          </div>
          <div>
            <label class="block text-[10pt] G-M text-gray-light mb-1">Email</label>
            <input v-model="form.email" type="email" placeholder="ivan@example.com"
              :class="errors.email ? 'border-rose-400' : 'border-gray-light'"
              class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] text-green-dark G-M focus:outline-none focus:border-green-bright" />
            <p v-if="errors.email" class="text-rose-400 text-[9pt] G-M mt-1">{{ errors.email }}</p>
          </div>
          <div>
            <label class="block text-[10pt] G-M text-gray-light mb-1">Телефон</label>
            <input v-model="form.phone" type="text" placeholder="+7 999 999 99 99"
              :class="errors.phone ? 'border-rose-400' : 'border-gray-light'"
              class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] text-green-dark G-M focus:outline-none focus:border-green-bright" />
            <p v-if="errors.phone" class="text-rose-400 text-[9pt] G-M mt-1">{{ errors.phone }}</p>
          </div>
          <div>
            <label class="block text-[10pt] G-M text-gray-light mb-1">Доступ до</label>
            <input v-model="form.access_until" type="date"
              class="w-full px-3 py-2 bg-bg-light border-l-[5px] border-b-[2px] border-gray-light text-green-dark G-M focus:outline-none focus:border-green-bright text-base" />
          </div>
        </div>

        <div class="flex gap-3 mt-6">
          <button @click="closeModals"
            class="flex-1 px-4 py-2 border-2 border-gray-light text-gray-medium G-M rounded hover:border-green-dark hover:text-green-dark transition">
            Отмена
          </button>
          <button @click="handleSubmit"
            class="flex-1 px-4 py-2 bg-green-bright text-white BP-B rounded hover:bg-green-dark transition">
            {{ showEditModal ? 'Сохранить' : 'Создать' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

definePageMeta({
  middleware: ['auth'],
  layout: "admin"
})

const { api } = useApi()
const authStore = useAuthStore()

interface Psychologist {
  id: string
  name: string
  email: string
  phone?: string
  created_at: string
  access_until: string | null
  is_blocked: boolean  // бек возвращает is_blocked, не is_active
}

const psychologists = ref<Psychologist[]>([])

// Загрузка списка
async function fetchPsychologists() {
  try {
    const result = await api('/users/admin') as Psychologist[]
    console.log('PSYCHOLOGISTS:', result)
    psychologists.value = result
  } catch (e) {
    console.error('Ошибка загрузки:', e)
  }
}

onMounted(() => fetchPsychologists())

const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingId = ref<string | null>(null)
const tempPassword = ref<string | null>(null)

const form = reactive({
  name: '',
  email: '',
  phone: '',
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
  tempPassword.value = null
  Object.assign(form, { name: '', email: '', phone: '', access_until: '' })
  Object.assign(errors, { name: '', email: '', phone: '' })
}

async function toggleBlock(psychologist: Psychologist) {
  try {
    const endpoint = psychologist.is_blocked
      ? `/users/${psychologist.id}/unblock`
      : `/users/${psychologist.id}/block`
    await api(endpoint, { method: 'POST' })
    psychologist.is_blocked = !psychologist.is_blocked
  } catch (e) {
    console.error('Ошибка блокировки:', e)
  }
}

const errors = reactive({
  name: '',
  email: '',
  phone: ''
})

function validate() {
  errors.name = ''
  errors.email = ''
  errors.phone = ''

  let valid = true

  if (!form.name.trim()) {
    errors.name = 'Заполните ФИО'
    valid = false
  }

  if (!form.email.trim()) {
    errors.email = 'Заполните email'
    valid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Некорректный email'
    valid = false
  }

  if (form.phone && !/^\+?[0-9\s\-()]{7,20}$/.test(form.phone)) {
    errors.phone = 'Некорректный номер телефона'
    valid = false
  }

  return valid
}


async function handleSubmit() {
  if (!validate()) return

  try {
    if (showEditModal.value) {
      closeModals()
    } else {
      await api('/users/create', {
        method: 'POST',
        body: {
          name: form.name,
          email: form.email,
          phone: form.phone || undefined,
          access_until: form.access_until || undefined
        }
      })

      await fetchPsychologists()
      closeModals()
      alert('Психолог создан! Пароль отправлен на почту.')
    }
  } catch (e: any) {
    console.error('Ошибка:', e)

    // Ошибки с бека — подсвечиваем нужное поле
    const detail = e?.data?.detail
    if (typeof detail === 'string') {
      if (detail.toLowerCase().includes('email')) {
        errors.email = detail
      } else {
        errors.name = detail
      }
    } else {
      errors.name = 'Ошибка при создании, попробуйте снова'
    }
  }
}

</script>

<style lang="css" scoped>
.blocked-user{
  border-color: #754444;
}
</style>