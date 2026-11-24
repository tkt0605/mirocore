<script setup lang="ts">
</script>

<template>
    <div class="prompt-bar">
        <input type="text" placeholder="プロンプトを入力してください" />
        <button type="button" aria-label="送信">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                <path d="M15.854 5.146a.5.5 0 0 1 0 .708L13.707 8l2.147 2.146a.5.5 0 0 1-.708.708L13 8.707l-2.146 2.147a.5.5 0 0 1-.708-.708L12.293 8 10.146 5.854a.5.5 0 1 1 .708-.708L13 7.293l2.146-2.147a.5.5 0 0 1 .708 0z"/>
            </svg>
        </button>
    </div>
</template>

<style scoped>
/* .prompt-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    box-sizing: border-box;
    width: 100%;
    max-width: 512px;
    padding: 8px 12px;
    background: #f0f0f0;
    border: 1px solid #ccc;
} */
.prompt-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  box-sizing: border-box;
  width: 100%;
  max-width: 512px;
  margin-inline: auto;
  padding: 8px 12px;
  background: #f0f0f0;
  border: 1px solid #ccc;
}

.prompt-bar input {
  flex: 1;
  min-width: 0;
  border: 0;
  background: transparent;
  font: inherit;
}

.prompt-bar button {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  padding: 0;
  border: 0;
  background: transparent;
}
</style>