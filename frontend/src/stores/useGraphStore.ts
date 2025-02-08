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
    nodes.value = newNodes.map((node) => ({
      ...node,
      ...(savedNodes.find((n) => n.id === node.id) || {}),
    }));
    saveToLocalStorage();
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
  function updateNode(nodeId: string, newData: Partial<GraphNode>) {
    const nodeIndex = nodes.value.findIndex((n) => n.id === nodeId);
    if (nodeIndex !== -1) {
      nodes.value[nodeIndex] = { ...nodes.value[nodeIndex], ...newData };
      saveToLocalStorage();
    }
  }

  function removeNode(nodeId: string) {
    nodes.value = nodes.value.filter((n) => n.id !== nodeId);
    links.value = links.value.filter(
      (l) => l.source !== nodeId && l.target !== nodeId
    );
    saveToLocalStorage();
  }

  return {
    nodes,
    links,
    initializeNodes,
    initializeLinks,
    updateNodePosition,
    loadFromLocalStorage,
    updateNode,
    removeNode,
  };
});
