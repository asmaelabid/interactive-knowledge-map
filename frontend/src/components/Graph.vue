<template>
    <div ref="graph">
      <h1>Graph</h1>
    </div>
  </template>
  
  <script setup lang="ts">
  import { onMounted, ref } from 'vue'
  import * as d3 from 'd3'

  const graph = ref(null)
  
  onMounted(() => {
    const svg = d3.select(graph.value)
      .append('svg')
      .attr('width', 500)
      .attr('height', 500)
  
    svg.append('circle')
      .attr('cx', 250)
      .attr('cy', 250)
      .attr('r', 40)
      .style('fill', 'blue')
  })
  </script>
  
  <style scoped>
  svg {
    border: 1px solid black;
  }
  </style>