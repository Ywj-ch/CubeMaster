<template>
  <div class="face">
    <div
      v-for="(cell, index) in face"
      :key="index"
      class="cell"
      :style="{ backgroundColor: colorMap[cell] }"
    >
    </div>
  </div>
</template>


<script setup>
const colorMap = {
  white: "#FFFFFF",
  yellow: "#FFD500",
  red: "#C41E3A",
  orange: "#FF5800",
  blue: "#0051BA",
  green: "#009E60",
};

defineProps({
  face: {
    type: Array,
    required: true
  }
});
</script>

<style scoped>
.face {
  display: grid;
  grid-template-columns: repeat(3, 40px);
  grid-template-rows: repeat(3, 40px);
  gap: 2px;
  margin: 2px;
}

.cell {
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #999;
  font-size: 12px;
}
</style>
