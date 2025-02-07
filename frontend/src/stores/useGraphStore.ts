import { defineStore } from "pinia";
import { ref } from "vue";

export const useGraphStore = defineStore("graph", () => {
  const nodes = ref([]);

  function initializeNodes(newNodes) {
    const storedNodes = JSON.parse(localStorage.getItem("graphNodes") || "[]");

    nodes.value = newNodes.map((node) => {
      const existingNode = storedNodes.find((n) => n.id === node.id);
      if (existingNode && existingNode.wasPositioned) {
        return {
          ...node,
          x: existingNode.x,
          y: existingNode.y,
          fx: existingNode.x,
          fy: existingNode.y,
          wasPositioned: true
        };
      }
      return {
        ...node,
        wasPositioned: false
      };
    });

    if (!storedNodes.length) {
      setTimeout(() => {
        saveToLocalStorage();
      }, 2000);
    }
  }

  function updateNodePosition(id, x, y) {
    const node = nodes.value.find((node) => node.id === id);
    if (node) {
      node.x = x;
      node.y = y;
      node.fx = x;
      node.fy = y;
      node.wasPositioned = true;
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
    loadFromLocalStorage,
  };
});
