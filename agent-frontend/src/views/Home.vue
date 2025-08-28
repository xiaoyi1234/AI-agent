<template>
  <div class="home">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="hero-icon">🚀</span>
          AI 技术平台
        </h1>
        <p class="hero-subtitle">探索前沿AI技术，体验智能对话的未来</p>
      </div>
    </div>

    <div class="apps-section">
      <h2 class="section-title">选择应用开始体验</h2>
      <div class="apps-grid">
        <router-link to="/love" class="app-card">
          <div class="app-avatar">🔧</div>
          <div class="app-content">
            <h3 class="app-title">PCIE技术顾问</h3>
            <p class="app-description">专业的PCIE技术咨询，解决硬件连接问题</p>
            <div class="app-features">
              <span class="feature-tag">技术咨询</span>
              <span class="feature-tag">硬件支持</span>
            </div>
          </div>
          <div class="app-arrow">→</div>
        </router-link>

        <router-link to="/manus" class="app-card">
          <div class="app-avatar">🤖</div>
          <div class="app-content">
            <h3 class="app-title">AI 超级智能体</h3>
            <p class="app-description">强大的AI助手，提供全方位的智能服务</p>
            <div class="app-features">
              <span class="feature-tag">智能对话</span>
              <span class="feature-tag">多领域</span>
            </div>
          </div>
          <div class="app-arrow">→</div>
        </router-link>

                 <router-link to="/typewriter" class="app-card">
           <div class="app-avatar">⌨️</div>
           <div class="app-content">
             <h3 class="app-title">打字机版</h3>
             <p class="app-description">独特的打字机效果，体验复古的AI对话</p>
             <div class="app-features">
               <span class="feature-tag">打字机效果</span>
               <span class="feature-tag">复古体验</span>
             </div>
           </div>
           <div class="app-arrow">→</div>
         </router-link>
      </div>
    </div>

    <div class="storage-section">
      <div class="storage-card">
        <h3 class="storage-title">
          <span class="storage-icon">💾</span>
          存储状态检查
        </h3>
        <div class="storage-status">
          <div class="status-item">
            <span class="status-label">会话存储状态：</span>
            <span class="status-value" :class="{ 'status-ok': storageAvailable, 'status-error': !storageAvailable }">
              {{ storageAvailable ? '✅ 正常' : '❌ 不可用' }}
            </span>
          </div>
          <p class="storage-description">
            {{ storageAvailable ? '聊天记录将自动保存到会话存储中（关闭标签页后清除）' : '会话存储不可用，聊天记录将不会保存' }}
          </p>
        </div>
        <div class="storage-actions">
          <button @click="testStorage" class="btn">测试存储</button>
          <button @click="clearAllStorage" class="btn danger">清空所有存储</button>
        </div>
        <div v-if="testResult" class="test-result">
          {{ testResult }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default { 
  name: 'Home',
  data() {
    return {
      storageAvailable: false,
      testResult: ''
    }
  },
  mounted() {
    this.checkStorageAvailability()
  },
  methods: {
    checkStorageAvailability() {
      try {
        const test = '__storage_test__'
        sessionStorage.setItem(test, test)
        sessionStorage.removeItem(test)
        this.storageAvailable = true
      } catch (e) {
        this.storageAvailable = false
      }
    },
    testStorage() {
      try {
        const testKey = 'test_storage_' + Date.now()
        const testValue = 'test_value_' + Date.now()
        
        // 测试写入
        sessionStorage.setItem(testKey, testValue)
        
        // 测试读取
        const readValue = sessionStorage.getItem(testKey)
        
        // 测试删除
        sessionStorage.removeItem(testKey)
        
        if (readValue === testValue) {
          this.testResult = '✅ 存储测试成功：写入、读取、删除功能正常'
        } else {
          this.testResult = '❌ 存储测试失败：读取值与写入值不匹配'
        }
      } catch (e) {
        this.testResult = '❌ 存储测试失败：' + e.message
      }
    },
    clearAllStorage() {
      try {
        const keys = Object.keys(sessionStorage)
        const chatKeys = keys.filter(key => key.startsWith('chat_history:'))
        chatKeys.forEach(key => sessionStorage.removeItem(key))
        this.testResult = `✅ 已清空 ${chatKeys.length} 个聊天记录存储项`
      } catch (e) {
        this.testResult = '❌ 清空存储失败：' + e.message
      }
    }
  }
} 
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.hero-section {
  text-align: center;
  padding: 60px 0;
  margin-bottom: 60px;
}

.hero-content {
  animation: fadeIn 1s ease-out;
}

.hero-title {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 20px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.hero-icon {
  font-size: 56px;
  filter: drop-shadow(0 0 20px var(--primary-color));
  animation: pulse 2s infinite;
}

.hero-subtitle {
  font-size: 20px;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.section-title {
  font-size: 32px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 40px;
  color: var(--text-primary);
}

.apps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
  margin-bottom: 60px;
}

.app-card {
  background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
  border: 1px solid var(--border-color);
  border-radius: 20px;
  padding: 24px;
  text-decoration: none;
  color: var(--text-primary);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  gap: 20px;
}

.app-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.1), transparent);
  transition: left 0.5s;
}

.app-card:hover::before {
  left: 100%;
}

.app-card:hover {
  transform: translateY(-8px);
  border-color: var(--primary-color);
  box-shadow: 0 20px 40px rgba(0, 212, 255, 0.2);
}

.app-avatar {
  font-size: 48px;
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  box-shadow: 0 8px 20px rgba(0, 212, 255, 0.3);
  flex-shrink: 0;
}

.app-content {
  flex: 1;
}

.app-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.app-description {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 12px;
  line-height: 1.5;
}

.app-features {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.feature-tag {
  background: rgba(0, 212, 255, 0.1);
  color: var(--primary-color);
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  border: 1px solid rgba(0, 212, 255, 0.2);
}

.app-arrow {
  font-size: 24px;
  color: var(--primary-color);
  transition: transform 0.3s ease;
}

.app-card:hover .app-arrow {
  transform: translateX(8px);
}

.storage-section {
  margin-top: 60px;
}

.storage-card {
  background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
  border: 1px solid var(--border-color);
  border-radius: 20px;
  padding: 32px;
  max-width: 600px;
  margin: 0 auto;
}

.storage-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-primary);
}

.storage-icon {
  font-size: 28px;
  filter: drop-shadow(0 0 10px var(--primary-color));
}

.storage-status {
  margin-bottom: 24px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.status-label {
  color: var(--text-secondary);
  font-weight: 500;
}

.status-value {
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 6px;
}

.status-ok {
  color: var(--success-color);
  background: rgba(16, 185, 129, 0.1);
}

.status-error {
  color: var(--danger-color);
  background: rgba(239, 68, 68, 0.1);
}

.storage-description {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

.storage-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.btn.danger {
  background: linear-gradient(135deg, var(--danger-color), #dc2626);
}

.test-result {
  padding: 12px;
  background: rgba(0, 212, 255, 0.1);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 8px;
  font-size: 14px;
  color: var(--text-primary);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 36px;
  }
  
  .hero-icon {
    font-size: 44px;
  }
  
  .hero-subtitle {
    font-size: 18px;
  }
  
  .section-title {
    font-size: 28px;
  }
  
  .apps-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .app-card {
    padding: 20px;
    gap: 16px;
  }
  
  .app-avatar {
    width: 60px;
    height: 60px;
    font-size: 36px;
  }
  
  .app-title {
    font-size: 18px;
  }
  
  .storage-card {
    padding: 24px;
  }
}

@media (max-width: 480px) {
  .home {
    padding: 0 16px;
  }
  
  .hero-title {
    font-size: 28px;
    flex-direction: column;
    gap: 8px;
  }
  
  .hero-icon {
    font-size: 36px;
  }
  
  .hero-subtitle {
    font-size: 16px;
  }
  
  .app-card {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .app-avatar {
    width: 80px;
    height: 80px;
    font-size: 48px;
  }
  
  .storage-actions {
    flex-direction: column;
  }
}
</style>

