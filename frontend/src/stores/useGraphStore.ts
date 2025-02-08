import { defineStore } from "pinia";
import { ref } from "vue";

interface GraphNode {
  id: string;
  name: string;
  x?: number;
  y?: number;
}

interface GraphLink {
  source: string;
  target: string;
}

export const useGraphStore = defineStore("graph", () => {
  const nodes = ref<GraphNode[]>([]);
  const links = ref<GraphLink[]>([]);

  function initializeNodes(newNodes: GraphNode[]) {
    const savedNodes = loadFromLocalStorage();
    nodes.value = newNodes.map(node => ({
      ...node,
      ...(savedNodes.find(n => n.id === node.id) || {})
    }));
  }

  function initializeLinks(newLinks: GraphLink[]) {
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
    return savedNodes ? JSON.parse(savedNodes) : [];
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
  };
});