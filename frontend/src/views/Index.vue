<script setup lang="ts">
import Expressive from '../components/Mirocore/Expressive.vue';
import PromptBar from '../components/Mirocore/PromptBar.vue';
import ModeSlecter from '../components/Mirocore/ModeSlecter.vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const selected_mode = ref<string>('memory_get');

const SelectedMode = (mode: string) => {
    selected_mode.value = mode
    console.log("選択されたモード：", selected_mode.value)
}
const submitPrompt = (text: string) => {
    router.push({
        name: 'output',
        query: {
            mode: selected_mode.value,
            prompt: text,
        }
    })
}

</script>

<template>
    <div class="home-container">
        <section class="home-sections">
            <Expressive />
            <PromptBar @submit-prompt="submitPrompt" />
        </section>
        <ModeSlecter @submit-mode="SelectedMode" />
    </div>
</template>

<style scoped>
/* .home-container {
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
} */
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  box-sizing: border-box;
  width: min(100%, 800px);
  height: 100%;
  padding: 32px 24px;
}

.home-sections,
.mode-select-belt {
  width: 100%;
}

.home-sections {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.home-sections :deep(#expressive-canvas) {
  width: 100%;
  height: 36svh;
}

.home-sections :deep(.prompt-bar) {
  width: 100%;
  max-width: none;
}

</style>