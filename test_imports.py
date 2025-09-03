#!/usr/bin/env python3
"""
Simple import test for the CF framework
"""

def test_basic_imports():
    """Test that all basic imports work"""
    print("🧪 Testing basic imports...")
    
    try:
        # Test core imports
        print("  Testing core imports...")
        from cf.core import CryptographicForgetting
        print("    ✅ CryptographicForgetting imported successfully")
        
        from cf.extractors import InformationBottleneckExtractor
        print("    ✅ InformationBottleneckExtractor imported successfully")
        
        from cf.obliteration import CryptographicObliterator
        print("    ✅ CryptographicObliterator imported successfully")
        
        from cf.synthesis import ResonanceSynthesizer
        print("    ✅ ResonanceSynthesizer imported successfully")
        
        from cf.proofs import DeletionProofGenerator
        print("    ✅ DeletionProofGenerator imported successfully")
        
        print("  ✅ All core imports successful!")
        
    except ImportError as e:
        print(f"    ❌ Import failed: {e}")
        return False
    
    try:
        # Test thermodynamics
        print("  Testing thermodynamics...")
        from cf.thermodynamics import TECS
        print("    ✅ TECS imported successfully")
        
    except ImportError as e:
        print(f"    ❌ Thermodynamics import failed: {e}")
        return False
    
    try:
        # Test utilities
        print("  Testing utilities...")
        from cf.utils import SecurityParameters, PerformanceMetrics
        print("    ✅ Utilities imported successfully")
        
    except ImportError as e:
        print(f"    ❌ Utilities import failed: {e}")
        return False
    
    print("✅ All imports successful!")
    return True


def test_basic_functionality():
    """Test basic functionality without external dependencies"""
    print("\n🔧 Testing basic functionality...")
    
    try:
        # Test creating a CF instance
        from cf.core import CryptographicForgetting
        
        cf = CryptographicForgetting(security_parameter=128, use_tee=False)
        print("  ✅ CF instance created successfully")
        
        # Test getting security guarantees
        guarantees = cf.get_security_guarantees()
        print(f"  ✅ Security guarantees: {len(guarantees)} guarantees available")
        
        # Test memory estimation
        memory_est = cf.estimate_memory_usage(1024)  # 1KB
        print(f"  ✅ Memory estimation: {memory_est} bytes for 1KB input")
        
        print("✅ Basic functionality works!")
        return True
        
    except Exception as e:
        print(f"  ❌ Functionality test failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 CF Framework Import and Functionality Test")
    print("=" * 50)
    
    imports_ok = test_basic_imports()
    
    if imports_ok:
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n🎉 All tests passed! The framework is ready to use.")
        else:
            print("\n⚠️  Imports work but functionality has issues.")
    else:
        print("\n❌ Import tests failed. Check dependencies.")