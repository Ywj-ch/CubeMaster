/**
 * 成绩记录管理 Composable
 * 使用 localStorage 持久化存储魔方还原记录
 */

import { ref, computed } from "vue";

const STORAGE_KEY = "cubemaster_records";
const MAX_RECORDS = 1000;

const records = ref([]);

function loadRecords() {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    if (data) {
      records.value = JSON.parse(data);
    }
  } catch (e) {
    console.error("Failed to load records:", e);
    records.value = [];
  }
}

function saveRecords() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(records.value));
  } catch (e) {
    console.error("Failed to save records:", e);
  }
}

loadRecords();

export function useRecords() {
  const sortedRecords = computed(() => {
    return [...records.value].sort(
      (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
    );
  });

  const bestTime = computed(() => {
    if (records.value.length === 0) return null;
    return Math.min(...records.value.map((r) => r.time));
  });

  const worstTime = computed(() => {
    if (records.value.length === 0) return null;
    return Math.max(...records.value.map((r) => r.time));
  });

  const averageTime = computed(() => {
    if (records.value.length === 0) return null;
    const sum = records.value.reduce((acc, r) => acc + r.time, 0);
    return sum / records.value.length;
  });

  const averageOf5 = computed(() => {
    if (records.value.length < 5) return null;
    const recent5 = sortedRecords.value.slice(0, 5);
    const sum = recent5.reduce((acc, r) => acc + r.time, 0);
    return sum / 5;
  });

  const averageOf12 = computed(() => {
    if (records.value.length < 12) return null;
    const recent12 = sortedRecords.value.slice(0, 12);
    const sum = recent12.reduce((acc, r) => acc + r.time, 0);
    return sum / 12;
  });

  const totalSolves = computed(() => records.value.length);

  const totalPracticeTime = computed(() => {
    return records.value.reduce((acc, r) => acc + r.time, 0);
  });

  const recordsByDate = computed(() => {
    const grouped = {};
    records.value.forEach((r) => {
      const dateKey = new Date(r.date).toLocaleDateString();
      if (!grouped[dateKey]) {
        grouped[dateKey] = [];
      }
      grouped[dateKey].push(r);
    });
    return grouped;
  });

  const recent7Days = computed(() => {
    const days = [];
    const now = new Date();
    for (let i = 6; i >= 0; i--) {
      const d = new Date(now);
      d.setDate(d.getDate() - i);
      const dateKey = d.toLocaleDateString();
      const dayRecords = recordsByDate.value[dateKey] || [];
      days.push({
        date: dateKey,
        count: dayRecords.length,
        avgTime:
          dayRecords.length > 0
            ? dayRecords.reduce((acc, r) => acc + r.time, 0) / dayRecords.length
            : null,
      });
    }
    return days;
  });

  function addRecord(record) {
    try {
      if (!record || typeof record.time !== "number") {
        console.error("Invalid record data:", record);
        return null;
      }

      const newRecord = {
        id: Date.now(),
        time: record.time,
        scramble: record.scramble || "",
        moves: record.moves || 0,
        tps: record.tps || 0,
        date: new Date().toISOString(),
      };

      records.value.unshift(newRecord);

      if (records.value.length > MAX_RECORDS) {
        records.value = records.value.slice(0, MAX_RECORDS);
        console.warn(
          `Reached maximum records limit (${MAX_RECORDS}), removing oldest records`,
        );
      }

      saveRecords();
      return newRecord;
    } catch (error) {
      console.error("Failed to add record:", error);
      return null;
    }
  }

  function deleteRecord(id) {
    const index = records.value.findIndex((r) => r.id === id);
    if (index !== -1) {
      records.value.splice(index, 1);
      saveRecords();
    }
  }

  function clearAllRecords() {
    records.value = [];
    saveRecords();
  }

  function exportRecords() {
    const dataStr = JSON.stringify(records.value, null, 2);
    const blob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `cubemaster-records-${new Date().toISOString().split("T")[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function importRecords(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result);
          if (Array.isArray(data)) {
            records.value = data;
            saveRecords();
            resolve(data.length);
          } else {
            reject(new Error("Invalid format"));
          }
        } catch (err) {
          reject(err);
        }
      };
      reader.onerror = reject;
      reader.readAsText(file);
    });
  }

  return {
    records: sortedRecords,
    bestTime,
    worstTime,
    averageTime,
    averageOf5,
    averageOf12,
    totalSolves,
    totalPracticeTime,
    recent7Days,
    addRecord,
    deleteRecord,
    clearAllRecords,
    exportRecords,
    importRecords,
  };
}
