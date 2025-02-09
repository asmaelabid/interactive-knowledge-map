import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";
import { useGraphStore } from "./useGraphStore";
interface Course {
  id: string;
  name: string;
  parent_id: string | null;
  parent_name: string | null;
}

export const useCourseStore = defineStore("courses", () => {
  const courses = ref<Course[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const graphStore = useGraphStore();
  const API_URL = import.meta.env.VITE_BACKEND_URL;

  async function fetchCourses() {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/courses`);
      const fetchedCourses = response.data;
      const deletedNodeIds = graphStore.nodes
        .filter(
          (node) => !fetchedCourses.some((course) => course.id === node.id)
        )
        .map((node) => node.id);
      courses.value = fetchedCourses.filter(
        (course) => !deletedNodeIds.includes(course.id)
      );
    } catch (err) {
      error.value = "Failed to fetch courses";
      console.error("Failed to fetch courses:", err);
    } finally {
      isLoading.value = false;
    }
  }

  async function addCourse(name: string, parentId: string | null = null) {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await axios.post(
        `${API_URL}/courses`,
        {
          name,
          parent_name: parentId,
        }
      );
      courses.value.push(response.data);
      return response.data;
    } catch (err) {
      error.value = "Failed to add course";
      console.error("Failed to add course:", err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  return {
    courses,
    isLoading,
    error,
    fetchCourses,
    addCourse,
  };
});
