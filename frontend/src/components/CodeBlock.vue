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
import 'prismjs/themes/prism-tomorrow.css'
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
.code-block-wrapper {
  background: #2d2d2d;
  border-radius: 12px;
  overflow: hidden;
  margin: 20px 0;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: #1e1e1e;
  border-bottom: 1px solid #3e3e3e;
}

.code-title {
  color: #e2e8f0;
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
  color: #94a3b8;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
}

.code-action-btn:hover {
  background: #3e3e3e;
  color: #e2e8f0;
}

.code-content {
  padding: 20px;
  overflow-x: auto;
  transition: max-height 0.3s ease;
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
}

.code-content code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  line-height: 1.6;
  color: #e2e8f0;
}

/* Prism.js 覆盖样式 */
.code-content :deep(.token.comment),
.code-content :deep(.token.prolog),
.code-content :deep(.token.doctype),
.code-content :deep(.token.cdata) {
  color: #6a9955;
}

.code-content :deep(.token.punctuation) {
  color: #d4d4d4;
}

.code-content :deep(.token.property),
.code-content :deep(.token.tag),
.code-content :deep(.token.boolean),
.code-content :deep(.token.number),
.code-content :deep(.token.constant),
.code-content :deep(.token.symbol),
.code-content :deep(.token.deleted) {
  color: #b5cea8;
}

.code-content :deep(.token.selector),
.code-content :deep(.token.attr-name),
.code-content :deep(.token.string),
.code-content :deep(.token.char),
.code-content :deep(.token.builtin),
.code-content :deep(.token.inserted) {
  color: #ce9178;
}

.code-content :deep(.token.operator),
.code-content :deep(.token.entity),
.code-content :deep(.token.url),
.code-content :deep(.language-css .token.string),
.code-content :deep(.style .token.string) {
  color: #d4d4d4;
}

.code-content :deep(.token.atrule),
.code-content :deep(.token.attr-value),
.code-content :deep(.token.keyword) {
  color: #569cd6;
}

.code-content :deep(.token.function) {
  color: #dcdcaa;
}

.code-content :deep(.token.class-name) {
  color: #4ec9b0;
}

.code-content :deep(.token.regex),
.code-content :deep(.token.important),
.code-content :deep(.token.variable) {
  color: #d16969;
}
</style>
