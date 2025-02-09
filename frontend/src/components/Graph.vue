<template>
  <div class="relative h-screen w-full bg-gray-50 dark:bg-gray-900">
    <div class="absolute inset-0 flex flex-col" :class="{ 'blur-sm': showJsonViewer }">
      <div class="flex-1 w-full rounded-lg shadow-inner bg-white dark:bg-gray-800" ref="graphContainer"></div>
      <NodeEditor v-if="selectedNode" :node="selectedNode" @close="selectedNode = null" />
    </div>
    <div v-if="showJsonViewer" class="fixed inset-0 z-50">
      <GraphJsonViewer :json="graphJson" @close="$emit('closeJsonViewer')" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import * as d3 from 'd3'
import axios from 'axios'
import NodeEditor from './NodeEditor.vue'
import GraphJsonViewer from './GraphJsonViewer.vue'
import { useGraphStore } from '../stores/useGraphStore'
import { useCourseStore } from '../stores/useCourseStore'

const props = withDefaults(defineProps<{
  showJsonViewer?: boolean
  graphJson?: string
}>(), {
  showJsonViewer: false,
  graphJson: ''
})

const selectedNode = ref(null)
const graphContainer = ref(null)
const courseStore = useCourseStore()
const graphStore = useGraphStore()
const svg = ref(null)
const simulation = ref(null)
const emit = defineEmits(['closeJsonViewer'])

function clearGraph() {
  if (!svg.value) return
  svg.value.select('.nodes').selectAll('*').remove()
  svg.value.select('.links').selectAll('*').remove()

  if (simulation.value) {
    simulation.value.stop()
    simulation.value = null
  }
}

function reinitializeSimulation() {
  if (!graphContainer.value) return

  const width = graphContainer.value.clientWidth
  const height = graphContainer.value.clientHeight

  d3.select(graphContainer.value).selectAll('svg').remove()

  svg.value = d3.select(graphContainer.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', `0 0 ${width} ${height}`)
    .attr('preserveAspectRatio', 'xMidYMid meet')
    .attr('class', 'rounded-lg')

  svg.value.append('g').attr('class', 'links')
  svg.value.append('g').attr('class', 'nodes')

  clearGraph()
  simulation.value = d3.forceSimulation(graphStore.nodes)
    .force('link', d3.forceLink(graphStore.links).id((d: any) => d.id).distance(200))
    .force('charge', d3.forceManyBody().strength(-100))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('x', d3.forceX(width / 2).strength(0.01))
    .force('y', d3.forceY(height / 2).strength(0.01))

  updateGraph()
}

function updateGraph() {
  if (!svg.value || !simulation.value) return

  const node = svg.value.select('.nodes').selectAll('g')
    .data(graphStore.nodes, (d: any) => d.id)

  node.exit().remove()

  node.select('text')
    .text(d => d.name)

  const nodeEnter = node.enter()
    .append('g')
    .attr('class', 'cursor-pointer')
    .call(d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended))

  nodeEnter.append('circle')
    .attr('r', 12)
    .attr('class', 'transition-all duration-200 fill-blue-500 stroke-blue-700 dark:fill-indigo-500 dark:stroke-indigo-700')
    .attr('stroke-width', 2)

  nodeEnter.append('text')
    .attr('x', 16)
    .attr('y', 4)
    .attr('class', 'text-sm font-medium fill-gray-700 dark:fill-gray-200')
    .text(d => d.name)

  nodeEnter.selectAll('circle')
    .on('mousedown', function (event, d) {
      d3.selectAll('circle')
        .attr('class', 'transition-all duration-200 fill-blue-500 stroke-blue-700 dark:fill-indigo-500 dark:stroke-indigo-700')
      d3.selectAll('line')
        .attr('class', 'transition-all duration-50 ease-in-out stroke-gray-400 dark:stroke-gray-600')
        .attr('stroke-width', '2')

      const connectedLinks = graphStore.links.filter(l =>
        l.source.id === d.id || l.target.id === d.id
      )

      const connectedNodeIds = new Set()
      connectedLinks.forEach(l => {
        connectedNodeIds.add(l.source.id)
        connectedNodeIds.add(l.target.id)
      })

      d3.selectAll('line')
        .filter(l => l.source.id === d.id || l.target.id === d.id)
        .attr('class', 'transition-all duration-50 ease-in-out stroke-purple-400 dark:stroke-purple-600')
        .attr('stroke-width', '3')

      d3.selectAll('circle')
        .filter(n => connectedNodeIds.has(n.id) && n.id !== d.id)
        .attr('class', 'transition-all duration-200 fill-purple-400 stroke-purple-600 dark:fill-purple-500 dark:stroke-purple-700')

      d3.select(this)
        .attr('class', 'transition-all duration-200 fill-purple-400 stroke-purple-600 dark:fill-purple-500 dark:stroke-purple-700')
    })
    .on('mouseover', function (event, d) {
      if (!event.buttons) {
        d3.select(this)
          .transition()
          .duration(50)
          .attr('r', 15)
          .attr('class', 'transition-all duration-200 fill-blue-300 stroke-blue-500 dark:fill-indigo-400 dark:stroke-indigo-600')
      }
    })
    .on('mouseout', function (event, d) {
      if (!event.buttons) {
        d3.select(this)
          .transition()
          .duration(50)
          .attr('r', 12)
          .attr('class', 'transition-all duration-200 fill-blue-500 stroke-blue-700 dark:fill-indigo-500 dark:stroke-indigo-700')
      }
    })
    .on('dblclick', function (event, d) {
      const updatedNode = graphStore.nodes.find(n => n.id === d.id)
      const courseData = courseStore.courses.find(c => c.id === d.id)
      selectedNode.value = updatedNode ? {
        ...updatedNode,
        parent_name: courseData?.parent_name || null
      } : null
    })

  const link = svg.value.select('.links').selectAll('line')
    .data(graphStore.links, (d: any) => `${d.source.id}-${d.target.id}`)

  simulation.value
    .nodes(graphStore.nodes)
    .force('link', d3.forceLink(graphStore.links).id((d: any) => d.id).distance(200))

  link.exit().remove()

  const linkEnter = link.enter()
    .append('line')
    .attr('class', 'transition-all duration-50 ease-in-out stroke-gray-400 dark:stroke-gray-600')
    .attr('stroke-width', 2)

  const allNodes = node.merge(nodeEnter)
  const allLinks = link.merge(linkEnter)

  simulation.value.nodes(graphStore.nodes)
  simulation.value.force('link').links(graphStore.links)

  simulation.value.on('tick', () => {
    allLinks
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)

    allNodes
      .attr('transform', d => `translate(${d.x},${d.y})`)
  })

  simulation.value.alpha(1).restart()
}
watch(
  [
    () => graphStore.nodes.length,
    () => graphStore.links.length,
    () => [...graphStore.nodes],
  ],
  ([newNodesLength, newLinksLength], [oldNodesLength, oldLinksLength]) => {
    if (newNodesLength !== oldNodesLength || newLinksLength !== oldLinksLength) {
      reinitializeSimulation()
    } else {
      updateGraph()
    }
  },
  { deep: true }
)
function dragstarted(event, d) {
  if (!event.active) simulation.value.alphaTarget(0.3).restart()
  d.fx = d.x
  d.fy = d.y
}

function dragged(event, d) {
  const padding = 20
  const width = graphContainer.value?.clientWidth || 800
  const height = graphContainer.value?.clientHeight || 600

  d.fx = Math.max(padding, Math.min(width - padding, event.x))
  d.fy = Math.max(padding, Math.min(height - padding, event.y))
}

function dragended(event, d) {
  const width = graphContainer.value?.clientWidth || 800
  const height = graphContainer.value?.clientHeight || 600

  if (!event.active) simulation.value?.alphaTarget(0)
  const x = Math.max(0, Math.min(width, event.x))
  const y = Math.max(0, Math.min(height, event.y))
  d.x = x
  d.y = y
  d.fx = null
  d.fy = null
  d3.selectAll('circle')
    .transition()
    .duration(50)
    .attr('r', 12)
    .attr('class', 'transition-all duration-200 fill-blue-500 stroke-blue-700 dark:fill-indigo-500 dark:stroke-indigo-700')

  // Reset all links
  d3.selectAll('line')
    .transition()
    .duration(50)
    .attr('class', 'transition-all duration-50 ease-in-out stroke-gray-400 dark:stroke-gray-600')
    .attr('stroke-width', '2')
  graphStore.updateNodePosition(d.id, x, y)
  simulation.value?.alpha(0.1).restart()

}
onMounted(async () => {
  graphStore.loadFromLocalStorage()
  await courseStore.fetchCourses()

  const nodes = courseStore.courses.map(d => {
    const storedNode = graphStore.nodes.find(n => n.id === d.id)
    if (storedNode) {
      return {
        id: d.id,
        name: d.name,
        x: storedNode.x,
        y: storedNode.y,
      }
    }
    return { id: d.id, name: d.name }
  })

  const links = courseStore.courses
    .filter(d => d.parent_id !== null)
    .map(d => ({ source: d.parent_id, target: d.id }))

  graphStore.initializeNodes(nodes)
  graphStore.initializeLinks(links)

  const width = graphContainer.value?.clientWidth || 800
  const height = graphContainer.value?.clientHeight || 600

  const svg = d3.select(graphContainer.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', `0 0 ${width} ${height}`)
    .attr('preserveAspectRatio', 'xMidYMid meet')
    .attr('class', 'rounded-lg')

  const simulation = d3.forceSimulation(graphStore.nodes)
    .force('link', d3.forceLink(links).id(d => d.id).distance(200))
    .force('charge', d3.forceManyBody().strength(-100))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('x', d3.forceX(width / 2).strength(0.01))
    .force('y', d3.forceY(height / 2).strength(0.01))

  simulation.nodes(graphStore.nodes)
  const link = svg.append('g')
    .attr('class', 'links')
    .selectAll('line')
    .data(graphStore.links)
    .enter()
    .append('line')
    .attr('class', 'transition-all duration-50 ease-in-out stroke-gray-400 dark:stroke-gray-600')
    .attr('stroke-width', 2)

  const node = svg.append('g')
    .attr('class', 'nodes')
    .selectAll('g')
    .data(graphStore.nodes)
    .enter()
    .append('g')
    .attr('class', 'cursor-pointer')
    .call(d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended))

  node.append('circle')
    .attr('r', 12)
    .attr('class', 'transition-all duration-200 fill-blue-500 stroke-blue-700 dark:fill-indigo-500 dark:stroke-indigo-700')
    .attr('stroke-width', 2)

  node.append('text')
    .attr('x', 16)
    .attr('y', 4)
    .attr('class', 'text-sm font-medium fill-gray-700 dark:fill-gray-200')
    .text(d => d.name)

  node.selectAll('circle')
    .on('mouseover', function (event, d) {
      if(event.buttons) return
      d3.select(this)
        .transition()
        .duration(50)
        .attr('r', 15)
        .attr('class', 'transition-all duration-200 fill-blue-300 stroke-blue-500 dark:fill-indigo-400 dark:stroke-indigo-600')
    })
    .on('mouseout', function (event) {
      if(event.buttons) return
      d3.select(this)
        .transition()
        .duration(50)
        .attr('r', 12)
        .attr('class', 'transition-all duration-200 fill-blue-500 stroke-blue-700 dark:fill-indigo-500 dark:stroke-indigo-700')
    })
    .on('dblclick', function (event, d) {
      const updatedNode = graphStore.nodes.find(n => n.id === d.id)
      const courseData = courseStore.courses.find(c => c.id === d.id)
      selectedNode.value = updatedNode ? {
        ...updatedNode,
        parent_name: courseData?.parent_name || null
      } : null

    })

  simulation.on('tick', () => {
    nodes.forEach(node => {
      node.x = Math.max(20, Math.min(width - 20, node.x))
      node.y = Math.max(20, Math.min(height - 20, node.y))
    })
    link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)

    node
      .attr('transform', d => `translate(${d.x},${d.y})`)
  })
  reinitializeSimulation()

})
</script>