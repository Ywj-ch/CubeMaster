/**
 * cubeMoves 模块测试
 * 
 * 测试魔方旋转逻辑的正确性
 */

import { describe, it, expect } from 'vitest'
import { SOLVED_STATE, cloneState, applyMove } from '../cubeMoves'

describe('cubeMoves', () => {
  describe('SOLVED_STATE', () => {
    it('should have 6 faces with 9 stickers each', () => {
      const faces = Object.keys(SOLVED_STATE.faces)
      expect(faces).toEqual(['U', 'D', 'F', 'B', 'L', 'R'])
      
      faces.forEach(face => {
        expect(SOLVED_STATE.faces[face]).toHaveLength(9)
      })
    })

    it('should have correct center colors', () => {
      expect(SOLVED_STATE.faces.U[4]).toBe('white')
      expect(SOLVED_STATE.faces.D[4]).toBe('yellow')
      expect(SOLVED_STATE.faces.F[4]).toBe('red')
      expect(SOLVED_STATE.faces.B[4]).toBe('orange')
      expect(SOLVED_STATE.faces.L[4]).toBe('blue')
      expect(SOLVED_STATE.faces.R[4]).toBe('green')
    })
  })

  describe('cloneState', () => {
    it('should create a deep copy of cube state', () => {
      const cloned = cloneState(SOLVED_STATE)
      
      // 引用不同
      expect(cloned).not.toBe(SOLVED_STATE)
      expect(cloned.faces).not.toBe(SOLVED_STATE.faces)
      
      // 值相同
      Object.keys(SOLVED_STATE.faces).forEach(face => {
        expect(cloned.faces[face]).toEqual(SOLVED_STATE.faces[face])
      })
    })

    it('should not affect original when modifying clone', () => {
      const cloned = cloneState(SOLVED_STATE)
      cloned.faces.U[0] = 'red'
      
      expect(SOLVED_STATE.faces.U[0]).toBe('white')
      expect(cloned.faces.U[0]).toBe('red')
    })
  })

  describe('applyMove', () => {
    it('should apply R move correctly', () => {
      const state = cloneState(SOLVED_STATE)
      applyMove(state, 'R')
      
      // 右面应该旋转（中心块不变）
      expect(state.faces.R[4]).toBe('green')
      
      // 相邻面应该变化
      expect(state.faces.U[2]).not.toBe('white')
      expect(state.faces.F[2]).not.toBe('red')
      expect(state.faces.D[2]).not.toBe('yellow')
      expect(state.faces.B[6]).not.toBe('orange')
    })

    it('should apply R prime move correctly', () => {
      const state = cloneState(SOLVED_STATE)
      applyMove(state, "R'")
      
      // 右面中心不变
      expect(state.faces.R[4]).toBe('green')
      
      // 相邻面变化方向与 R 相反
      expect(state.faces.U[8]).not.toBe('white')
    })

    it('should apply multiple moves in sequence', () => {
      const state = cloneState(SOLVED_STATE)
      applyMove(state, 'R')
      applyMove(state, 'U')
      applyMove(state, "R'")
      
      // 确保状态有效
      Object.keys(state.faces).forEach(face => {
        expect(state.faces[face]).toHaveLength(9)
      })
    })
  })
})
