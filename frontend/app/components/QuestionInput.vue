<template>
    <div>
        <!-- Число -->
        <input v-if="type === 'number'" type="number" :value="value"
            @input="updateValue(($event.target as HTMLInputElement).value)"
            class="w-full px-3 py-2 text-green-dark bg-bg-light border-l-[5px] border-b-[2px] border-gray-light focus:outline-none focus:border-green-bright G-M" />

        <!-- Текст -->
        <input v-else-if="type === 'text'" type="text" :value="value"
            @input="updateValue(($event.target as HTMLInputElement).value)"
            class="w-full px-3 py-2 text-green-dark bg-bg-light border-l-[5px] border-b-[2px] border-gray-light focus:outline-none focus:border-green-bright G-M" />

        <!-- Ползунок -->
        <input v-else-if="type === 'rating'" type="range" :value="value"
            @input="updateValue(($event.target as HTMLInputElement).value)" :min="min" :max="max"
            class="w-full slider-custom" />

        <!-- Двойной ползунок (диапазон) -->
        <div v-else-if="type === 'slider'" class="dual-slider-container">
            <div class="slider-wrapper">
                <div class="slider-track">
                    <div class="slider-range" :style="rangeStyle"></div>
                </div>
                <input ref="minSlider" type="range" :value="rangeValue.min" @input="updateMin" :min="min" :max="max"
                    class="dual-slider-input dual-slider-input-min" :class="{ 'reversed': isReversed }" />
                <input ref="maxSlider" type="range" :value="rangeValue.max" @input="updateMax" :min="min" :max="max"
                    class="dual-slider-input dual-slider-input-max" :class="{ 'reversed': isReversed }" />
            </div>
            <div class="slider-labels relative">
                <span class="slider-value-min">{{ formatValue(rangeValue.min) }}</span>
                <span class="slider-value-max">{{ formatValue(rangeValue.max) }}</span>
            </div>
        </div>

        <!-- Радио -->
        <div v-else-if="type === 'single_choice'" class="space-y-2">
            <label v-for="opt in options" :key="opt" class="flex items-center gap-2">
                <input class="radio-custom" type="radio" :value="opt" :checked="value === opt"
                    @change="updateValue(opt)" />
                <span class="G-M text-gray-main text-[12pt]">{{ opt }}</span>
            </label>
        </div>

        <!-- Чекбоксы -->
        <div v-else-if="type === 'multiple_choice'" class="space-y-2">
            <label v-for="opt in options" :key="opt" class="flex items-center gap-2">
                <input type="checkbox" class="checkbox-custom" :value="opt" :checked="value?.includes(opt)"
                    @change="toggleCheckbox(opt)" />
                <span>{{ opt }}</span>
            </label>
        </div>

        <!-- Дата -->
        <input v-else-if="type === 'date'" :type="dateSubtype === 'datetime' ? 'datetime-local' : 'date'" :value="value"
            @input="updateValue(($event.target as HTMLInputElement).value)"
            class="w-full px-3 py-2 text-green-dark bg-bg-light border-l-[5px] border-b-[2px] border-gray-light focus:outline-none focus:border-green-bright G-M" />

        <!-- Да/Нет -->
        <div v-else-if="type === 'yes_no'" class="flex gap-4">
            <label class="flex items-center gap-2 G-M text-gray-main text-[12pt]">
                <input class="radio-custom" type="radio" :checked="value === 'yes'" @change="updateValue('yes')" /> Да
            </label>
            <label class="flex items-center gap-2 G-M text-gray-main text-[12pt]">
                <input class="radio-custom" type="radio" :checked="value === 'no'" @change="updateValue('no')" /> Нет
            </label>
        </div>

        <!-- Текстареа -->
        <textarea v-else-if="type === 'textarea'" :value="value"
            @input="updateValue(($event.target as HTMLTextAreaElement).value)" rows="4"
            class="w-full px-3 py-2 h-[70px] resize-y max-h-[200px] w-full px-3 py-2 text-green-dark bg-bg-light border-l-[5px] border-b-[2px] border-gray-light focus:outline-none focus:border-green-bright G-M"></textarea>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
    type: string
    options?: string[]
    min?: number
    max?: number
    dateSubtype?: string
}>()

const value = defineModel<any>()
const selected = defineModel<any>('selected')

const selectedValue = computed(() => selected.value)

const updateValue = (val: any) => {
    value.value = val
}

const rangeValue = computed({
    get: () => value.value || { min: props.min || 0, max: props.max || 100 },
    set: (val) => value.value = val
})

const minSlider = ref<HTMLInputElement>()
const maxSlider = ref<HTMLInputElement>()

const updateMin = (event: Event) => {
    const target = event.target as HTMLInputElement
    let newMin = Number(target.value)
    let newMax = rangeValue.value.max

    // Проверяем пересечение ползунков
    if (!isReversed.value && newMin > newMax) {
        // Если перекидываем левый за правый - меняем их местами
        rangeValue.value = { min: newMax, max: newMin }
    } else {
        rangeValue.value = { ...rangeValue.value, min: newMin }
    }

    // Синхронизируем позиции ползунков
    syncSliders()
}


const updateMax = (event: Event) => {
    const target = event.target as HTMLInputElement
    let newMax = Number(target.value)
    let newMin = rangeValue.value.min

    // Проверяем пересечение ползунков
    if (!isReversed.value && newMax < newMin) {
        // Если перекидываем правый за левый - меняем их местами
        rangeValue.value = { min: newMax, max: newMin }
    } else {
        rangeValue.value = { ...rangeValue.value, max: newMax }
    }

    // Синхронизируем позиции ползунков
    syncSliders()
}
const toggleCheckbox = (opt: string) => {
    const current = value.value || []
    const index = current.indexOf(opt)
    if (index > -1) {
        current.splice(index, 1)
    } else {
        current.push(opt)
    }
    value.value = [...current]
}

const syncSliders = () => {
    if (minSlider.value && maxSlider.value) {
        minSlider.value.value = rangeValue.value.min.toString()
        maxSlider.value.value = rangeValue.value.max.toString()
    }
}
watch(() => rangeValue.value, () => {
    syncSliders()
}, { deep: true })

const formatValue = (val: number): string => {
    // Для часов: 0-24
    if (props.min === 0 && props.max === 24) {
        return `${val}:00`
    }
    return val.toString()
}
const isReversed = computed(() => rangeValue.value.min > rangeValue.value.max)
const rangeStyle = computed(() => {
    const total = (props.max || 100) - (props.min || 0)
    const leftPercent = ((rangeValue.value.min - (props.min || 0)) / total) * 100
    const rightPercent = ((rangeValue.value.max - (props.min || 0)) / total) * 100

    if (!isReversed.value) {
        // Обычный режим: подсвечиваем между ползунками
        return {
            left: `${leftPercent}%`,
            width: `${rightPercent - leftPercent}%`
        }
    } else {
        // Перевернутый режим: подсвечиваем от правого до конца и от начала до левого
        return {
            left: `${rightPercent}%`,
            width: `${leftPercent - rightPercent}%`,
            background: 'linear-gradient(90deg, #4CAF50, #4CAF50)',
            boxShadow: '0 0 0 1px #4CAF50'
        }
    }
})
</script>