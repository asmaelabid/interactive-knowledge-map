import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

interface Course {
  id: string;
  name: string;
  parent_id: string | null;
}

export const useCourseStore = defineStore("courses", () => {
  const courses = ref<Course[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  async function fetchCourses() {
    if (courses.value.length > 0) return;
    
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await axios.get('http://localhost:8000/api/v1/courses');
      courses.value = response.data;
    } catch (err) {
      error.value = 'Failed to fetch courses';
      console.error('Failed to fetch courses:', err);
    } finally {
      isLoading.value = false;
    }
  }

  async function addCourse(name: string, parentId: string | null = null) {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await axios.post('http://localhost:8000/api/v1/courses', {
        name,
        parent_id: parentId
      });
      courses.value.push(response.data);
      return response.data;
    } catch (err) {
      error.value = 'Failed to add course';
      console.error('Failed to add course:', err);
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
