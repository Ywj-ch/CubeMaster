import { ref } from 'vue'

const isLoading = ref(false)
const loadingText = ref('')

export function useLoading() {
  function showLoading(text = '') {
    isLoading.value = true
    loadingText.value = text
  }

  function hideLoading() {
    isLoading.value = false
    loadingText.value = ''
  }

  async function withLoading(asyncFn, text = '') {
    showLoading(text)
    try {
      return await asyncFn()
    } finally {
      hideLoading()
    }
  }

  return {
    isLoading,
    loadingText,
    showLoading,
    hideLoading,
    withLoading
  }
}
