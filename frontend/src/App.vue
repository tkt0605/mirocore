<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'
import { onMounted } from 'vue';

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

</script>

<template>
  <HelloWorld />
</template>
