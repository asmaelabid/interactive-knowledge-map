<script setup lang="ts">
</script>

<template>
  <div>
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/graph">Graph</router-link>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
nav {
  margin-bottom: 1em;
}
nav a {
  margin-right: 1em;
}
</style>