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
  <header class="flex items-center justify-between p-4 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
    <div class="flex items-center gap-4">
      <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-100">Course Manager</h1>
      <Button variant="primary" @click="handleAddNode">Add Node</Button>
      <Button variant="secondary" @click="handleShowJson">Show Graph as JSON</Button>
    </div>
    <div class="flex items-center gap-4">
      <ThemeToggle />
      <Button variant="danger">Logout</Button>
    </div>
  </header>
</template>