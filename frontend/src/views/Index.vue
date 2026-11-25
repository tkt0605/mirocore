<script setup lang="ts">
import Expressive from '../components/Mirocore/Expressive.vue';
import PromptBar from '../components/Mirocore/PromptBar.vue';
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
    <div class="home-container">
        <div>
            <section class="home-sections">
                <Expressive />
                <PromptBar />
            </section>
        </div>
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

    </div>
</template>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: min(100%, 480px);
}

.home-sections {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: 100%;
}

.mode-select-belt {
  width: 100%;
}

.mode-select-belt ul {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.mode-select-belt button {
  padding: 6px 12px;
  border: 1px solid #ccc;
  background: #fff;
}

.mode-select-belt button[aria-pressed="true"] {
  background: #f0f0f0;
}

</style>