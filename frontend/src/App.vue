<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { RouterView, RouterLink, useRouter, useRoute } from 'vue-router';
import Sidebar from './components/AppDesign/Sidebar.vue';

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
  <section>
    <button @click="toggleSidebar" type="button" aria-label="メニューを開く">Toggle Sidebar</button>
  </section>
  <Sidebar :is-open=isSidebarOpen @toggle-sidebar="toggleSidebar" />
  <main>
    <!-- Mirocの表情を表す。Canvasを載せる -->
    <section>
      <h2>Mirocの表情</h2>
    </section>
    <!-- プロンプトバー設置　・・各自モードを選べるようにする。 -->
    <section>
      <h2>プロンプトバー</h2>
    </section>

    <!-- 全ての画面を表示するためのルーター -->
    <section>
      <router-view />
    </section>

  </main>
</template>
