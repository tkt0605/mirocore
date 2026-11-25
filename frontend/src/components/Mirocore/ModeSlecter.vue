<script setup lang="ts">
import { ref } from 'vue';
const modes = [
    { id: "memory_get", text: "引き出す" },
    { id: "memory_read", text: "読み出す" },
    { id: "memory_write", text: "書き込む" },
    { id: "memory_delete", text: "消去する" },
]
const selectedMode = ref<(typeof modes)[number]['id']>('memory_get')

const emit = defineEmits<{
    (e: "submit-mode", mode: (typeof modes)[number]['id']): void
}>()

const SubmitMode = (mode: (typeof modes)[number]['id']): void => {
    selectedMode.value = mode
    emit('submit-mode', mode)
}
</script>

<template>
        <div class="mode-select-belt">
            <ul>
                <li v-for="mode in modes" :key="mode.id">
                    <button
                        type="button"
                        :aria-pressed="selectedMode === mode.id"
                        @click="SubmitMode(mode.id)"
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
  justify-content: center;
  gap: 8px;
  width: 100%;
  margin: 0;
  padding: 0;
  list-style: none;
}
.mode-select-belt button {
  cursor: pointer;
  padding: 6px 12px;
  border: 1px solid #ccc;
  background: #fff;
}

.mode-select-belt button[aria-pressed="true"] {
  background: #f0f0f0;
}
</style>