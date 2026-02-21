/**
 * @fileoverview 全局加载状态管理组合式函数
 * 
 * 提供全局加载指示器的状态管理，使用单例模式确保整个应用共享同一加载状态。
 * 
 * @module composables/useLoading
 */

import { ref } from 'vue'

/** @type {import('vue').Ref<boolean>} 全局加载状态 */
const isLoading = ref(false)

/** @type {import('vue').Ref<string>} 加载提示文本 */
const loadingText = ref('')

/**
 * 加载状态管理组合式函数
 * 
 * @returns {Object} 加载状态和方法
 * @property {import('vue').Ref<boolean>} isLoading - 是否正在加载
 * @property {import('vue').Ref<string>} loadingText - 加载提示文本
 * @property {Function} showLoading - 显示加载状态
 * @property {Function} hideLoading - 隐藏加载状态
 * @property {Function} withLoading - 包装异步函数，自动显示/隐藏加载状态
 * 
 * @example
 * const { isLoading, showLoading, hideLoading } = useLoading()
 * showLoading('正在处理...')
 * // ... 执行操作
 * hideLoading()
 * 
 * @example
 * // 使用 withLoading 包装异步操作
 * const { withLoading } = useLoading()
 * await withLoading(() => fetchData(), '加载数据中...')
 */
export function useLoading() {
  /**
   * 显示加载状态
   * @param {string} [text=''] - 加载提示文本
   */
  function showLoading(text = '') {
    isLoading.value = true
    loadingText.value = text
  }

  /**
   * 隐藏加载状态
   */
  function hideLoading() {
    isLoading.value = false
    loadingText.value = ''
  }

  /**
   * 包装异步函数，自动显示和隐藏加载状态
   * 
   * @template T
   * @param {Function} asyncFn - 异步函数
   * @param {string} [text=''] - 加载提示文本
   * @returns {Promise<T>} 异步函数的返回值
   */
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
