<!-- 出力画面 -->
<script setup lang="ts">
import { useRoute } from 'vue-router';
import Expressive from '../components/Mirocore/Expressive.vue';
import PromptBar from '../components/Mirocore/PromptBar.vue';


const route = useRoute();
const mode = route.query.mode
const prompt = route.query.prompt
</script>

<template>
    <div class="output-container">
        <section class="output-expressive">
            <Expressive/>
        </section>
        <section class="output-board">
            <!-- 出力表示ボード -->
            <div>
                <p>{{ prompt }}</p>
                <p>{{ mode }}</p>
            </div>
        </section>
        <section class="output-prompt-bar">
            <PromptBar/>
        </section>
    </div>
</template>

<style scoped>
.output-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
  width: min(100%, 800px);
  height: 100%;
  min-height: 0;
  padding: 32px 24px;
}

.output-expressive,
.output-board,
.output-prompt-bar {
  width: 100%;
}

.output-expressive {
  flex: none;
  margin-bottom: 16px;
}

.output-expressive :deep(#expressive-canvas) {
  width: 96px;
  height: 96px;
  margin-inline: auto;
}

.output-board {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}

.output-board > div {
  box-sizing: border-box;
  width: 100%;
  min-height: 100%;
  padding: 16px;
  /* border: 1px solid #ccc; */
  /* background: #f0f0f0; */
}

.output-prompt-bar {
  flex: none;
  margin-top: 16px;
}

.output-prompt-bar :deep(.prompt-bar) {
  width: 100%;
  max-width: none;
}
</style>