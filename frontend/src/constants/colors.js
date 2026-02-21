/**
 * 魔方颜色常量定义
 * 
 * 提供统一的颜色映射，用于 2D 面视图和 3D 渲染组件。
 * 颜色值基于标准魔方配色方案。
 * 
 * @module constants/colors
 */

/**
 * 颜色名称到十六进制值的映射
 * @constant {Object.<string, string>}
 */
export const COLOR_MAP = {
  white: '#FFFFFF',
  yellow: '#FFD500',
  red: '#C41E3A',
  orange: '#FF5800',
  blue: '#0051BA',
  green: '#009E60',
  internal: '#222222',
  black: '#000000',
  gray: '#808080'
}

/**
 * 标准魔方六面颜色名称（按 U, D, F, B, L, R 顺序）
 * 用于数字索引到颜色名称的转换
 * @constant {string[]}
 */
export const COLOR_NAMES = ['white', 'yellow', 'red', 'orange', 'blue', 'green']

/**
 * 颜色名称到数字索引的映射
 * @constant {Object.<string, number>}
 */
export const COLOR_INDEX = {
  white: 0,
  yellow: 1,
  red: 2,
  orange: 3,
  blue: 4,
  green: 5
}

/**
 * 获取颜色的十六进制值
 * @param {string} colorName - 颜色名称
 * @returns {string} 十六进制颜色值，未知颜色返回灰色
 */
export function getHexColor(colorName) {
  return COLOR_MAP[colorName] || COLOR_MAP.gray
}

/**
 * 根据数字索引获取颜色名称
 * @param {number} index - 颜色索引 (0-5)
 * @returns {string} 颜色名称
 */
export function getColorName(index) {
  return COLOR_NAMES[index] || 'gray'
}

/**
 * 根据数字索引获取十六进制颜色值
 * @param {number} index - 颜色索引 (0-5)
 * @returns {string} 十六进制颜色值
 */
export function getHexColorByIndex(index) {
  const colorName = getColorName(index)
  return getHexColor(colorName)
}
