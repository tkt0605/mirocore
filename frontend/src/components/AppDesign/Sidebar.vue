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
    <aside v-if="isOpen">
        <nav aria-label="メインメニュー">
            <h3>メインメニュー</h3>
        </nav>
    </aside>
</template>

<style scoped>
</style>