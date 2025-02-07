<template>
  <div v-if="node" class="node-editor absolute top-2 right-2 bg-white p-4 border border-gray-300 rounded-lg shadow-lg">
    <h2 class="text-lg font-bold mb-2">Edit Node</h2>
    <label class="block mb-2">
      Name:
      <input v-model="node.name" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50" />
    </label>
    <div class="flex space-x-2">
      <button @click="updateNode" class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600" :disabled="loading">Update</button>
      <button @click="removeNode" class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600" :disabled="loading">Remove</button>
      <button @click="closeEditor" class="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600" :disabled="loading">Close</button>
    </div>
    <div v-if="loading" class="mt-2 text-center text-gray-500">Loading...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toast-notification'

const props = defineProps<{ node: any }>()
const emit = defineEmits(['close'])

const node = ref({ ...props.node })
const loading = ref(false)
const toastMessage = ref('')
const toast = useToast()

watch(() => props.node, (newNode) => {
  node.value = { ...newNode }
})

async function updateNode() {
  loading.value = true
  try {
    await axios.put(`http://localhost:8000/api/v1/courses/${node.value.id}`, {
      name: node.value.name,
      parent_id: node.value.parent_id
    })
    toastMessage.value = 'Node updated successfully'
    toast.success(toastMessage.value)
    emit('close')
  } catch (error) {
    console.error('Failed to update node:', error)
    toastMessage.value = 'Failed to update node'
    toast.error(toastMessage.value)
  } finally {
    loading.value = false
  }
}

async function removeNode() {
  loading.value = true
  try {
    await axios.delete(`http://localhost:8000/api/v1/courses/${node.value.id}`)
    toastMessage.value = 'Node removed successfully'
    toast.success(toastMessage.value)
    emit('close')
  } catch (error) {
    console.error('Failed to remove node:', error)
    toastMessage.value = 'Failed to remove node'
    toast.error(toastMessage.value)
  } finally {
    loading.value = false
  }
}

function closeEditor() {
  emit('close')
}
</script>