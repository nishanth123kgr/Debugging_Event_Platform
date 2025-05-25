#!/usr/bin/env python3
"""
Test script to verify runcode functionality works correctly
"""

from runcode import RunCCode, RunPyCode

def test_c_compilation():
    """Test C code compilation and execution"""
    print("Testing C code compilation...")
    
    c_code = '''
#include <stdio.h>

int main() {
    printf("Hello from C!\\n");
    return 0;
}
'''
    
    try:
        runner = RunCCode(c_code)
        compilation_result, execution_result = runner.run_c_code()
        
        print(f"Compilation: {compilation_result}")
        print(f"Execution: {execution_result}")
        
        if execution_result and "Hello from C!" in execution_result:
            print("✅ C compilation test PASSED")
            return True
        else:
            print("❌ C compilation test FAILED")
            return False
            
    except Exception as e:
        print(f"❌ C compilation test ERROR: {e}")
        return False

def test_python_execution():
    """Test Python code execution"""
    print("Testing Python code execution...")
    
    py_code = 'print("Hello from Python!")'
    
    try:
        runner = RunPyCode(py_code)
        stderr, stdout = runner.run_py_code()
        
        print(f"Stderr: {stderr}")
        print(f"Stdout: {stdout}")
        
        if stdout and "Hello from Python!" in stdout:
            print("✅ Python execution test PASSED")
            return True
        else:
            print("❌ Python execution test FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Python execution test ERROR: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing runcode functionality...\n")
    
    c_test = test_c_compilation()
    print()
    py_test = test_python_execution()
    
    print("\n📊 Test Results:")
    print(f"C Compilation: {'✅ PASS' if c_test else '❌ FAIL'}")
    print(f"Python Execution: {'✅ PASS' if py_test else '❌ FAIL'}")
    
    if c_test and py_test:
        print("\n🎉 All tests passed! Ready for deployment.")
    else:
        print("\n⚠️  Some tests failed. Check your environment.")
