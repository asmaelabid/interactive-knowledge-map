<template>
  <div ref="graph">
    <h1>Graph</h1>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import * as d3 from 'd3'
import axios from 'axios'

const graph = ref(null)

onMounted(async () => {
  const response = await axios.get('http://localhost:8000/api/v1/courses')
  const data = response.data

  const nodes = data.map(d => ({ id: d.id, name: d.name }))
  const links = data
    .filter(d => d.parent_id !== null)
    .map(d => ({ source: d.parent_id, target: d.id }))

  const width = 800
  const height = 600

  const svg = d3.select(graph.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)

  const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id).distance(100))
    .force('charge', d3.forceManyBody().strength(-300))
    .force('center', d3.forceCenter(width / 2, height / 2))

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