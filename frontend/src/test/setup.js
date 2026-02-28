/**
 * Vitest 测试配置文件
 *
 * 用于设置全局测试环境、 mocks 和工具函数
 */

import { config } from "@vue/test-utils";

// 全局配置 Vue Test Utils
config.global.mocks = {
  $t: (key) => key, // i18n mock
};

// 全局提供 Vue 3 的 createApp 用于测试
globalThis.createApp = (await import("vue")).createApp;

// 禁用 Vue 警告（保持测试输出干净）
config.global.config.warnHandler = () => {};

// 打印测试配置信息
console.log("[Vitest] 测试环境初始化完成");
