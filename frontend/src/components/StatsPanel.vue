<template>
  <div class="stats-panel" :class="{ expanded: isVisible }">
    <div class="stats-header" @click="togglePanel">
      <div class="header-left">
        <svg class="stats-icon" viewBox="0 0 24 24" fill="currentColor">
          <path
            d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zM7 10h2v7H7zm4-3h2v10h-2zm4 6h2v4h-2z"
          />
        </svg>
        <span class="header-title">统计信息</span>
        <span v-if="totalSolves > 0" class="record-badge">{{
          totalSolves
        }}</span>
      </div>
      <svg
        class="expand-icon"
        :class="{ rotated: isVisible }"
        viewBox="0 0 24 24"
        fill="currentColor"
      >
        <path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z" />
      </svg>
    </div>

    <transition name="slide">
      <div v-if="isVisible" class="stats-content">
        <div v-if="totalSolves === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="currentColor" class="empty-icon">
            <path
              d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14z"
            />
          </svg>
          <p>暂无记录</p>
          <span>完成一次还原即可查看统计数据！</span>
        </div>

        <template v-else>
          <div class="stats-cards">
            <div class="stat-card best">
              <div class="stat-label">最佳成绩</div>
              <div class="stat-value">{{ formatTime(bestTime) }}</div>
            </div>
            <div class="stat-card avg">
              <div class="stat-label">平均时间</div>
              <div class="stat-value">{{ formatTime(averageTime) }}</div>
            </div>
            <div class="stat-card total">
              <div class="stat-label">还原次数</div>
              <div class="stat-value">{{ totalSolves }}</div>
            </div>
            <div class="stat-card ao5">
              <div class="stat-label">平均5次</div>
              <div class="stat-value">{{ averageOf5 ? formatTime(averageOf5) : '-' }}</div>
            </div>
            <div class="stat-card ao12">
              <div class="stat-label">平均12次</div>
              <div class="stat-value">{{ averageOf12 ? formatTime(averageOf12) : '-' }}</div>
            </div>
            <div class="stat-card practice">
               <div class="stat-label">练习时长</div>
               <div class="stat-value">{{ formatPracticeTime }}</div>
             </div>
           </div>

          <div class="chart-section">
            <div class="section-header">
              <span class="section-title">最近7天</span>
            </div>
            <div class="mini-chart">
              <div
                v-for="(day, index) in recent7Days"
                :key="index"
                class="chart-bar"
                :style="{ height: getBarHeight(day.count) }"
                   :title="`${day.date}: ${day.count}次还原`"
              >
                <span v-if="day.count > 0" class="bar-count">{{
                  day.count
                }}</span>
              </div>
            </div>
            <div class="chart-labels">
              <span
                v-for="(day, index) in recent7Days"
                :key="index"
                class="chart-label"
              >
                {{ getDayLabel(day.date) }}
              </span>
            </div>
          </div>

          <div class="history-section">
            <div class="section-header">
              <span class="section-title">最近记录</span>
              <div class="header-actions">
                <button
                  class="action-btn"
                  @click="exportRecords"
                   title="导出"
                >
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path
                      d="M19 12v7H5v-7H3v7c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-7h-2zm-6 .67l2.59-2.58L17 11.5l-5 5-5-5 1.41-1.41L11 12.67V3h2v9.67z"
                    />
                  </svg>
                </button>
                <button
                  class="action-btn danger"
                  @click="confirmClear"
                   title="清空记录"
                >
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path
                      d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"
                    />
                  </svg>
                </button>
              </div>
            </div>
            <div class="history-list">
              <div
                v-for="record in records.slice(0, 10)"
                :key="record.id"
                class="history-item"
                :class="{ best: record.time === bestTime }"
              >
                <div class="item-time">{{ formatTime(record.time) }}</div>
                <div class="item-details">
                  <span class="item-date">{{ formatDate(record.date) }}</span>
                  <span v-if="record.tps" class="item-tps"
                    >{{ record.tps }} TPS</span
                  >
                </div>
                <button
                  class="delete-btn"
                  @click="deleteRecord(record.id)"
                  title="Delete"
                >
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path
                      d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
                    />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </template>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRecords } from "../composables/useRecords";

const {
  records,
  bestTime,
  averageTime,
  averageOf5,
  averageOf12,
  totalSolves,
  recent7Days,
  deleteRecord,
  clearAllRecords,
  exportRecords,
} = useRecords();

const isVisible = ref(false);

function togglePanel() {
  isVisible.value = !isVisible.value;
}

function formatTime(ms) {
  if (ms === null || ms === undefined) return "-";
  const seconds = ms / 1000;
  const mins = Math.floor(seconds / 60);
  const secs = (seconds % 60).toFixed(2);
  return mins > 0 ? `${mins}:${secs.padStart(5, "0")}` : secs + "s";
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) return "刚刚";
    if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`;
    return date.toLocaleDateString();
  }

const formatPracticeTime = computed(() => {
  const totalMs =
    totalSolves.value > 0
      ? records.value.reduce((acc, r) => acc + r.time, 0)
      : 0;
  const hours = Math.floor(totalMs / 3600000);
  const mins = Math.floor((totalMs % 3600000) / 60000);
  if (hours > 0) return `${hours}h ${mins}m`;
  return `${mins}m`;
});

function getBarHeight(count) {
  const maxCount = Math.max(...recent7Days.value.map((d) => d.count), 1);
  const height = (count / maxCount) * 100;
  return height > 0 ? `${Math.max(height, 10)}%` : "4px";
}

function getDayLabel(dateStr) {
  const date = new Date(dateStr);
  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  return days[date.getDay()];
}

function confirmClear() {
  if (confirm('确定要删除所有记录吗？此操作无法撤销。')) {
    clearAllRecords()
  }
}
</script>

<style scoped>
.stats-panel {
  position: fixed;
  right: 20px;
  top: 220px;
  width: 320px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  z-index: 50;
  transition: all 0.3s ease;
}

[data-theme="dark"] .stats-panel {
  background: rgba(30, 41, 59, 0.95);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  cursor: pointer;
  user-select: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.3s;
}

.stats-panel.expanded .stats-header {
  border-bottom-color: rgba(0, 0, 0, 0.1);
}

[data-theme="dark"] .stats-panel.expanded .stats-header {
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.stats-icon {
  width: 20px;
  height: 20px;
  color: #6366f1;
}

.header-title {
  font-weight: 600;
  font-size: 15px;
  color: #1e293b;
}

[data-theme="dark"] .header-title {
  color: #e2e8f0;
}

.record-badge {
  background: #6366f1;
  color: white;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 10px;
}

.expand-icon {
  width: 24px;
  height: 24px;
  color: #94a3b8;
  transition: transform 0.3s ease;
}

.expand-icon.rotated {
  transform: rotate(180deg);
}

.stats-content {
  padding: 16px;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #94a3b8;
}

.empty-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.empty-state p {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: #64748b;
}

[data-theme="dark"] .empty-state p {
  color: #94a3b8;
}

.empty-state span {
  font-size: 13px;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 16px;
}

.stat-card {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  padding: 12px;
  text-align: center;
}

[data-theme="dark"] .stat-card {
  background: linear-gradient(135deg, #334155 0%, #1e293b 100%);
}

.stat-card.best {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
}

[data-theme="dark"] .stat-card.best {
  background: linear-gradient(135deg, #166534 0%, #14532d 100%);
}

.stat-label {
  font-size: 11px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

[data-theme="dark"] .stat-label {
  color: #94a3b8;
}

.stat-card.best .stat-label {
  color: #16a34a;
}

.stat-value {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
}

[data-theme="dark"] .stat-value {
  color: #e2e8f0;
}

.stat-card.best .stat-value {
  color: #15803d;
}

.chart-section {
  margin-bottom: 16px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 12px;
}

[data-theme="dark"] .chart-section {
  background: #1e293b;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.section-title {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
}

[data-theme="dark"] .section-title {
  color: #cbd5e1;
}

.mini-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  height: 60px;
  gap: 6px;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(to top, #6366f1, #818cf8);
  border-radius: 4px 4px 0 0;
  min-height: 4px;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  transition: all 0.2s;
}

.chart-bar:hover {
  filter: brightness(1.1);
}

.bar-count {
  font-size: 10px;
  font-weight: 600;
  color: white;
  padding-top: 4px;
}

.chart-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 6px;
}

.chart-label {
  flex: 1;
  text-align: center;
  font-size: 10px;
  color: #94a3b8;
}

.history-section {
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  padding-top: 12px;
}

[data-theme="dark"] .history-section {
  border-top-color: rgba(255, 255, 255, 0.1);
}

.header-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.action-btn svg {
  width: 16px;
  height: 16px;
  color: #64748b;
}

.action-btn:hover {
  background: rgba(0, 0, 0, 0.05);
}

[data-theme="dark"] .action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.action-btn.danger:hover {
  background: rgba(239, 68, 68, 0.1);
}

.action-btn.danger:hover svg {
  color: #ef4444;
}

.history-list {
  max-height: 200px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  border-radius: 8px;
  margin-bottom: 4px;
  background: #f8fafc;
  transition: all 0.2s;
}

[data-theme="dark"] .history-item {
  background: #334155;
}

.history-item:hover {
  background: #f1f5f9;
}

[data-theme="dark"] .history-item:hover {
  background: #475569;
}

.history-item.best {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
}

[data-theme="dark"] .history-item.best {
  background: linear-gradient(135deg, #166534 0%, #14532d 100%);
}

.item-time {
  font-size: 15px;
  font-weight: 700;
  color: #1e293b;
  min-width: 70px;
}

[data-theme="dark"] .item-time {
  color: #e2e8f0;
}

.history-item.best .item-time {
  color: #15803d;
}

.item-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.item-date {
  font-size: 12px;
  color: #94a3b8;
}

.item-tps {
  font-size: 11px;
  color: #6366f1;
}

.delete-btn {
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.2s;
}

.history-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn svg {
  width: 16px;
  height: 16px;
  color: #94a3b8;
}

.delete-btn:hover svg {
  color: #ef4444;
}
</style>
