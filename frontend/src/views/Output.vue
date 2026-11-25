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
  width: min(100%, 480px);
  height: 100%;
  min-height: 0;
}

.output-expressive {
  flex: none;
  width: 96px;
  margin-top: 24px;
}

.output-board {
  flex: 1;
  width: 100%;
  min-height: 0;
  overflow-y: auto;
}

.output-board > div {
  width: 100%;
  height: auto;
  margin: 12px;
  padding: 12px;
  border: 1px solid #ccc;
}

.output-prompt-bar {
  flex: none;
  width: 100%;
  margin-bottom: 24px;
}
</style>