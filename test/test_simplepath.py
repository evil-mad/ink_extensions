#!/usr/bin/env python3
"""
Comprehensive test suite for simplepath module.
Tests all SVG path processing functions with various command combinations.
"""

import pytest
import sys

# Add the path to find ink_extensions
sys.path.insert(0, '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages')

from ink_extensions import simplepath, cubicsuperpath


class TestSimplePath:
    """Test suite for simplepath module functions"""

    def test_absolute_moveto_lineto(self):
        """Test absolute MoveTo (M) and LineTo (L) commands"""
        test_cases = [
            # Basic M and L
            "M 10,20 L 30,40",
            "M 0,0 L 100,100 L 200,50 L 150,150",
            
            # M with multiple coordinates (implicit L)
            "M 10,20 30,40 50,60",
            "M 0,0 25,25 50,50 75,75 100,100",
            
            # Mixed single and multiple coordinates
            "M 10,10 L 20,20 30,30 40,40 L 50,50"
        ]
        
        for path_d in test_cases:
            # Test that both parsePath functions produce identical results
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_relative_moveto_lineto(self):
        """Test relative moveto (m) and lineto (l) commands"""
        test_cases = [
            # Basic m and l
            "m 10,20 l 30,40",
            "m 0,0 l 10,10 l 20,0 l -5,15",
            
            # m with multiple coordinates (implicit l)
            "m 10,20 30,40 50,60",
            "m 50,50 10,10 10,10 10,10",
            
            # Mixed relative commands
            "m 10,10 l 20,20 30,30 l 40,40"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_horizontal_vertical_absolute(self):
        """Test absolute Horizontal (H) and Vertical (V) commands"""
        test_cases = [
            # Single H and V
            "M 10,10 H 50",
            "M 10,10 V 50", 
            "M 10,10 H 50 V 80",
            
            # Multiple H and V coordinates
            "M 0,0 H 10 20 30 40",
            "M 0,0 V 10 20 30 40",
            
            # Mixed H and V
            "M 10,10 H 50 V 80 H 100 V 120",
            "M 0,0 H 25 V 25 H 50 V 50 H 75 V 75"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_horizontal_vertical_relative(self):
        """Test relative horizontal (h) and vertical (v) commands"""
        test_cases = [
            # Single h and v
            "m 10,10 h 40",
            "m 10,10 v 40",
            "m 10,10 h 40 v 70",
            
            # Multiple h and v coordinates
            "m 0,0 h 10 20 30 40",
            "m 0,0 v 10 20 30 40",
            
            # Mixed h and v
            "m 10,10 h 40 v 70 h 50 v 30",
            "m 0,0 h 10 v 10 h 10 v 10 h 10 v 10"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_cubic_bezier_absolute(self):
        """Test absolute Cubic Bézier (C) commands"""
        test_cases = [
            # Single C command
            "M 10,10 C 20,20 30,0 40,10",
            "M 0,0 C 10,10 20,20 30,30",
            
            # Multiple C commands
            "M 0,0 C 10,10 20,20 30,30 C 40,40 50,50 60,60",
            "M 10,150 C 10,150 200,100 250,150 C 300,200 350,100 400,150",
            
            # Multiple coordinates in single C
            "M 0,0 C 10,10 20,20 30,30 40,40 50,50 60,60"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_cubic_bezier_relative(self):
        """Test relative cubic bézier (c) commands"""
        test_cases = [
            # Single c command
            "m 10,10 c 10,10 20,-10 30,0",
            "m 0,0 c 5,5 10,10 15,15",
            
            # Multiple c commands
            "m 0,0 c 10,10 20,20 30,30 c 10,10 20,20 30,30",
            "m 50,50 c 20,0 40,20 60,0 c 20,-20 40,0 60,20",
            
            # Multiple coordinates in single c
            "m 0,0 c 10,10 20,20 30,30 10,10 20,20 30,30"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_smooth_cubic_absolute(self):
        """Test absolute Smooth Cubic (S) commands"""
        test_cases = [
            # S after C
            "M 10,10 C 20,20 30,0 40,10 S 60,20 70,10",
            "M 0,0 C 10,10 20,20 30,30 S 50,50 60,60",
            
            # Multiple S commands
            "M 10,80 C 40,10 65,10 95,80 S 150,150 180,80 S 230,10 260,80",
            
            # S with multiple coordinates
            "M 0,0 C 10,10 20,20 30,30 S 50,50 60,60 70,70 80,80"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_smooth_cubic_relative(self):
        """Test relative smooth cubic (s) commands"""
        test_cases = [
            # s after c
            "m 10,10 c 10,10 20,-10 30,0 s 20,10 30,0",
            "m 0,0 c 10,10 20,20 30,30 s 20,20 30,30",
            
            # Multiple s commands
            "m 10,80 c 30,-70 55,-70 85,0 s 55,70 85,0 s 55,-70 85,0",
            
            # s with multiple coordinates
            "m 0,0 c 10,10 20,20 30,30 s 20,20 30,30 20,20 30,30"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_quadratic_bezier_absolute(self):
        """Test absolute Quadratic Bézier (Q) commands"""
        test_cases = [
            # Single Q command
            "M 10,10 Q 50,5 90,10",
            "M 0,0 Q 25,50 50,0",
            
            # Multiple Q commands
            "M 10,50 Q 25,25 40,50 Q 55,75 70,50",
            "M 0,0 Q 10,10 20,0 Q 30,20 40,0",
            
            # Multiple coordinates in single Q
            "M 0,0 Q 10,10 20,0 30,20 40,0"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_quadratic_bezier_relative(self):
        """Test relative quadratic bézier (q) commands"""
        test_cases = [
            # Single q command
            "m 10,10 q 40,-5 80,0",
            "m 0,0 q 25,50 50,0",
            
            # Multiple q commands
            "m 10,50 q 15,-25 30,0 q 15,25 30,0",
            "m 0,0 q 10,10 20,0 q 10,20 20,0",
            
            # Multiple coordinates in single q
            "m 0,0 q 10,10 20,0 10,20 20,0"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_smooth_quadratic_absolute(self):
        """Test absolute Smooth Quadratic (T) commands"""
        test_cases = [
            # T after Q
            "M 10,10 Q 50,5 90,10 T 170,10",
            "M 0,0 Q 25,50 50,0 T 100,0",
            
            # Multiple T commands
            "M 10,50 Q 25,25 40,50 T 70,50 T 100,50",
            "M 0,0 Q 10,10 20,0 T 40,0 T 60,0",
            
            # T with multiple coordinates
            "M 0,0 Q 10,10 20,0 T 40,0 60,0 80,0"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_smooth_quadratic_relative(self):
        """Test relative smooth quadratic (t) commands"""
        test_cases = [
            # t after q
            "m 10,10 q 40,-5 80,0 t 80,0",
            "m 0,0 q 25,50 50,0 t 50,0",
            
            # Multiple t commands
            "m 10,50 q 15,-25 30,0 t 30,0 t 30,0",
            "m 0,0 q 10,10 20,0 t 20,0 t 20,0",
            
            # t with multiple coordinates
            "m 0,0 q 10,10 20,0 t 20,0 20,0 20,0"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_elliptical_arc_absolute(self):
        """Test absolute Elliptical Arc (A) commands"""
        test_cases = [
            # Basic A command
            "M 10,10 A 5,5 0 0,1 20,20",
            "M 0,0 A 10,15 0 0,0 30,20",
            
            # Different sweep and large-arc flags
            "M 10,10 A 5,5 0 0,0 20,20",  # sweep-flag=0
            "M 10,10 A 5,5 0 1,1 20,20",  # large-arc-flag=1
            "M 10,10 A 5,5 0 1,0 20,20",  # large-arc-flag=1, sweep-flag=0
            
            # With rotation
            "M 10,10 A 5,5 45 0,1 20,20",
            "M 0,0 A 20,10 30 1,0 50,25",
            
            # Multiple A commands
            "M 10,10 A 5,5 0 0,1 20,20 A 5,5 0 0,1 30,10",
            
            # Multiple coordinates in single A
            "M 0,0 A 5,5 0 0,1 10,10 5,5 0 0,1 20,0"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_elliptical_arc_relative(self):
        """Test relative elliptical arc (a) commands"""
        test_cases = [
            # Basic a command
            "m 10,10 a 5,5 0 0,1 10,10",
            "m 0,0 a 10,15 0 0,0 30,20",
            
            # Different sweep and large-arc flags
            "m 10,10 a 5,5 0 0,0 10,10",  # sweep-flag=0
            "m 10,10 a 5,5 0 1,1 10,10",  # large-arc-flag=1
            "m 10,10 a 5,5 0 1,0 10,10",  # large-arc-flag=1, sweep-flag=0
            
            # With rotation
            "m 10,10 a 5,5 45 0,1 10,10",
            "m 0,0 a 20,10 30 1,0 50,25",
            
            # Multiple a commands
            "m 10,10 a 5,5 0 0,1 10,10 a 5,5 0 0,1 10,-10",
            
            # Multiple coordinates in single a
            "m 0,0 a 5,5 0 0,1 10,10 5,5 0 0,1 10,-10"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_closepath(self):
        """Test ClosePath (Z/z) commands"""
        test_cases = [
            # Basic Z
            "M 10,10 L 20,20 L 15,25 Z",
            "M 0,0 L 50,0 L 50,50 L 0,50 Z",
            
            # Basic z
            "m 10,10 l 10,10 l -5,5 z",
            "m 0,0 l 50,0 l 0,50 l -50,0 z",
            
            # Multiple subpaths with Z/z
            "M 10,10 L 20,20 Z M 30,30 L 40,40 Z",
            "m 10,10 l 10,10 z m 20,20 l 10,10 z",
            
            # Mixed absolute and relative with closepath
            "M 0,0 L 50,0 l 0,50 L 0,50 Z",
            "m 10,10 L 60,10 l 0,50 l -50,0 z"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_mixed_absolute_relative_commands(self):
        """Test combinations of absolute and relative commands"""
        test_cases = [
            # Mix M and l
            "M 10,10 l 20,20 L 50,50 l -10,-10",
            
            # Mix m and L
            "m 10,10 L 30,30 l 20,20 L 70,70",
            
            # Complex mixed curves
            "M 0,0 c 10,10 20,20 30,30 S 60,60 90,30 q 20,-20 40,0 T 170,30",
            
            # Mixed H/V with relative
            "M 10,10 H 50 v 40 H 90 V 10 h -20 v 20",
            
            # Arcs mixed with other commands
            "M 20,20 A 10,10 0 0,1 40,40 l 20,0 a 5,5 0 0,0 10,10 Z",
            
            # Complex real-world-like path
            "M 150,150 C 150,150 200,100 250,150 c 50,50 100,-50 150,0 L 450,200 l 50,50 Q 550,300 600,250 t 50,0 A 25,25 0 0,1 700,300 Z",
            
            # Subpaths with mixed commands
            "M 10,10 L 30,30 Z m 50,50 c 10,10 20,20 30,30 z M 100,100 H 150 V 150 h -50 z"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_edge_cases_and_special_values(self):
        """Test edge cases and special numeric values"""
        test_cases = [
            # Floating point numbers
            "M 10.5,20.75 L 30.25,40.125",
            
            # Scientific notation
            "M 1e2,2e-1 L 3.14e1,2.71e0",
            
            # Negative coordinates
            "M -10,-20 L -30,-40 C -50,-60 -70,-80 -90,-100",
            
            # Very small numbers
            "M 0.001,0.002 L 0.003,0.004",
            
            # Zero values
            "M 0,0 L 0,10 H 0 V 0",
            "M 10,10 l 0,0 h 0 v 0",
            
            # Large numbers
            "M 1000,2000 L 3000,4000",
            
            # Mixed positive/negative in curves
            "M 50,50 C -10,10 110,10 50,50 S -10,90 50,50",
            
            # Zero-radius arcs
            "M 10,10 A 0,0 0 0,1 10,10",
            "M 10,10 A 5,0 0 0,1 20,10",
            "M 10,10 A 0,5 0 0,1 10,20"
        ]
        
        for path_d in test_cases:
            result1 = simplepath.parsePath(path_d)
            result2 = simplepath.parsePath2(path_d)
            assert result1 == result2, f"parsePath mismatch for path: {path_d}"
    
    def test_parse_string_functions(self):
        """Test parse_string and parse_string2 functions"""
        test_cases = [
            # Every absolute command
            "M 10,20 L 30,40 H 50 V 60 C 70,80 90,100 110,120 S 130,140 150,160 Q 170,180 190,200 T 210,220 A 10,10 0 0,1 230,240 Z",
            
            # Every relative command  
            "m 10,20 l 30,40 h 50 v 60 c 70,80 90,100 110,120 s 130,140 150,160 q 170,180 190,200 t 210,220 a 10,10 0 0,1 230,240 z",
            
            # Mixed commands
            "M 0,0 l 10,10 H 20 v 10 C 30,40 40,50 50,60 s 10,10 20,20 Q 80,90 100,100 t 20,20 A 5,5 0 0,1 140,140 z"
        ]
        
        for path_d in test_cases:
            # Test parse_string functions produce equivalent results
            original_result = list(simplepath.parse_string(path_d))
            
            # Convert parse_string2 ASCII output to string commands for comparison
            string2_result = []
            for cmd_ascii, args in simplepath.parse_string2(path_d):
                cmd_str = chr(cmd_ascii)
                string2_result.append((cmd_str, args))
            
            assert original_result == string2_result, f"parse_string mismatch for path: {path_d}"
    
    def test_utility_functions(self):
        """Test utility functions with complex paths"""
        
        # Create a complex test path
        test_path = [
            ['M', [10.0, 20.0]],
            ['L', [30.0, 40.0]], 
            ['C', [50.0, 60.0, 70.0, 80.0, 90.0, 100.0]],
            ['Q', [110.0, 120.0, 130.0, 140.0]],
            ['A', [5.0, 5.0, 0.0, 0, 1, 150.0, 160.0]],
            ['Z', []]
        ]
        
        # Test formatPath
        formatted = simplepath.formatPath(test_path.copy())
        assert isinstance(formatted, str), "formatPath should return a string"
        assert 'M' in formatted and 'L' in formatted, "formatPath should contain path commands"
        
        # Test translatePath
        test_path_translate = [
            ['M', [10.0, 20.0]],
            ['L', [30.0, 40.0]], 
            ['C', [50.0, 60.0, 70.0, 80.0, 90.0, 100.0]]
        ]
        original_coords = [cmd[1][:] for cmd in test_path_translate]  # Deep copy coordinates
        
        simplepath.translatePath(test_path_translate, 15.5, -7.25)
        
        # Verify translation occurred
        for i, (cmd, params) in enumerate(test_path_translate):
            orig_params = original_coords[i]
            for j in range(0, len(params), 2):
                if j < len(orig_params):
                    assert abs(params[j] - (orig_params[j] + 15.5)) < 1e-10, "X coordinate should be translated"
                if j+1 < len(orig_params):
                    assert abs(params[j+1] - (orig_params[j+1] - 7.25)) < 1e-10, "Y coordinate should be translated"
        
        # Test scalePath
        test_path_scale = [
            ['M', [10.0, 20.0]],
            ['L', [30.0, 40.0]], 
            ['A', [5.0, 10.0, 30.0, 0, 1, 50.0, 60.0]]
        ]
        
        simplepath.scalePath(test_path_scale, 2.5, 1.5)
        
        # Verify scaling occurred (check first point)
        assert abs(test_path_scale[0][1][0] - 25.0) < 1e-10, "X coordinate should be scaled"
        assert abs(test_path_scale[0][1][1] - 30.0) < 1e-10, "Y coordinate should be scaled"
        
        # Test rotatePath
        test_path_rotate = [
            ['M', [10.0, 0.0]],  # Simple point for easy verification
            ['L', [20.0, 0.0]]
        ]
        
        result = simplepath.rotatePath(test_path_rotate, 1.5708, 0, 0)  # 90 degrees around origin
        
        # After 90 degree rotation, (10,0) should become approximately (0,10)
        rotated_x = test_path_rotate[0][1][0]
        rotated_y = test_path_rotate[0][1][1]
        assert abs(rotated_x - 0.0) < 1e-4, f"Rotated X should be ~0, got {rotated_x}"
        assert abs(rotated_y - 10.0) < 1e-4, f"Rotated Y should be ~10, got {rotated_y}"

    def test_cubicsuperpath_functions(self):
        """Test cubicsuperpath parsePath and parsePath2 functions"""
        test_cases = [
            "M 10,20 L 30,40 Z",
            "M 0,0 C 10,10 20,20 30,30 L 40,40",
            "M 0,0 Q 10,10 20,20",
        ]
        
        for path_d in test_cases:
            original_result = cubicsuperpath.parsePath(path_d)
            result2 = cubicsuperpath.parsePath2(path_d)
            
            assert original_result == result2, f"cubicsuperpath parsePath mismatch for path: {path_d}"


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])