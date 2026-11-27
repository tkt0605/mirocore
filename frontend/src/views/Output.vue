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
const message = ref<string>("")

onMounted(async () => {
    if (typeof prompt !== "string"){
        return;
    }
    try {
        if(mode === "memory_get"){
            await searchMemory(user, prompt)
        }else if (mode === "memory_read"){
            await readMemory(user, prompt)
        }else if (mode === "memory_write"){
            await writeMemory(user, prompt)
        }else if (mode === "memory_delete"){
            await deleteMemory(user, prompt)
        }
    } catch (error) {
        console.error("Error fetching memory search results:", error)
        message.value = "エラーが発生しました。"
        return;
    }
})

const searchMemory = async(user: string, prompt: string): Promise<void> => {
    try{
        const params = new URLSearchParams({
            user_name: user,
            query: prompt,
        })
        const response = await fetch(
            `http://localhost:8000/api/memory/search?${params.toString()}`,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            }
        )
        const data = await response.json()
        if (!response.ok) {
            throw new Error(data.detail || "Failed to fetch memory search results")
        }
        results.value = data.results
    }catch(error){
        console.error("Error fetching memory search results:", error)
    }
}

const readMemory = async(user: string, prompt: string): Promise<void> => {
    try {
        const params = new URLSearchParams({
            user_name: user,
            text: prompt
        })
        const response = await fetch(
            `http://localhost:8000/api/memory/read?${params.toString()}`,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            }
        )
        const data = await response.json()
        if (!response.ok){
            throw new Error(data.detail || "Failed to read memory")
        }
        results.value = data.results
    } catch (error) {
        console.error("Error reading memory:", error)
        message.value = "エラーが発生しました。"
        return;
    }
}
const writeMemory = async(user: string, prompt: string): Promise<void> => {
    try {
        const params = new URLSearchParams({
            user_name: user,
            text:  prompt
        })
        const response = await fetch(
            `http://localhost:8000/api/memory/write?${params.toString()}`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    user_name: user,
                    text: prompt
                })
            }
        )
        const data = await response.json()
        if (!response.ok){
            throw new Error(data.detail || "Failed to write memory")
        }
        message.value = data.message
        results.value = data.saved && typeof data.memory === "string" ? [data.memory] : []
    }catch (error) {
        console.error("Error writing memory:", error)
        message.value = "エラーが発生しました。"
        return;
    }
}

const deleteMemory = async(user: string, prompt: string): Promise<void> => {
    try {
        const params = new URLSearchParams({
            user_name: user,
            text: prompt
        })
        const response = await fetch(
            `http://localhost:8000/api/memory/delete?${params.toString()}`,
            {
                method: "delete",
                headers: {
                    "Content-Type": "application/json",
                }
            }
        )
        const data = await response.json()
        if (!response.ok){
            throw new Error(data.detail || "Failed to delete memory")
        }
        message.value = data.message
        results.value = data.deleted
    } catch (error) {
        console.error("Error deleting memory:", error)
        message.value = "エラーが発生しました。"
        return;
    }
}

</script>

<template>
    <div class="output-container">
        <section class="output-expressive">
            <Expressive :face-size="100"/>
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