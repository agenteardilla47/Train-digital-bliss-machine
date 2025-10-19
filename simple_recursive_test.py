#!/usr/bin/env python3
"""
Simplified Recursive Function Test Suite

This script implements various recursive functions and tests them 33 times
to evaluate performance, correctness, and resource usage patterns.
"""

import time
import sys
import traceback
import psutil
import os
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import json
import numpy as np


@dataclass
class TestResult:
    """Result of a single test execution"""
    test_id: int
    function_name: str
    execution_time: float
    memory_usage: float
    success: bool
    error_message: str = ""
    return_value: Any = None
    recursion_depth: int = 0
    stack_usage: int = 0


class RecursiveTestSuite:
    """Comprehensive test suite for recursive functions"""
    
    def __init__(self):
        self.results: List[TestResult] = []
        self.test_count = 33
        self.max_recursion_depth = 1000
        
    def fibonacci_recursive(self, n: int) -> int:
        """Classic recursive Fibonacci implementation"""
        if n <= 1:
            return n
        return self.fibonacci_recursive(n - 1) + self.fibonacci_recursive(n - 2)
    
    def factorial_recursive(self, n: int) -> int:
        """Recursive factorial implementation"""
        if n <= 1:
            return 1
        return n * self.factorial_recursive(n - 1)
    
    def binary_search_recursive(self, arr: List[int], target: int, left: int = 0, right: int = None) -> int:
        """Recursive binary search implementation"""
        if right is None:
            right = len(arr) - 1
        
        if left > right:
            return -1
        
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            return self.binary_search_recursive(arr, target, left, mid - 1)
        else:
            return self.binary_search_recursive(arr, target, mid + 1, right)
    
    def tree_traversal_recursive(self, node: Dict[str, Any], depth: int = 0) -> List[Any]:
        """Recursive tree traversal implementation"""
        if depth > self.max_recursion_depth:
            return []
        
        result = [node.get('value', None)]
        
        for child in node.get('children', []):
            result.extend(self.tree_traversal_recursive(child, depth + 1))
        
        return result
    
    def merge_sort_recursive(self, arr: List[int]) -> List[int]:
        """Recursive merge sort implementation"""
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = self.merge_sort_recursive(arr[:mid])
        right = self.merge_sort_recursive(arr[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        """Helper function for merge sort"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def tower_of_hanoi_recursive(self, n: int, source: str, destination: str, auxiliary: str) -> List[str]:
        """Recursive Tower of Hanoi implementation"""
        if n == 1:
            return [f"Move disk 1 from {source} to {destination}"]
        
        moves = []
        moves.extend(self.tower_of_hanoi_recursive(n - 1, source, auxiliary, destination))
        moves.append(f"Move disk {n} from {source} to {destination}")
        moves.extend(self.tower_of_hanoi_recursive(n - 1, auxiliary, destination, source))
        
        return moves
    
    def quicksort_recursive(self, arr: List[int]) -> List[int]:
        """Recursive quicksort implementation"""
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return (self.quicksort_recursive(left) + 
                middle + 
                self.quicksort_recursive(right))
    
    def depth_first_search_recursive(self, graph: Dict[int, List[int]], 
                                   start: int, 
                                   visited: set = None) -> List[int]:
        """Recursive depth-first search implementation"""
        if visited is None:
            visited = set()
        
        if start in visited:
            return []
        
        visited.add(start)
        result = [start]
        
        for neighbor in graph.get(start, []):
            result.extend(self.depth_first_search_recursive(graph, neighbor, visited))
        
        return result
    
    def calculate_recursion_depth(self, func, *args, **kwargs) -> int:
        """Calculate the maximum recursion depth reached"""
        original_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(self.max_recursion_depth)
        
        try:
            # Use a wrapper to track recursion depth
            depth = [0]
            max_depth = [0]
            
            def depth_tracker(*args, **kwargs):
                depth[0] += 1
                max_depth[0] = max(max_depth[0], depth[0])
                try:
                    return func(*args, **kwargs)
                finally:
                    depth[0] -= 1
            
            depth_tracker(*args, **kwargs)
            return max_depth[0]
        finally:
            sys.setrecursionlimit(original_limit)
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    
    def run_single_test(self, test_id: int, func, func_name: str, *args, **kwargs) -> TestResult:
        """Run a single test and collect metrics"""
        start_time = time.time()
        start_memory = self.get_memory_usage()
        
        try:
            # Calculate recursion depth
            recursion_depth = self.calculate_recursion_depth(func, *args, **kwargs)
            
            # Run the actual function
            start_time = time.time()
            return_value = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            end_memory = self.get_memory_usage()
            memory_usage = end_memory - start_memory
            
            return TestResult(
                test_id=test_id,
                function_name=func_name,
                execution_time=execution_time,
                memory_usage=memory_usage,
                success=True,
                return_value=return_value,
                recursion_depth=recursion_depth,
                stack_usage=sys.getrecursionlimit()
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            end_memory = self.get_memory_usage()
            memory_usage = end_memory - start_memory
            
            return TestResult(
                test_id=test_id,
                function_name=func_name,
                execution_time=execution_time,
                memory_usage=memory_usage,
                success=False,
                error_message=str(e),
                recursion_depth=0,
                stack_usage=sys.getrecursionlimit()
            )
    
    def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run all recursive function tests 33 times each"""
        print("🚀 Starting Comprehensive Recursive Function Test Suite")
        print("=" * 60)
        
        test_functions = [
            ("fibonacci", self.fibonacci_recursive, [10]),
            ("factorial", self.factorial_recursive, [15]),
            ("binary_search", self.binary_search_recursive, [list(range(1000)), 500]),
            ("tree_traversal", self.tree_traversal_recursive, [{"value": 1, "children": [{"value": 2, "children": []}, {"value": 3, "children": []}]}]),
            ("merge_sort", self.merge_sort_recursive, [list(np.random.randint(0, 100, 50))]),
            ("tower_of_hanoi", self.tower_of_hanoi_recursive, [4, "A", "C", "B"]),
            ("quicksort", self.quicksort_recursive, [list(np.random.randint(0, 100, 50))]),
            ("dfs", self.depth_first_search_recursive, [{0: [1, 2], 1: [3, 4], 2: [5], 3: [], 4: [], 5: []}, 0])
        ]
        
        all_results = []
        
        for func_name, func, args in test_functions:
            print(f"\n📊 Testing {func_name} function {self.test_count} times...")
            function_results = []
            
            for i in range(self.test_count):
                result = self.run_single_test(i + 1, func, func_name, *args)
                function_results.append(result)
                all_results.append(result)
                
                if not result.success:
                    print(f"   ❌ Test {i + 1} failed: {result.error_message}")
                elif i % 5 == 0:  # Progress indicator
                    print(f"   ✅ Test {i + 1} completed in {result.execution_time:.4f}s")
            
            # Calculate statistics for this function
            successful_tests = [r for r in function_results if r.success]
            if successful_tests:
                avg_time = sum(r.execution_time for r in successful_tests) / len(successful_tests)
                avg_memory = sum(r.memory_usage for r in successful_tests) / len(successful_tests)
                max_depth = max(r.recursion_depth for r in successful_tests)
                success_rate = len(successful_tests) / len(function_results) * 100
                
                print(f"   📈 {func_name} Statistics:")
                print(f"      • Success Rate: {success_rate:.1f}%")
                print(f"      • Average Time: {avg_time:.4f}s")
                print(f"      • Average Memory: {avg_memory:.2f}MB")
                print(f"      • Max Recursion Depth: {max_depth}")
        
        return self._analyze_results(all_results)
    
    def _analyze_results(self, results: List[TestResult]) -> Dict[str, Any]:
        """Analyze test results and generate comprehensive report"""
        successful_tests = [r for r in results if r.success]
        failed_tests = [r for r in results if not r.success]
        
        analysis = {
            "total_tests": len(results),
            "successful_tests": len(successful_tests),
            "failed_tests": len(failed_tests),
            "success_rate": len(successful_tests) / len(results) * 100 if results else 0,
            "performance_metrics": {},
            "function_breakdown": {},
            "error_analysis": {},
            "recommendations": []
        }
        
        if successful_tests:
            analysis["performance_metrics"] = {
                "average_execution_time": sum(r.execution_time for r in successful_tests) / len(successful_tests),
                "max_execution_time": max(r.execution_time for r in successful_tests),
                "min_execution_time": min(r.execution_time for r in successful_tests),
                "average_memory_usage": sum(r.memory_usage for r in successful_tests) / len(successful_tests),
                "max_memory_usage": max(r.memory_usage for r in successful_tests),
                "average_recursion_depth": sum(r.recursion_depth for r in successful_tests) / len(successful_tests),
                "max_recursion_depth": max(r.recursion_depth for r in successful_tests)
            }
        
        # Function-specific analysis
        function_groups = {}
        for result in results:
            if result.function_name not in function_groups:
                function_groups[result.function_name] = []
            function_groups[result.function_name].append(result)
        
        for func_name, func_results in function_groups.items():
            successful_func_tests = [r for r in func_results if r.success]
            analysis["function_breakdown"][func_name] = {
                "total_tests": len(func_results),
                "successful_tests": len(successful_func_tests),
                "success_rate": len(successful_func_tests) / len(func_results) * 100 if func_results else 0,
                "average_time": sum(r.execution_time for r in successful_func_tests) / len(successful_func_tests) if successful_func_tests else 0,
                "average_memory": sum(r.memory_usage for r in successful_func_tests) / len(successful_func_tests) if successful_func_tests else 0,
                "max_recursion_depth": max(r.recursion_depth for r in successful_func_tests) if successful_func_tests else 0
            }
        
        # Error analysis
        error_types = {}
        for result in failed_tests:
            error_type = type(result.error_message).__name__
            if error_type not in error_types:
                error_types[error_type] = 0
            error_types[error_type] += 1
        
        analysis["error_analysis"] = error_types
        
        # Generate recommendations
        if analysis["success_rate"] < 100:
            analysis["recommendations"].append("Some tests failed - investigate error patterns")
        
        if successful_tests:
            avg_time = analysis["performance_metrics"]["average_execution_time"]
            if avg_time > 1.0:
                analysis["recommendations"].append("Consider optimizing slow recursive functions")
            
            max_depth = analysis["performance_metrics"]["max_recursion_depth"]
            if max_depth > 100:
                analysis["recommendations"].append("High recursion depth detected - consider iterative alternatives")
        
        return analysis
    
    def generate_report(self, analysis: Dict[str, Any]) -> str:
        """Generate a comprehensive test report"""
        report = []
        report.append("🔬 COMPREHENSIVE RECURSIVE FUNCTION TEST REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Summary
        report.append("📊 SUMMARY")
        report.append("-" * 20)
        report.append(f"Total Tests Executed: {analysis['total_tests']}")
        report.append(f"Successful Tests: {analysis['successful_tests']}")
        report.append(f"Failed Tests: {analysis['failed_tests']}")
        report.append(f"Success Rate: {analysis['success_rate']:.2f}%")
        report.append("")
        
        # Performance Metrics
        if analysis["performance_metrics"]:
            report.append("⚡ PERFORMANCE METRICS")
            report.append("-" * 25)
            metrics = analysis["performance_metrics"]
            report.append(f"Average Execution Time: {metrics['average_execution_time']:.4f}s")
            report.append(f"Max Execution Time: {metrics['max_execution_time']:.4f}s")
            report.append(f"Min Execution Time: {metrics['min_execution_time']:.4f}s")
            report.append(f"Average Memory Usage: {metrics['average_memory_usage']:.2f}MB")
            report.append(f"Max Memory Usage: {metrics['max_memory_usage']:.2f}MB")
            report.append(f"Average Recursion Depth: {metrics['average_recursion_depth']:.1f}")
            report.append(f"Max Recursion Depth: {metrics['max_recursion_depth']}")
            report.append("")
        
        # Function Breakdown
        report.append("🔧 FUNCTION BREAKDOWN")
        report.append("-" * 20)
        for func_name, func_data in analysis["function_breakdown"].items():
            report.append(f"\n{func_name.upper()}:")
            report.append(f"  Success Rate: {func_data['success_rate']:.1f}%")
            report.append(f"  Average Time: {func_data['average_time']:.4f}s")
            report.append(f"  Average Memory: {func_data['average_memory']:.2f}MB")
            report.append(f"  Max Recursion Depth: {func_data['max_recursion_depth']}")
        
        # Error Analysis
        if analysis["error_analysis"]:
            report.append("\n❌ ERROR ANALYSIS")
            report.append("-" * 15)
            for error_type, count in analysis["error_analysis"].items():
                report.append(f"{error_type}: {count} occurrences")
        
        # Recommendations
        if analysis["recommendations"]:
            report.append("\n💡 RECOMMENDATIONS")
            report.append("-" * 15)
            for i, rec in enumerate(analysis["recommendations"], 1):
                report.append(f"{i}. {rec}")
        
        report.append("\n" + "=" * 60)
        report.append("Test completed successfully!")
        
        return "\n".join(report)


def main():
    """Main execution function"""
    print("🌟 Starting Recursive Function Test Suite")
    print("Testing 33 iterations of various recursive functions...")
    print()
    
    # Initialize test suite
    test_suite = RecursiveTestSuite()
    
    # Run comprehensive tests
    analysis = test_suite.run_comprehensive_tests()
    
    # Generate and display report
    report = test_suite.generate_report(analysis)
    print("\n" + report)
    
    # Save report to file
    with open("/workspace/recursive_test_report.txt", "w") as f:
        f.write(report)
    
    print(f"\n📄 Detailed report saved to: /workspace/recursive_test_report.txt")
    
    return analysis


if __name__ == "__main__":
    main()