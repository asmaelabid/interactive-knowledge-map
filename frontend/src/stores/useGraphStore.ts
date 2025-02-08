import { defineStore } from "pinia";
import { ref } from "vue";

export const useGraphStore = defineStore("graph", () => {
  const nodes = ref<any[]>([]);
  const links = ref<any[]>([]);

  function initializeNodes(newNodes: any[]) {
    nodes.value = newNodes;
  }

  function initializeLinks(newLinks: any[]) {
    links.value = newLinks;
  }

  function updateNodePosition(id: string, x: number, y: number) {
    const node = nodes.value.find((n) => n.id === id);
    if (node) {
      node.x = x;
      node.y = y;
    }
    saveToLocalStorage();
  }

  function loadFromLocalStorage() {
    const savedNodes = localStorage.getItem("graph-nodes");
    if (savedNodes) {
      nodes.value = JSON.parse(savedNodes);
    }
  }

  function saveToLocalStorage() {
    localStorage.setItem("graph-nodes", JSON.stringify(nodes.value));
  }

  return {
    nodes,
    links,
    initializeNodes,
    initializeLinks,
    updateNodePosition,
    loadFromLocalStorage,
    saveToLocalStorage,
  };
});
