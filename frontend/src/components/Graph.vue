<template>
  <div class="h-full w-full flex flex-col">
    <h1 class="p-4 text-2xl font-bold text-gray-800 dark:text-gray-100">Graph</h1>
    <div class="flex-1 w-full rounded-lg shadow-inner bg-white dark:bg-gray-800" ref="graphContainer"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import * as d3 from 'd3'
import axios from 'axios'

const graphContainer = ref(null)

onMounted(async () => {
  const response = await axios.get('http://localhost:8000/api/v1/courses')
  const data = response.data

  const nodes = data.map(d => ({ id: d.id, name: d.name }))
  const links = data
    .filter(d => d.parent_id !== null)
    .map(d => ({ source: d.parent_id, target: d.id }))

  const width = graphContainer.value?.clientWidth || 800
  const height = graphContainer.value?.clientHeight || 600

  const svg = d3.select(graphContainer.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', `0 0 ${width} ${height}`)
    .attr('preserveAspectRatio', 'xMidYMid meet')
    .attr('class', 'rounded-lg')

  const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id).distance(200))
    .force('charge', d3.forceManyBody().strength(-100))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('x', d3.forceX(width / 2).strength(0.05))
    .force('y', d3.forceY(height / 2).strength(0.05))

  const link = svg.append('g')
    .attr('class', 'links')
    .selectAll('line')
    .data(links)
    .enter()
    .append('line')
    .attr('class', 'transition-all duration-50 ease-in-out')
    .attr('stroke-width', 2)
    .attr('stroke', '#999')

  const node = svg.append('g')
    .attr('class', 'nodes')
    .selectAll('g')
    .data(nodes)
    .enter()
    .append('g')
    .attr('class', 'cursor-pointer transition-all duration-50 ease-in-out')
    .call(d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended))

  node.append('circle')
    .attr('r', 12)
    .attr('class', 'node-circle')

  node.append('text')
    .attr('x', 16)
    .attr('y', 4)
    .attr('class', 'node-text')
    .text(d => d.name)

  node
    .on('mouseover', function () {
      d3.select(this).select('circle')
        .transition()
        .duration(50)
        .attr('r', 15)
    })
    .on('mouseout', function () {
      d3.select(this).select('circle')
        .transition()
        .duration(50)
        .attr('r', 12)
    })

  simulation.on('tick', () => {
    link
      .transition()
      .duration(50)
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)

    node
      .transition()
      .duration(50)
      .attr('transform', d => `translate(${d.x},${d.y})`)
  })

  function dragstarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart()
    d.fx = d.x
    d.fy = d.y
  }

  function dragged(event, d) {
  const width = graphContainer.value?.clientWidth || 800
  const height = graphContainer.value?.clientHeight || 600

  d.fx = Math.max(0, Math.min(width, event.x))
  d.fy = Math.max(0, Math.min(height, event.y))
}
  function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0)
    d.fx = null
    d.fy = null
  }
})
</script>

<style scoped>
/* Base theme variables */
:root {
  --node-gradient-from: #60a5fa;
  --node-gradient-to: #3b82f6;
  --node-stroke: #2563eb;
  --link-color: #94a3b8;
  --text-color: #1f2937;
}

/* Dark mode variables */
:root.dark {
  --node-gradient-from: #818cf8;
  --node-gradient-to: #6366f1;
  --node-stroke: #4f46e5;
  --link-color: #64748b;
  --text-color: #f1f5f9;
}

/* SVG container */
svg {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 0.5rem;
  overflow: visible;
}

/* Links styling */
.links line {
  stroke: var(--link-color);
  stroke-opacity: 0.6;
  stroke-width: 2px;
  stroke-linecap: round;
}

/* Nodes styling */
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

.nodes g:hover ~ line {
  stroke-opacity: 0.8;
  stroke-width: 3px;
}
</style>