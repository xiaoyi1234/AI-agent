<template>
  <div class="layout">
    <header class="header">
      <div class="container">
        <div class="header-content">
          <h1 class="title">
            <span class="title-icon">🚀</span>
            AI 技术平台
          </h1>
          <nav class="nav">
            <router-link to="/" class="nav-link">
              <span class="nav-icon">🏠</span>
              主页
            </router-link>
            <router-link to="/love" class="nav-link">
              <span class="nav-icon">🔧</span>
              PCIE技术顾问
            </router-link>
            <router-link to="/manus" class="nav-link">
              <span class="nav-icon">🤖</span>
              AI 超级智能体
            </router-link>
            <router-link to="/typewriter" class="nav-link">
              <span class="nav-icon">⌨️</span>
              打字机版
            </router-link>
          </nav>
        </div>
      </div>
    </header>
    <main class="main">
      <div class="container">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
.layout {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  color: var(--text-primary);
  position: relative;
}

.layout::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(124, 58, 237, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(245, 158, 11, 0.05) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

.header {
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  background: rgba(26, 26, 46, 0.95);
  backdrop-filter: blur(20px);
  z-index: 100;
  box-shadow: var(--shadow-md);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) 0;
}

.title {
  margin: 0;
  font-size: var(--font-size-2xl);
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.title-icon {
  font-size: 28px;
  filter: drop-shadow(0 0 10px var(--primary-color));
}

.nav {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.nav-link {
  color: var(--text-secondary);
  text-decoration: none;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-weight: 500;
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  opacity: 0;
  transition: opacity var(--transition-normal);
  z-index: -1;
}

.nav-link:hover {
  color: white;
  transform: translateY(-2px);
}

.nav-link:hover::before {
  opacity: 0.1;
}

.nav-link.router-link-exact-active {
  color: white;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  box-shadow: var(--glow-primary);
}

.nav-icon {
  font-size: 16px;
}

.main {
  position: relative;
  z-index: 1;
  padding: var(--spacing-xl) 0;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: var(--spacing-md);
    padding: var(--spacing-sm) 0;
  }
  
  .title {
    font-size: var(--font-size-xl);
  }
  
  .nav {
    flex-wrap: wrap;
    justify-content: center;
    gap: var(--spacing-xs);
  }
  
  .nav-link {
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: var(--font-size-sm);
  }
  
  .container {
    padding: 0 var(--spacing-md);
  }
  
  .main {
    padding: var(--spacing-md) 0;
  }
}

@media (max-width: 480px) {
  .title {
    font-size: var(--font-size-lg);
  }
  
  .nav-link {
    padding: var(--spacing-xs);
    font-size: var(--font-size-xs);
  }
  
  .nav-icon {
    font-size: 14px;
  }
  
  .container {
    padding: 0 var(--spacing-sm);
  }
}
</style>

