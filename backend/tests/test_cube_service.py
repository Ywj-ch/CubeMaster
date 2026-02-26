"""
CubeService 模块测试

测试魔方识别、状态保存和求解的业务逻辑
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys

# Mock 昂贵的依赖
mock_modules = {
    'twophase.solver': MagicMock(),
    'ultralytics': MagicMock(),
    'ultralytics.YOLO': MagicMock(),
    'cube_image_detection': MagicMock(),
}

for name, mock_obj in mock_modules.items():
    if name not in sys.modules:
        sys.modules[name] = mock_obj

from cube_service import recognize_cube, save_cube_state, get_detector


class TestCubeService:
    """CubeService 业务逻辑测试类"""

    @patch('cube_service.save_base64_images')
    @patch('cube_service.get_detector')
    def test_recognize_cube_success(self, mock_get_detector, mock_save_images):
        """测试魔方识别功能 - 正常情况"""
        # 准备测试数据
        test_images = {
            'U': 'base64_white',
            'D': 'base64_yellow',
            'F': 'base64_green',
            'B': 'base64_blue',
            'L': 'base64_orange',
            'R': 'base64_red'
        }
        
        # Mock 检测器返回
        mock_detector = Mock()
        expected_state = [['R'] * 9, ['U'] * 9, ['F'] * 9, ['B'] * 9, ['L'] * 9, ['D'] * 9]
        mock_detector.detect_all_faces.return_value = expected_state
        mock_get_detector.return_value = mock_detector
        
        # 执行测试
        result = recognize_cube(test_images)
        
        # 验证结果
        assert result == expected_state
        mock_save_images.assert_called_once_with(test_images, output_dir='images')
        mock_detector.detect_all_faces.assert_called_once()

    def test_recognize_cube_empty_input(self):
        """测试魔方识别功能 - 空输入"""
        with pytest.raises(ValueError) as exc_info:
            recognize_cube({})
        
        assert "未接收到图片数据" in str(exc_info.value)

    @patch('cube_service.get_detector')
    def test_save_cube_state_success(self, mock_get_detector):
        """测试保存魔方状态 - 正常情况"""
        test_state = {
            'faces': {
                'U': ['white'] * 9,
                'D': ['yellow'] * 9,
                'F': ['red'] * 9,
                'B': ['orange'] * 9,
                'L': ['blue'] * 9,
                'R': ['green'] * 9
            }
        }
        
        mock_detector = Mock()
        mock_get_detector.return_value = mock_detector
        
        # 执行测试
        save_cube_state(test_state)
        
        # 验证调用
        mock_detector.save_cube_state_json.assert_called_once_with(test_state)

    def test_save_cube_state_empty_input(self):
        """测试保存魔方状态 - 空输入"""
        with pytest.raises(ValueError) as exc_info:
            save_cube_state({})
        
        assert "状态数据为空" in str(exc_info.value)

    def test_save_cube_state_none_input(self):
        """测试保存魔方状态 - None 输入"""
        with pytest.raises(ValueError) as exc_info:
            save_cube_state(None)
        
        assert "状态数据为空" in str(exc_info.value)

    @patch('cube_service.CubeDetector')
    def test_get_detector_singleton(self, mock_cube_detector_class):
        """测试检测器单例模式"""
        # 重置全局变量
        import cube_service
        cube_service._detector_instance = None
        
        mock_detector_instance = Mock()
        mock_cube_detector_class.return_value = mock_detector_instance
        
        # 第一次调用应该创建新实例
        detector1 = get_detector()
        assert mock_cube_detector_class.assert_called_once
        assert mock_cube_detector_class.call_count == 1
        
        # 第二次调用应该返回同一实例
        detector2 = get_detector()
        assert detector1 is detector2
        assert mock_cube_detector_class.call_count == 1


class TestRecognizeCubeIntegration:
    """识别功能集成测试"""

    @patch('cube_service.save_base64_images')
    @patch('cube_service.get_detector')
    def test_recognize_cube_with_invalid_face_key(self, mock_get_detector, mock_save_images):
        """测试包含无效面名的识别请求"""
        test_images = {
            'U': 'base64_white',
            'X': 'base64_invalid',  # 无效的面名
        }
        
        mock_detector = Mock()
        mock_detector.detect_all_faces.return_value = [['R'] * 9] * 6
        mock_get_detector.return_value = mock_detector
        
        # 应该不会抛出异常，但会保存图片
        result = recognize_cube(test_images)
        
        assert len(result) == 6
        mock_save_images.assert_called_once()
