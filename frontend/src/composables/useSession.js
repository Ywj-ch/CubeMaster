/**
 * @fileoverview 会话管理 Composable
 *
 * 管理用户会话 ID，确保多用户并发访问时文件存储隔离。
 * 前端生成 UUID 作为 session_id，随请求发送到后端。
 *
 * @module composables/useSession
 */

import { ref } from "vue";
import { createSession, closeSession } from "../api/cubeService.js";

const sessionId = ref(null);
let createPromise = null;

/**
 * 获取当前会话 ID，如不存在则自动创建
 *
 * @returns {Promise<string>} 会话 ID
 */
export function useSession() {
  const ensureSession = async () => {
    if (sessionId.value) {
      return sessionId.value;
    }

    if (createPromise) {
      return createPromise;
    }

    createPromise = (async () => {
      try {
        const res = await createSession();
        if (res.data && res.data.success) {
          sessionId.value = res.data.session_id;
          return sessionId.value;
        }
        throw new Error(res.data?.error || "创建会话失败");
      } catch (err) {
        console.error("[Session] 创建会话失败:", err);
        throw err;
      } finally {
        createPromise = null;
    }
    })();

    return createPromise;
  };

  /**
   * 销毁当前会话，清理服务端文件
   */
  const destroySession = async () => {
    if (!sessionId.value) return;

    try {
      await closeSession(sessionId.value);
    } catch (err) {
      console.warn("[Session] 销毁会话失败:", err);
    } finally {
      sessionId.value = null;
      createPromise = null;
    }
  };

  /**
   * 重置会话（销毁旧会话并创建新会话）
   *
   * @returns {Promise<string>} 新的会话 ID
   */
  const resetSession = async () => {
    await destroySession();
    return ensureSession();
  };

  return {
    sessionId,
    ensureSession,
    destroySession,
    resetSession,
  };
}