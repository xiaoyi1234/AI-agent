<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
// 主应用组件
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  margin: 0;
  padding: 0;
  background: var(--bg-primary);
  color: var(--text-primary);
}

/* 全局滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
  background: var(--primary-color);
  border-radius: 4px;
  box-shadow: var(--glow-primary);
}

::-webkit-scrollbar-thumb:hover {
  background: var(--secondary-color);
}

/* 全局选择文本样式 */
::selection {
  background: var(--primary-color);
  color: white;
}

::-moz-selection {
  background: var(--primary-color);
  color: white;
}

/* 全局焦点样式 */
*:focus {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

/* 全局链接样式 */
a {
  color: var(--primary-color);
  text-decoration: none;
  transition: color 0.3s ease;
}

a:hover {
  color: var(--secondary-color);
}

/* 全局按钮样式 */
button {
  font-family: inherit;
}

/* 全局输入框样式 */
input, textarea, select {
  font-family: inherit;
}

/* 全局图片样式 */
img {
  max-width: 100%;
  height: auto;
}
</style>
