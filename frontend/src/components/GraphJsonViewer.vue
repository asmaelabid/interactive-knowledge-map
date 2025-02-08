<template>
    <div class="fixed inset-0 flex items-center justify-center bg-gray-500/50 dark:bg-gray-900/50 backdrop-blur-sm"
        @click.self="$emit('close')">
        <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-xl relative max-w-2xl max-h-[80vh] overflow-auto">
            <button @click="$emit('close')"
                class="absolute top-2 right-2 p-2 bg-red-500 hover:bg-red-600 text-white rounded-full transition-colors">
                X
            </button>
            <pre class="text-sm text-gray-800 dark:text-gray-100 whitespace-pre-wrap break-words">{{ json }}</pre>
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

const props = defineProps<{ json: string }>()
</script>