// 测试后端服务连接
import http from 'http';

console.log('🔍 测试后端服务连接');
console.log('=' .repeat(50));

const testPorts = [8080, 3000, 8000, 5000, 4000];

async function testPort(port) {
  return new Promise((resolve) => {
    const req = http.request({
      hostname: 'localhost',
      port: port,
      path: '/api/health',
      method: 'GET',
      timeout: 5000
    }, (res) => {
      console.log(`✅ 端口 ${port}: 服务运行中 (状态码: ${res.statusCode})`);
      resolve({ port, status: 'running', statusCode: res.statusCode });
    });

    req.on('error', (err) => {
      if (err.code === 'ECONNREFUSED') {
        console.log(`❌ 端口 ${port}: 连接被拒绝 (服务未运行)`);
      } else {
        console.log(`❌ 端口 ${port}: 连接错误 - ${err.message}`);
      }
      resolve({ port, status: 'error', error: err.message });
    });

    req.on('timeout', () => {
      console.log(`⏰ 端口 ${port}: 请求超时`);
      req.destroy();
      resolve({ port, status: 'timeout' });
    });

    req.end();
  });
}

async function testAllPorts() {
  console.log('开始测试常用后端端口...\n');
  
  const results = [];
  for (const port of testPorts) {
    const result = await testPort(port);
    results.push(result);
    await new Promise(resolve => setTimeout(resolve, 1000)); // 延迟1秒
  }

  console.log('\n📊 测试结果总结:');
  console.log('=' .repeat(50));
  
  const runningPorts = results.filter(r => r.status === 'running');
  const errorPorts = results.filter(r => r.status === 'error');
  const timeoutPorts = results.filter(r => r.status === 'timeout');

  if (runningPorts.length > 0) {
    console.log(`✅ 发现运行中的服务: ${runningPorts.map(r => r.port).join(', ')}`);
  } else {
    console.log('❌ 未发现运行中的后端服务');
  }

  console.log(`❌ 连接失败: ${errorPorts.length} 个端口`);
  console.log(`⏰ 请求超时: ${timeoutPorts.length} 个端口`);

  console.log('\n💡 建议:');
  if (runningPorts.length === 0) {
    console.log('1. 启动本地后端服务');
    console.log('2. 或修改 Vite 代理配置指向正确的端口');
    console.log('3. 或使用远程后端服务');
  } else {
    console.log('1. 修改 Vite 代理配置指向发现的端口');
    console.log('2. 或使用环境变量配置正确的 API 地址');
  }
}

testAllPorts().catch(console.error);
