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
            <button type="button" aria-label="メニューを閉じる" @click="emit('toggle-sidebar')">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg> 
            </button>
        </nav>
    </aside>
</template>