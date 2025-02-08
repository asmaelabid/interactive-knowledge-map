<template>
    <div class="fixed inset-0 flex items-center justify-center bg-transparent" @click.self="$emit('close')">
        <div class="p-4 bg-white dark:bg-gray-800 rounded-lg shadow-xl relative">
            <button @click="$emit('close')"
                class="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full">X</button>
            <pre class="text-sm text-gray-800 dark:text-gray-100">{{ json }}</pre>
        </div>
    </div>
</template>
<script setup lang="ts">
import { defineProps } from 'vue'

const props = defineProps<{ json: string }>()
</script>

<style scoped>
pre {
    white-space: pre-wrap;
    word-wrap: break-word;
}
</style>