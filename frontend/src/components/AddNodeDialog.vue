<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toast-notification'
import Button from './ui/Button.vue'
import { useCourseStore } from '../stores/useCourseStore'

const emit = defineEmits(['close'])
const toast = useToast()
const loading = ref(false)
const nodeName = ref('')
const courseStore = useCourseStore()

async function addNode() {
  loading.value = true
  try {
    await courseStore.addCourse(nodeName.value)
    toast.success('Node added successfully')
    emit('close')
  } catch (error) {
    console.error('Failed to add node:', error)
    toast.error('Failed to add node')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center bg-gray-500/50 dark:bg-gray-900/50 backdrop-blur-sm">
    <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-xl relative max-w-md w-full">
      <h2 class="text-lg font-bold mb-4 text-gray-900 dark:text-white">Add New Node</h2>
      <label class="block mb-4">
        <span class="text-gray-700 dark:text-gray-200">Name:</span>
        <input v-model="nodeName"
          class="mt-1 block w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent" />
      </label>
      <div class="flex space-x-3">
        <Button variant="primary" :disabled="loading" @click="addNode">
          Add
        </Button>
        <Button variant="secondary" :disabled="loading" @click="$emit('close')">
          Cancel
        </Button>
      </div>
      <div v-if="loading" class="mt-2 text-center text-gray-500 dark:text-gray-400">Loading...</div>
    </div>
  </div>
</template>