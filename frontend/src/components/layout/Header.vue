<script setup lang="ts">
import ThemeToggle from '../ThemeToggle.vue'
import Button from '../ui/Button.vue'
import { useGraphStore } from '../../stores/useGraphStore'

const emit = defineEmits(['openAddNode', 'toggleJsonViewer'])
const store = useGraphStore()

const handleAddNode = () => {
  emit('openAddNode')
}

const handleShowJson = () => {
  const graphData = {
    nodes: store.nodes,
    links: store.links
  }
  console.log(graphData, 'graphData')
  emit('toggleJsonViewer', graphData)
}
</script>

<template>
  <header class="flex items-center justify-between p-6 bg-gradient-to-r from-blue-500 to-purple-600 dark:from-gray-700 dark:to-gray-900 shadow-lg">
    <div class="flex items-center gap-6">
      <h1 class="text-3xl font-extrabold text-white dark:text-gray-100">Course Manager</h1>
      <Button variant="primary" @click="handleAddNode">Add Node</Button>
      <Button variant="secondary" @click="handleShowJson">Show Graph as JSON</Button>
    </div>
    <div class="flex items-center gap-6">
      <ThemeToggle />
    </div>
  </header>
</template>