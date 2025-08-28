import axios from 'axios'
import { config } from '../config/env.js'

export const apiClient = axios.create({
  baseURL: config.api.baseURL,
  timeout: 30000
})

export function generateChatId() {
  const t = Date.now().toString(36)
  const r = Math.random().toString(36).slice(2, 8)
  return `chat_${t}_${r}`
}

export function eventSourceUrl(path, params) {
  const q = new URLSearchParams(params)
  const sep = path.includes('?') ? '&' : '?'
  return `${apiClient.defaults.baseURL}${path}${sep}${q.toString()}`
}

// 本地持久化：按命名空间保存聊天记录
const STORAGE_KEY_PREFIX = 'chat_history:'

function storageKey(namespace) {
  return STORAGE_KEY_PREFIX + namespace
}

const MAX_PAIRS = 10
const SAVE_DEBOUNCE_MS = 150
const namespaceToTimerId = new Map()

export function loadMessages(namespace, options = {}) {
  try {
    const raw = sessionStorage.getItem(storageKey(namespace))
    const parsed = raw ? JSON.parse(raw) : []
    const limit = Number.isFinite(options.maxPairs) ? options.maxPairs : MAX_PAIRS
    return clampToLastPairs(parsed, limit)
  } catch (_) {
    return []
  }
}

export function saveMessages(namespace, messages, options = {}) {
  try {
    const list = Array.isArray(messages) ? messages : []
    const limit = Number.isFinite(options.maxPairs) ? options.maxPairs : MAX_PAIRS
    const trimmed = clampToLastPairs(list, limit)
    sessionStorage.setItem(storageKey(namespace), JSON.stringify(trimmed))
  } catch (_) {
    // ignore
  }
}

// 防抖保存，减少 SSE 流式更新导致的频繁写入
export function saveMessagesDebounced(namespace, messages, options = {}) {
  try {
    if (namespaceToTimerId.has(namespace)) {
      clearTimeout(namespaceToTimerId.get(namespace))
    }
    const timerId = setTimeout(() => {
      try { saveMessages(namespace, messages, options) } catch (_) {}
      namespaceToTimerId.delete(namespace)
    }, SAVE_DEBOUNCE_MS)
    namespaceToTimerId.set(namespace, timerId)
  } catch (_) {
    // ignore
  }
}

export function clearMessages(namespace) {
  try {
    if (namespaceToTimerId.has(namespace)) {
      clearTimeout(namespaceToTimerId.get(namespace))
      namespaceToTimerId.delete(namespace)
    }
    sessionStorage.removeItem(storageKey(namespace))
  } catch (_) {
    // ignore
  }
}

// 保留最后 N 组（问题+回答）
function clampToLastPairs(messages, maxPairs) {
  if (!Array.isArray(messages) || messages.length === 0) return []
  const kept = []
  let pairs = 0
  for (let i = messages.length - 1; i >= 0; i--) {
    kept.push(messages[i])
    if (messages[i].role === 'user') {
      pairs++
      if (pairs >= maxPairs) break
    }
  }
  return kept.reverse()
}

