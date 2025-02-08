<template>
  <div v-if="node"
    class="absolute top-4 right-4 bg-white dark:bg-gray-800 p-6 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg"
    ref="editorRef">
    <h2 class="text-lg font-bold mb-4 text-gray-900 dark:text-white">Edit Node</h2>
    <label class="block mb-4">
      <span class="text-gray-700 dark:text-gray-200">Name:</span>
      <input v-model="node.name"
        class="mt-1 block w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent" />
    </label>
    <label class="block mb-4">
      <span class="text-gray-700 dark:text-gray-200">Parent Name:</span>
      <input v-model="node.parent_name"
        class="mt-1 block w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent" />
    </label>
    <div class="flex space-x-3">
      <Button variant="primary" :disabled="loading" @click="updateNode">
        Update
      </Button>
      <Button variant="danger" :disabled="loading" @click="removeNode">
        Remove
      </Button>
      <Button variant="secondary" :disabled="loading" @click="closeEditor">
        Close
      </Button>
    </div>
    <div v-if="loading" class="mt-2 text-center text-gray-500 dark:text-gray-400">Loading...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toast-notification'
import Button from './ui/Button.vue';
import { useGraphStore } from '../stores/useGraphStore'
import { useCourseStore } from '../stores/useCourseStore'


const props = defineProps<{ node: any }>()
const emit = defineEmits(['close'])
const graphStore = useGraphStore()
const courseStore = useCourseStore()
const node = ref({ ...props.node })
const loading = ref(false)
const toastMessage = ref('')
const toast = useToast()
const editorRef = ref<HTMLElement | null>(null)

watch(() => props.node, (newNode) => {
  node.value = { ...newNode }
})

async function updateNode() {
  loading.value = true
  try {
    await axios.put(`http://localhost:8000/api/v1/courses/${node.value.id}`, {
      name: node.value.name,
      parent_name: node.value.parent_name
    })
    graphStore.updateNode(node.value.id, { name: node.value.name })
    await courseStore.fetchCourses()
    const nodes = courseStore.courses.map(d => {
      const storedNode = graphStore.nodes.find(n => n.id === d.id)
      return {
        id: d.id,
        name: d.name,
        x: storedNode?.x,
        y: storedNode?.y
      }
    })

    const links = courseStore.courses
      .filter(d => d.parent_id !== null)
      .map(d => ({ source: d.parent_id, target: d.id }))

    graphStore.initializeNodes(nodes)
    graphStore.initializeLinks(links)

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
    graphStore.removeNode(node.value.id)
    await courseStore.fetchCourses()

    const nodes = courseStore.courses.map(d => {
      const storedNode = graphStore.nodes.find(n => n.id === d.id)
      return {
        id: d.id,
        name: d.name,
        x: storedNode?.x,
        y: storedNode?.y
      }
    })

    const links = courseStore.courses
      .filter(d => d.parent_id !== null)
      .map(d => ({ source: d.parent_id, target: d.id }))

    graphStore.initializeNodes(nodes)
    graphStore.initializeLinks(links)

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
const handleClickOutside = (event: MouseEvent) => {
  if (editorRef.value && !editorRef.value.contains(event.target as Node)) {
    emit('close')
  }
}

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside)
})

</script>