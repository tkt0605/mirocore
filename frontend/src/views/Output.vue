<!-- 出力画面 -->
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import Expressive from '../components/Mirocore/Expressive.vue';
import PromptBar from '../components/Mirocore/PromptBar.vue';
import ModeSlecter from '../components/Mirocore/ModeSlecter.vue';


const route = useRoute();
const results = ref<string[]>([])

const mode = route.query.mode
const prompt = route.query.prompt

const user = "takato"

onMounted(async () => {
    try{
        if (mode !== "memory_get" || typeof prompt !== "string") {
            return;
        }
        const params = new URLSearchParams({
            user_name: user,
            query: prompt,
        })
        const response = await fetch(`http://localhost:8000/api/memory/search?${params.toString()}`)
        const data = await response.json()
        if (!response.ok) {
            throw new Error(data.detail || "Failed to fetch memory search results")
        }
        results.value = data.results
    }catch(error){
        console.error("Error fetching memory search results:", error)
    }
})

</script>

<template>
    <div class="output-container">
        <section class="output-expressive">
            <Expressive/>
        </section>
        <section class="output-board">
            <!-- 出力表示ボード -->
            <div>
                <div v-for="result in results" :key="result">
                    <p>{{ result }}</p>
                </div>
            </div>
        </section>
        <section class="output-prompt-bar">
            <PromptBar/>
            <div class="mode-select-belt">
                <ModeSlecter/>
            </div>
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

.mode-select-belt {
  width: 100%;
  margin-top: 16px;
}

</style>