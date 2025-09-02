<template>
  <div class="home">
    <!-- 背景动画 -->
    <div class="background-animation">
      <div class="grid-lines"></div>
      <div class="floating-particles"></div>
    </div>
    
    <div class="container">
      <div class="header-section fade-in-up">
        <h1 class="title">
          <span class="title-main">AI智能体应用</span>
          <span class="title-sub">Artificial Intelligence Agent Platform</span>
        </h1>
        <p class="subtitle">选择您想要使用的AI应用，开启智能对话新时代</p>
      </div>
      
      <div class="app-grid">
        <div class="app-card tech-card" @click="navigateTo('/love-app-chat')">
          <div class="card-header">
            <div class="app-icon">🤖</div>
            <div class="app-badge">PCIE</div>
          </div>
          <h3>AI PCIE技术应用</h3>
          <p>基于PCIE技术的智能对话系统，提供专业的技术咨询服务，支持实时流式响应</p>
          <div class="app-features">
            <span class="feature-tag">实时对话</span>
            <span class="feature-tag">技术咨询</span>
            <span class="feature-tag">PCIE专业</span>
          </div>
          <div class="card-footer">
            <span class="enter-text">点击进入 →</span>
          </div>
        </div>
        
        <div class="app-card tech-card" @click="navigateTo('/manus-chat')">
          <div class="card-header">
            <div class="app-icon">🧠</div>
            <div class="app-badge">AI</div>
          </div>
          <h3>AI 超级智能体</h3>
          <p>多功能智能体系统，能够处理各种复杂任务和问题，提供全方位的智能服务</p>
          <div class="app-features">
            <span class="feature-tag">智能对话</span>
            <span class="feature-tag">多任务处理</span>
            <span class="feature-tag">超级智能</span>
          </div>
          <div class="card-footer">
            <span class="enter-text">点击进入 →</span>
          </div>
        </div>
      </div>
      
      <div class="footer-section fade-in-up">
        <div class="tech-info">
          <div class="info-item">
            <span class="info-icon">⚡</span>
            <span>实时SSE通信</span>
          </div>
          <div class="info-item">
            <span class="info-icon">🔒</span>
            <span>安全可靠</span>
          </div>
          <div class="info-item">
            <span class="info-icon">📱</span>
            <span>全平台兼容</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateTo = (path) => {
  router.push(path)
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: var(--bg-primary);
  position: relative;
  overflow: hidden;
}

.background-animation {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.grid-lines {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(rgba(0, 212, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 212, 255, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridMove 20s linear infinite;
}

.floating-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.floating-particles::before,
.floating-particles::after {
  content: '';
  position: absolute;
  width: 4px;
  height: 4px;
  background: var(--primary-color);
  border-radius: 50%;
  box-shadow: var(--glow-primary);
  animation: float 6s ease-in-out infinite;
}

.floating-particles::before {
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.floating-particles::after {
  top: 60%;
  right: 15%;
  animation-delay: 3s;
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

@keyframes float {
  0%, 100% { transform: translateY(0px) scale(1); opacity: 0.8; }
  50% { transform: translateY(-20px) scale(1.2); opacity: 1; }
}

.container {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.header-section {
  margin-bottom: 60px;
}

.title {
  margin-bottom: 20px;
}

.title-main {
  display: block;
  font-size: clamp(2.5rem, 8vw, 4rem);
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
  margin-bottom: 10px;
}

.title-sub {
  display: block;
  font-size: clamp(1rem, 3vw, 1.2rem);
  color: var(--text-secondary);
  font-weight: 300;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.subtitle {
  font-size: clamp(1.1rem, 3vw, 1.3rem);
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.app-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 40px;
  margin: 60px 0;
}

.app-card {
  cursor: pointer;
  text-align: left;
  position: relative;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  padding: 32px;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  overflow: hidden;
}

.app-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.app-card:hover::before {
  opacity: 1;
}

.app-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  border-color: var(--primary-color);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.app-icon {
  font-size: 3rem;
  filter: drop-shadow(0 0 10px rgba(0, 212, 255, 0.5));
}

.app-badge {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: var(--glow-primary);
}

.app-card h3 {
  font-size: 1.8rem;
  color: var(--text-primary);
  margin-bottom: 16px;
  font-weight: 600;
}

.app-card p {
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 24px;
  font-size: 1rem;
}

.app-features {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 24px;
}

.feature-tag {
  background: rgba(0, 212, 255, 0.1);
  color: var(--primary-color);
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid rgba(0, 212, 255, 0.3);
  transition: all 0.3s ease;
}

.app-card:hover .feature-tag {
  background: rgba(0, 212, 255, 0.2);
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

.card-footer {
  text-align: right;
}

.enter-text {
  color: var(--primary-color);
  font-size: 0.9rem;
  font-weight: 500;
  opacity: 0.8;
  transition: all 0.3s ease;
}

.app-card:hover .enter-text {
  opacity: 1;
  transform: translateX(5px);
}

.footer-section {
  margin-top: 80px;
}

.tech-info {
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.info-icon {
  font-size: 1.2rem;
  filter: drop-shadow(0 0 8px rgba(0, 212, 255, 0.5));
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container {
    padding: 20px 15px;
  }
  
  .app-grid {
    grid-template-columns: 1fr;
    gap: 30px;
    margin: 40px 0;
  }
  
  .app-card {
    padding: 24px;
  }
  
  .tech-info {
    flex-direction: column;
    gap: 20px;
  }
  
  .header-section {
    margin-bottom: 40px;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .app-grid {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
  }
  
  .container {
    padding: 30px 25px;
  }
}

@media (min-width: 1025px) {
  .app-grid {
    grid-template-columns: repeat(2, 1fr);
    max-width: 1000px;
    margin: 60px auto;
  }
}

/* 动画延迟 */
.app-card:nth-child(1) {
  animation-delay: 0.1s;
}

.app-card:nth-child(2) {
  animation-delay: 0.2s;
}

.footer-section {
  animation-delay: 0.3s;
}
</style>
