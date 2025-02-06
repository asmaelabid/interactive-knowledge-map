<template>
  <div ref="graph" class="w-full h-full flex flex-col items-center justify-center">
    <h1 class="text-2xl font-bold mb-4">Graph</h1>
    <div class="w-full h-full" ref="graphContainer"></div>
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

  const width = graphContainer.value.clientWidth || 800
  const height = graphContainer.value.clientHeight || 600

  const svg = d3.select(graphContainer.value)
    .append('svg')
    .attr('width', '100%')
    .attr('height', '100%')
    .attr('viewBox', `0 0 ${width} ${height}`)
    .attr('preserveAspectRatio', 'xMidYMid meet')

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
    .attr('stroke-width', 2)
    .attr('stroke', '#999')

  const node = svg.append('g')
    .attr('class', 'nodes')
    .selectAll('g')
    .data(nodes)
    .enter()
    .append('g')
    .call(d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended))

  node.append('circle')
    .attr('r', 10)
    .attr('fill', 'blue')

  node.append('text')
    .attr('x', 12)
    .attr('y', 3)
    .text(d => d.name)

  simulation.on('tick', () => {
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
    d.fx = event.x
    d.fy = event.y
  }

  function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0)
    d.fx = null
    d.fy = null
  }
})
</script>

<style scoped>
svg {
  border: 1px solid black;
  width: 100%;
  height: 100%;
}

.links line {
  stroke: #999;
  stroke-opacity: 0.6;
}

.nodes circle {
  stroke: #fff;
  stroke-width: 1.5px;
}
</style>