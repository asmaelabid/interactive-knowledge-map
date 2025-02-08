<script setup lang="ts">
import { ref } from 'vue'
import Header from './components/layout/Header.vue'
import Footer from './components/layout/Footer.vue'
import AddNodeDialog from './components/AddNodeDialog.vue'
import { useGraphStore } from './stores/useGraphStore'

const showAddNodeDialog = ref(false)
const showJsonViewer = ref(false)
const store = useGraphStore()
const graphJson = ref('')

const handleToggleJsonViewer = (graphData?: { nodes: any[], links: any[] }) => {
  showJsonViewer.value = !showJsonViewer.value
  if (showJsonViewer.value && graphData) {
    graphJson.value = JSON.stringify(graphData, null, 2)
  }
}

const handleOpenAddNode = () => {
  showAddNodeDialog.value = true
}

const handleCloseAddNode = () => {
  showAddNodeDialog.value = false
}

</script>

<template>
  <div class="min-h-screen w-full flex flex-col bg-white dark:bg-gray-800">
    <Header 
      @open-add-node="handleOpenAddNode" 
      @toggle-json-viewer="handleToggleJsonViewer" 
    />
    <main class="flex-1">
      <router-view
        :show-json-viewer="showJsonViewer"
        :graph-json="graphJson"
        @close-json-viewer="showJsonViewer = false"
      />
    </main>
    <Footer />
    <AddNodeDialog v-if="showAddNodeDialog" @close="handleCloseAddNode" />
  </div>
</template>