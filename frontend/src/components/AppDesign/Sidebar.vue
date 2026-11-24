<!-- サイドバーのコンポーネント -->
<script setup lang="ts">
const props = defineProps<{
  isOpen: boolean
}>()

const emit = defineEmits<{
    (e: 'toggle-sidebar'): void
}>()


</script>

<template>
    <aside class="sidebar" v-if="isOpen">
        <nav aria-label="メインメニュー">
            <h3>メインメニュー</h3>
        </nav>
    </aside>
</template>

<style scoped>
.sidebar {
  position: absolute;
  top: 0;
  left: 0;
  box-sizing: border-box;
  width: 240px;
  height: 100%;
  padding: 56px 16px 16px;
  border-right: 1px solid #ccc;
}
nav {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
h2 {
  margin: 0;
  font-size: 16px;
}
</style>