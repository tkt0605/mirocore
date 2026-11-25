<script setup lang="ts">
import { ref } from 'vue';

const modes = [
    { id: "memory_get", text: "引き出す" },
    { id: "memory_read", text: "読み出す" },
    { id: "memory_write", text: "書き込む" },
    { id: "memory_delete", text: "消去する" },
];

const selectedMode = ref<(typeof modes)[number]['id']>('memory_get')
</script>

<template>
    <div class="mode-select-belt">
        <ul>
            <li v-for="mode in modes" :key="mode.id">
                <button
                    type="button"
                    :aria-pressed="selectedMode === mode.id"
                    @click="selectedMode = mode.id"
                >
                    {{ mode.text }}
                </button>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.mode-select-belt ul {
  display: flex;
  gap: 8px;
  margin: 0;
  padding: 0;
  list-style: none;
}
</style>