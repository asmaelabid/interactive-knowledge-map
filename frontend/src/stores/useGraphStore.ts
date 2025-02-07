import { defineStore } from "pinia";
import { ref } from "vue";

export const useGraphStore = defineStore("graph", () => {
  const nodes = ref([]);

  function initializeNodes(newNodes) {
    // Initialize store with nodes from API
    nodes.value = newNodes.map(node => ({
      ...node,
      x: node.x || window.innerWidth / 2,
      y: node.y || window.innerHeight / 2,
      fx: node.fx || null,
      fy: node.fy || null,
    }));
    saveToLocalStorage();
  }

  function updateNodePosition(id, x, y) {
    const node = nodes.value.find((node) => node.id === id);
    if (node) {
      node.x = x;
      node.y = y;
      node.fx = x;
      node.fy = y;
      saveToLocalStorage();
    }
  }

  function saveToLocalStorage() {
    localStorage.setItem("graphNodes", JSON.stringify(nodes.value));
  }

  function loadFromLocalStorage() {
    const storedNodes = localStorage.getItem("graphNodes");
    if (storedNodes) {
      nodes.value = JSON.parse(storedNodes);
    }
  }

  return { 
    nodes, 
    initializeNodes,
    updateNodePosition, 
    loadFromLocalStorage 
  };
});