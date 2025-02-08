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
import { onMounted, ref } from 'vue'
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

const emit = defineEmits(['closeJsonViewer'])

onMounted(async () => {
  graphStore.loadFromLocalStorage()
  await courseStore.fetchCourses()
  // const data = response.data

  const nodes = courseStore.courses.map(d => {
    const storedNode = graphStore.nodes.find(n => n.id === d.id)
    if (storedNode) {
      return {
        id: d.id,
        name: d.name,
        x: storedNode.x,
        y: storedNode.y,
        // fx: storedNode.x,
        // fy: storedNode.y
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
    .attr('class', 'transition-all duration-50 ease-in-out')
    .attr('stroke-width', 2)
    .attr('stroke', '#999')

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
    .attr('class', 'transition-all duration-200')
    .attr('fill', 'rgb(59 130 246)')
    .attr('stroke', 'rgb(37 99 235)')
    .attr('stroke-width', 2)

  node.append('text')
    .attr('x', 16)
    .attr('y', 4)
    .attr('class', 'text-sm font-medium fill-gray-700 dark:fill-gray-200')
    .text(d => d.name)

  node.selectAll('circle')
    .on('mouseover', function () {
      d3.select(this)
        .transition()
        .duration(50)
        .attr('r', 15)
        .attr('fill', 'orange')
    })
    .on('mouseout', function () {
      d3.select(this)
        .transition()
        .duration(50)
        .attr('r', 12)
        .attr('fill', 'var(--node-gradient-from)')
    })
    .on('mousedown', function (event, d) {
      link.each(function (l) {
        if (l.source.id === d.id || l.target.id === d.id) {
          d3.select(this)
            .transition()
            .duration(50)
            .attr('stroke', '#ffa07a')
          node.selectAll('circle').each(function (n) {
            if (l.source.id === n.id || l.target.id === n.id) {
              if (n.id !== d.id) {
                d3.select(this)
                  .transition()
                  .duration(50)
                  .attr('fill', '#ffa07a')
              }
            }
          })
        }
      })
    })
    .on('mouseup', function (event, d) {
      node.selectAll('circle')
        .transition()
        .duration(50)
        .attr('fill', 'var(--node-gradient-from)')
      link
        .transition()
        .duration(50)
        .attr('stroke', '#999')
    })
    .on('dblclick', function (event, d) {
      console.log('Double clicked on:', d)
      selectedNode.value = d
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

  function dragstarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart()
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
    if (!event.active) simulation.alphaTarget(0)
    const x = Math.max(0, Math.min(width, event.x))
    const y = Math.max(0, Math.min(height, event.y))
    d.x = x
    d.y = y
    d.fx = null
    d.fy = null
    graphStore.updateNodePosition(d.id, x, y)
    simulation.alpha(0.1).restart()

    node.selectAll('circle')
      .transition()
      .duration(50)
      .attr('fill', 'var(--node-gradient-from)')
    link
      .transition()
      .duration(50)
      .attr('stroke', '#999')
  }
})
</script>

<style scoped>
:root {
  --node-gradient-from: #60a5fa;
  --node-gradient-to: #3b82f6;
  --node-stroke: #2563eb;
  --link-color: #94a3b8;
  --text-color: #1f2937;
}

:root.dark {
  --node-gradient-from: #818cf8;
  --node-gradient-to: #6366f1;
  --node-stroke: #4f46e5;
  --link-color: #64748b;
  --text-color: #f1f5f9;
}
svg {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 0.5rem;
  overflow: visible;
}

.links line {
  stroke: var(--link-color);
  stroke-opacity: 0.6;
  stroke-width: 2px;
  stroke-linecap: round;
}

.nodes circle.node-circle {
  fill: var(--node-gradient-from);
  stroke: var(--node-stroke);
  stroke-width: 2px;
  filter: drop-shadow(0 4px 3px rgb(0 0 0 / 0.07));
}

.nodes text.node-text {
  fill: var(--text-color);
  font-size: 0.875rem;
  font-weight: 500;
  paint-order: stroke;
  stroke: #ffffff;
  stroke-width: 3px;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* Hover effects */
.nodes g:hover circle.node-circle {
  filter: drop-shadow(0 8px 6px rgb(0 0 0 / 0.1));
}

.nodes g:hover~line {
  stroke-opacity: 0.8;
  stroke-width: 3px;
}
</style>