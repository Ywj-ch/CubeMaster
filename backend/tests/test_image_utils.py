"""
Image Utils 模块测试

测试 Base64 图片处理和保存功能
"""

import pytest
import os
import base64
from unittest.mock import patch, MagicMock
import numpy as np
import cv2

# 导入被测试函数
from image_utils import (
    _safe_base64_decode,
    _resize_keep_ratio,
    save_base64_images,
    FACE_TO_FILENAME
)


def create_test_image_base64(color='red'):
    """创建测试用的 base64 图片字符串"""
    if color == 'red':
        img_data = np.zeros((10, 10, 3), dtype=np.uint8)
        img_data[:, :] = [0, 0, 255]
    elif color == 'white':
        img_data = np.zeros((10, 10, 3), dtype=np.uint8)
        img_data[:, :] = [255, 255, 255]
    else:
        img_data = np.zeros((10, 10, 3), dtype=np.uint8)
    
    _, buffer = cv2.imencode('.png', img_data)
    return base64.b64encode(buffer).decode('utf-8')


class TestSafeBase64Decode:
    """_safe_base64_decode 函数测试"""

    def test_decode_plain_base64(self):
        """测试解码纯 base64 字符串"""
        test_data = b"hello world"
        base64_str = base64.b64encode(test_data).decode('utf-8')
        
        result = _safe_base64_decode(base64_str)
        
        assert result == test_data

    def test_decode_with_data_uri(self):
        """测试解码带 data:image 前缀的 base64"""
        test_data = b"test image data"
        base64_str = "data:image/png;base64," + base64.b64encode(test_data).decode('utf-8')
        
        result = _safe_base64_decode(base64_str)
        
        assert result == test_data

    def test_decode_invalid_base64(self):
        """测试解码无效 base64 字符串"""
        result = _safe_base64_decode("invalid!!!base64")
        
        assert result is None

    def test_decode_empty_string(self):
        """测试解码空字符串"""
        result = _safe_base64_decode("")
        
        # 空字符串会返回空字节
        assert result == b''


class TestResizeKeepRatio:
    """_resize_keep_ratio 函数测试"""

    def test_resize_large_image(self):
        """测试缩放超过最大尺寸的图片"""
        img = np.zeros((1000, 800, 3), dtype=np.uint8)
        
        result = _resize_keep_ratio(img, 640)
        
        assert max(result.shape[:2]) <= 640
        assert result.shape[0] / result.shape[1] == pytest.approx(1000 / 800, rel=0.01)

    def test_no_resize_small_image(self):
        """测试不缩放小于最大尺寸的图片"""
        img = np.zeros((100, 80, 3), dtype=np.uint8)
        
        result = _resize_keep_ratio(img, 640)
        
        assert result.shape == (100, 80, 3)

    def test_resize_square_image(self):
        """测试缩放正方形图片"""
        img = np.zeros((1000, 1000, 3), dtype=np.uint8)
        
        result = _resize_keep_ratio(img, 640)
        
        assert result.shape == (640, 640, 3)


class TestSaveBase64Images:
    """save_base64_images 函数测试"""

    @patch('image_utils.cv2.imwrite')
    def test_save_single_image(self, mock_imwrite):
        """测试保存单张图片"""
        base64_str = create_test_image_base64('red')
        images_dict = {'U': base64_str}
        
        mock_imwrite.return_value = True
        
        result = save_base64_images(images_dict, output_dir='test_images')
        
        assert 'U' in result
        assert result['U'] == True
        mock_imwrite.assert_called()

    @patch('image_utils.cv2.imwrite')
    def test_save_multiple_images(self, mock_imwrite):
        """测试保存多张图片"""
        images_dict = {
            'U': create_test_image_base64('white'),
            'F': create_test_image_base64('red'),
            'R': create_test_image_base64('green'),
        }
        
        mock_imwrite.return_value = True
        
        result = save_base64_images(images_dict, output_dir='test_images')
        
        assert len(result) == 3
        assert all(result.values())

    @patch('image_utils.cv2.imwrite')
    def test_save_with_invalid_face_key(self, mock_imwrite):
        """测试保存时包含无效面名"""
        images_dict = {
            'U': create_test_image_base64('white'),
            'X': create_test_image_base64('red'),
        }
        
        result = save_base64_images(images_dict, output_dir='test_images')
        
        assert 'U' in result
        assert 'X' not in result

    def test_save_with_invalid_base64(self):
        """测试保存时无效的 base64 数据"""
        images_dict = {
            'U': 'invalid_base64_data!!!',
        }
        
        result = save_base64_images(images_dict, output_dir='test_images')
        
        assert 'U' in result
        assert result['U'] == False

    @patch('image_utils.os.makedirs')
    def test_creates_output_directory(self, mock_makedirs):
        """测试自动创建输出目录"""
        images_dict = {'U': create_test_image_base64('white')}
        
        with patch('image_utils.cv2.imwrite', return_value=True):
            save_base64_images(images_dict, output_dir='new_dir')
        
        mock_makedirs.assert_called_once_with('new_dir', exist_ok=True)


class TestFaceToFilenameMapping:
    """面名到文件名映射测试"""

    def test_all_faces_mapped(self):
        """测试所有标准面名都有映射"""
        expected_faces = ['U', 'R', 'F', 'D', 'L', 'B']
        
        for face in expected_faces:
            assert face in FACE_TO_FILENAME

    def test_mapping_values(self):
        """测试映射值正确"""
        assert FACE_TO_FILENAME['U'] == 'white'
        assert FACE_TO_FILENAME['D'] == 'yellow'
        assert FACE_TO_FILENAME['F'] == 'green'
        assert FACE_TO_FILENAME['B'] == 'blue'
        assert FACE_TO_FILENAME['L'] == 'orange'
        assert FACE_TO_FILENAME['R'] == 'red'
