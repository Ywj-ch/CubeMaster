<template>
  <div class="code-block-wrapper">
    <div class="code-header">
      <span class="code-title">{{ title }}</span>
      <div class="code-actions">
        <button 
          v-if="foldable" 
          @click="toggleFold" 
          class="code-action-btn"
          :title="isFolded ? '展开代码' : '折叠代码'"
        >
          <el-icon v-if="isFolded"><ArrowDown /></el-icon>
          <el-icon v-else><ArrowUp /></el-icon>
        </button>
        <button 
          @click="copyCode" 
          class="code-action-btn"
          :title="copySuccess ? '已复制!' : '复制代码'"
        >
          <el-icon v-if="copySuccess"><Check /></el-icon>
          <el-icon v-else><DocumentCopy /></el-icon>
        </button>
      </div>
    </div>
    <div class="code-content" :class="{ folded: isFolded }">
      <pre><code :class="`language-${language}`">{{ code }}</code></pre>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ArrowDown, ArrowUp, DocumentCopy, Check } from '@element-plus/icons-vue'
import Prism from 'prismjs'
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-javascript'
import 'prismjs/components/prism-bash'

const props = defineProps({
  language: {
    type: String,
    default: 'python'
  },
  code: {
    type: String,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  foldable: {
    type: Boolean,
    default: true
  }
})

const isFolded = ref(false)
const copySuccess = ref(false)

const toggleFold = () => {
  isFolded.value = !isFolded.value
}

const copyCode = async () => {
  try {
    await navigator.clipboard.writeText(props.code)
    copySuccess.value = true
    setTimeout(() => {
      copySuccess.value = false
    }, 2000)
  } catch (err) {
    console.error('复制失败:', err)
  }
}

onMounted(() => {
  if (props.language && props.code) {
    Prism.highlightAll()
  }
})
</script>

<style scoped>
/* CSS 变量定义 - 白天模式（默认） */
.code-block-wrapper {
  --code-bg: #f8fafc;
  --code-header-bg: #f1f5f9;
  --code-border: #e2e8f0;
  --code-title-color: #475569;
  --code-text-color: #1e293b;
  --code-btn-color: #64748b;
  --code-btn-hover-bg: #e2e8f0;
  --code-btn-hover-color: #1e293b;
  
  /* 语法高亮颜色 */
  --token-comment: #6b7280;
  --token-keyword: #2563eb;
  --token-string: #059669;
  --token-function: #ea580c;
  --token-number: #0891b2;
  --token-operator: #4b5563;
  --token-punctuation: #64748b;
  --token-class-name: #7c3aed;
  --token-variable: #dc2626;
  --token-property: #0891b2;
  --token-boolean: #2563eb;
  --token-constant: #0891b2;
}

/* 黑夜模式 */
[data-theme="dark"] .code-block-wrapper {
  --code-bg: #1e293b;
  --code-header-bg: #0f172a;
  --code-border: #334155;
  --code-title-color: #cbd5e1;
  --code-text-color: #e2e8f0;
  --code-btn-color: #94a3b8;
  --code-btn-hover-bg: #334155;
  --code-btn-hover-color: #f1f5f9;
  
  /* 语法高亮颜色 */
  --token-comment: #6a9955;
  --token-keyword: #60a5fa;
  --token-string: #fbbf24;
  --token-function: #c084fc;
  --token-number: #2dd4bf;
  --token-operator: #94a3b8;
  --token-punctuation: #cbd5e1;
  --token-class-name: #22d3ee;
  --token-variable: #f87171;
  --token-property: #2dd4bf;
  --token-boolean: #60a5fa;
  --token-constant: #2dd4bf;
}

/* 基础样式 */
.code-block-wrapper {
  background: var(--code-bg);
  border-radius: 12px;
  overflow: hidden;
  margin: 20px 0;
  border: 1px solid var(--code-border);
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: var(--code-header-bg);
  border-bottom: 1px solid var(--code-border);
}

.code-title {
  color: var(--code-title-color);
  font-size: 14px;
  font-weight: 600;
  font-family: 'JetBrains Mono', monospace;
}

.code-actions {
  display: flex;
  gap: 8px;
}

.code-action-btn {
  background: transparent;
  border: none;
  color: var(--code-btn-color);
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
}

.code-action-btn:hover {
  background: var(--code-btn-hover-bg);
  color: var(--code-btn-hover-color);
}

.code-content {
  padding: 20px;
  overflow-x: auto;
  transition: max-height 0.3s ease;
  text-align: left;
}

.code-content.folded {
  max-height: 0;
  padding: 0 20px;
  overflow: hidden;
}

.code-content pre {
  margin: 0;
  padding: 0;
  background: transparent;
  text-align: left;
}

.code-content code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  line-height: 1.6;
  color: var(--code-text-color);
  display: block;
  text-align: left;
}

/* Prism.js 语法高亮覆盖 - 使用 CSS 变量 */
.code-content :deep(.token.comment),
.code-content :deep(.token.prolog),
.code-content :deep(.token.doctype),
.code-content :deep(.token.cdata) {
  color: var(--token-comment);
}

.code-content :deep(.token.punctuation) {
  color: var(--token-punctuation);
}

.code-content :deep(.token.property),
.code-content :deep(.token.tag),
.code-content :deep(.token.boolean),
.code-content :deep(.token.number),
.code-content :deep(.token.constant),
.code-content :deep(.token.symbol),
.code-content :deep(.token.deleted) {
  color: var(--token-number);
}

.code-content :deep(.token.selector),
.code-content :deep(.token.attr-name),
.code-content :deep(.token.string),
.code-content :deep(.token.char),
.code-content :deep(.token.builtin),
.code-content :deep(.token.inserted) {
  color: var(--token-string);
}

.code-content :deep(.token.operator),
.code-content :deep(.token.entity),
.code-content :deep(.token.url),
.code-content :deep(.language-css .token.string),
.code-content :deep(.style .token.string) {
  color: var(--token-operator);
}

.code-content :deep(.token.atrule),
.code-content :deep(.token.attr-value),
.code-content :deep(.token.keyword) {
  color: var(--token-keyword);
}

.code-content :deep(.token.function) {
  color: var(--token-function);
}

.code-content :deep(.token.class-name) {
  color: var(--token-class-name);
}

.code-content :deep(.token.regex),
.code-content :deep(.token.important),
.code-content :deep(.token.variable) {
  color: var(--token-variable);
}
</style>
