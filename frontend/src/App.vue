<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { RouterView, RouterLink, useRouter, useRoute } from 'vue-router';
import Sidebar from './components/AppDesign/Sidebar.vue';
import Expressive from './components/Mirocore/Expressive.vue';
import PromptBar from './components/Mirocore/PromptBar.vue';


onMounted(async() => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/health')
    if (!response.ok){
      throw new Error("Failed to fetch health check")
    }
    const data = await response.json()
    console.log("Health Check Response:", data)
    if (data.status=="ok"){
      console.log("Health Messgae:", data.message)
    } else {
      console.error("I can't get the Health Message")
    }
  } catch (error) {
    console.error("Error fetching health check:", error)
  }
})

const isSidebarOpen = ref(false)
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

</script>

<template>
  <div class="app-container">
    <aside class="sidebar-section" :class="{ 'is-open': isSidebarOpen }">
      <button @click="toggleSidebar" type="button" aria-label="メニューを開く" v-if="!isSidebarOpen">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-menu-app" viewBox="0 0 16 16">
          <path d="M0 1.5A1.5 1.5 0 0 1 1.5 0h2A1.5 1.5 0 0 1 5 1.5v2A1.5 1.5 0 0 1 3.5 5h-2A1.5 1.5 0 0 1 0 3.5zM1.5 1a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 .5.5h2a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-.5-.5zM0 8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm1 3v2a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2zm14-1V8a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v2zM2 8.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5m0 4a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 0 1h-6a.5.5 0 0 1-.5-.5"/>
        </svg>
      </button>
      <button @click="toggleSidebar" type="button" aria-label="メニューを閉じる" v-if="isSidebarOpen">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-menu-app-fill" viewBox="0 0 16 16">
          <path d="M0 1.5A1.5 1.5 0 0 1 1.5 0h2A1.5 1.5 0 0 1 5 1.5v2A1.5 1.5 0 0 1 3.5 5h-2A1.5 1.5 0 0 1 0 3.5zM0 8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm1 3v2a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2zm14-1V8a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v2zM2 8.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5m0 4a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 0 1h-6a.5.5 0 0 1-.5-.5"/>
        </svg>  
      </button>
      <Sidebar :is-open=isSidebarOpen @toggle-sidebar="toggleSidebar" />
    </aside>
    <main>
      <!-- Mirocの表情を表す。Canvasを載せる -->
      <section class="face-prompt-section">
        <Expressive />
        <!-- プロンプトバー設置　・・各自モードを選べるようにする。 -->
        <PromptBar />
        <!-- 全ての画面を表示するためのルーター -->
        <section class="screen-section">
          <router-view />
        </section>
      </section>
    </main>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  width: 100%;
  height: 100svh;
}

.sidebar-section {
  position: relative;
  flex: none;
  width: 56px;
  height: 100%;
  z-index: 20;
}
.sidebar-section button{
  position: absolute;
  z-index: 1;
}
.content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  height: 100%;
}

main {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 0;
}

.face-prompt-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: min(100%, 480px);
}

.prompt-bar-section {
  flex: none;
  padding: 12px 16px 16px;
}
</style>