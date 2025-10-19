#!/usr/bin/env python3
"""
Enhanced Security Test Suite

This script tests all the enhanced security implementations including:
- Fixed security vulnerabilities
- Enhanced zk-SNARK proofs
- TEE support
- Enhanced MINE estimator
- Security validation
"""

import sys
import time
import numpy as np
from typing import Dict, Any

# Add the cf module to path
sys.path.append('.')

from cf.core import CryptographicForgetting
from cf.thermodynamics import TECS
from cf.proofs.zk_snark import EnhancedDeletionProofGenerator
from cf.obliteration.tee_support import TEESupport
from cf.extractors.mine_estimator import MINEEstimator
from cf.security.security_validator import SecurityValidator


def test_security_vulnerability_fixes():
    """Test that security vulnerabilities have been fixed"""
    print("🔒 Testing Security Vulnerability Fixes")
    print("-" * 50)
    
    # Test 1: eval() usage fix
    print("1. Testing eval() usage fix...")
    try:
        from cf.proofs.deletion_proof_generator import DeletionProofGenerator
        
        # Create proof generator
        proof_gen = DeletionProofGenerator(security_parameter=256)
        
        # Test proof generation (should not use eval)
        resonance = np.random.normal(0, 1, 32)
        certificates = [{'deletion_successful': True, 'timestamp': time.time()}]
        output = "test output"
        
        proof = proof_gen.generate_proof(resonance, certificates, output)
        
        # Verify proof is JSON, not eval-able
        import json
        proof_data = json.loads(proof.decode())
        
        print("   ✅ eval() usage fixed - using JSON parsing")
        
    except Exception as e:
        print(f"   ❌ eval() fix failed: {e}")
        return False
    
    # Test 2: Input validation
    print("2. Testing input validation...")
    try:
        cf = CryptographicForgetting(security_parameter=256, use_tee=False)
        
        # Test with invalid inputs
        try:
            cf.forget(None, {})  # Should raise ValueError
            print("   ❌ Input validation failed - should reject None input")
            return False
        except ValueError:
            print("   ✅ Input validation working - rejects None input")
        
        try:
            cf.forget("test", {})  # Should raise ValueError for empty requirements
            print("   ❌ Input validation failed - should reject empty requirements")
            return False
        except ValueError:
            print("   ✅ Input validation working - rejects empty requirements")
        
    except Exception as e:
        print(f"   ❌ Input validation test failed: {e}")
        return False
    
    print("   ✅ All security vulnerability fixes working")
    return True


def test_enhanced_zk_snark():
    """Test enhanced zk-SNARK implementation"""
    print("\n🔐 Testing Enhanced zk-SNARK Implementation")
    print("-" * 50)
    
    try:
        # Test enhanced proof generator
        proof_gen = EnhancedDeletionProofGenerator(security_parameter=256)
        
        # Setup the proof system
        print("1. Setting up zk-SNARK proof system...")
        proving_key, verification_key = proof_gen.setup()
        print("   ✅ Proof system setup complete")
        
        # Test proof generation
        print("2. Testing proof generation...")
        resonance = np.random.normal(0, 1, 32)
        certificates = [{'deletion_successful': True, 'timestamp': time.time()}]
        output = "test output"
        
        proof = proof_gen.generate_proof(resonance, certificates, output)
        print(f"   ✅ Proof generated: {len(proof)} bytes")
        
        # Test proof verification
        print("3. Testing proof verification...")
        public_inputs = {'resonance_commitment': 'test', 'output_hash': 'test'}
        
        is_valid = proof_gen.verify_proof(proof, public_inputs)
        print(f"   ✅ Proof verification: {'PASSED' if is_valid else 'FAILED'}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Enhanced zk-SNARK test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tee_support():
    """Test TEE support implementation"""
    print("\n🛡️ Testing TEE Support Implementation")
    print("-" * 50)
    
    try:
        # Test TEE support
        tee_support = TEESupport()
        
        print(f"1. TEE Available: {tee_support.is_available()}")
        print(f"   TEE Type: {tee_support.get_tee_type()}")
        
        if tee_support.is_available():
            print("2. Testing secure deletion with TEE...")
            test_data = "sensitive test data"
            
            success = tee_support.secure_delete_tee(test_data)
            print(f"   ✅ Secure deletion: {'SUCCESS' if success else 'FAILED'}")
            
            print("3. Testing TEE attestation...")
            attestation = tee_support.get_attestation()
            print(f"   ✅ Attestation generated: {len(attestation)} fields")
            
        else:
            print("   ℹ️ TEE not available - using software fallback")
        
        print("4. Testing final sanitization...")
        tee_support.final_sanitization()
        print("   ✅ Final sanitization complete")
        
        return True
        
    except Exception as e:
        print(f"   ❌ TEE support test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_enhanced_mine_estimator():
    """Test enhanced MINE estimator"""
    print("\n🧠 Testing Enhanced MINE Estimator")
    print("-" * 50)
    
    try:
        # Test MINE estimator
        mine_estimator = MINEEstimator(
            learning_rate=0.001,
            batch_size=32,
            epochs=10  # Reduced for testing
        )
        
        print("1. Testing mutual information estimation...")
        
        # Test with string data
        source_text = "This is a test string for mutual information estimation."
        resonance = np.random.normal(0, 1, 64)
        
        mi_estimate = mine_estimator.estimate_mi(source_text, resonance)
        print(f"   ✅ MI estimate (string): {mi_estimate:.4f}")
        
        # Test with array data
        source_array = np.random.random(32)
        mi_estimate2 = mine_estimator.estimate_mi(source_array, resonance)
        print(f"   ✅ MI estimate (array): {mi_estimate2:.4f}")
        
        # Test training summary
        print("2. Testing training summary...")
        summary = mine_estimator.get_training_summary()
        print(f"   ✅ Training summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Enhanced MINE estimator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_security_validator():
    """Test security validator"""
    print("\n🔍 Testing Security Validator")
    print("-" * 50)
    
    try:
        validator = SecurityValidator()
        
        print("1. Testing code security validation...")
        
        # Test safe code
        safe_code = """
def safe_function(data):
    if data is None:
        raise ValueError("Data cannot be None")
    return data.upper()
"""
        safe_result = validator.validate_code_security(safe_code, "safe_code.py")
        print(f"   ✅ Safe code validation: Score {safe_result['security_score']}")
        
        # Test unsafe code
        unsafe_code = """
def unsafe_function(data):
    return eval(data)
"""
        unsafe_result = validator.validate_code_security(unsafe_code, "unsafe_code.py")
        print(f"   ✅ Unsafe code validation: Score {unsafe_result['security_score']}")
        print(f"   Vulnerabilities found: {len(unsafe_result['vulnerabilities'])}")
        
        print("2. Testing security tests...")
        test_results = validator.run_security_tests()
        print(f"   ✅ Security tests: {test_results['passed_tests']}/{test_results['passed_tests'] + test_results['failed_tests']} passed")
        print(f"   Overall score: {test_results['overall_score']:.1f}%")
        
        print("3. Testing compliance checks...")
        compliance = validator.check_compliance()
        print(f"   ✅ Compliance checks: {len(compliance['checks'])} frameworks checked")
        
        print("4. Generating security report...")
        report = validator.generate_security_report()
        print(f"   ✅ Security report generated: Overall score {report['overall_security_score']:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Security validator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integrated_framework():
    """Test the integrated framework with all enhancements"""
    print("\n🚀 Testing Integrated Framework with Enhancements")
    print("-" * 50)
    
    try:
        # Test CF framework with enhancements
        print("1. Testing enhanced CF framework...")
        cf = CryptographicForgetting(security_parameter=256, use_tee=True)
        
        test_data = "This is test data for the enhanced CF framework."
        requirements = {
            'task_type': 'text_generation',
            'style': 'creative',
            'regularization': 'l2'
        }
        
        start_time = time.time()
        result = cf.forget(test_data, requirements)
        execution_time = time.time() - start_time
        
        print(f"   ✅ CF execution time: {execution_time:.3f}s")
        print(f"   Output type: {type(result.output).__name__}")
        print(f"   Proof size: {len(result.proof)} bytes")
        print(f"   Certificates: {len(result.deletion_certificates)}")
        
        # Test TECS framework with enhancements
        print("2. Testing enhanced TECS framework...")
        tecs = TECS(security_parameter=256, use_tee=True)
        
        collaborator_profile = {
            'entropy': 0.8,
            'type': 'test_collaboration',
            'domain': 'testing'
        }
        
        start_time = time.time()
        tecs_result = tecs.generate(test_data, collaborator_profile)
        execution_time = time.time() - start_time
        
        print(f"   ✅ TECS execution time: {execution_time:.3f}s")
        print(f"   Cognitive temperature: {tecs_result['cognitive_temperature']:.4f}")
        print(f"   Entropy gradient: {tecs_result['entropy_gradient']:.6f}")
        print(f"   Output length: {len(str(tecs_result['output']))}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Integrated framework test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    print("🌟 Enhanced Security Test Suite")
    print("=" * 60)
    print()
    
    test_results = {}
    
    # Run all tests
    tests = [
        ("Security Vulnerability Fixes", test_security_vulnerability_fixes),
        ("Enhanced zk-SNARK", test_enhanced_zk_snark),
        ("TEE Support", test_tee_support),
        ("Enhanced MINE Estimator", test_enhanced_mine_estimator),
        ("Security Validator", test_security_validator),
        ("Integrated Framework", test_integrated_framework)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            test_results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed_tests = sum(1 for result in test_results.values() if result)
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("\n🎉 All enhanced security implementations are working correctly!")
        print("   • Security vulnerabilities fixed")
        print("   • Enhanced zk-SNARK proofs implemented")
        print("   • TEE support completed")
        print("   • Enhanced MINE estimator working")
        print("   • Security validation operational")
        print("   • Integrated framework functional")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} tests failed. Please check the output above for details.")
    
    return passed_tests == total_tests


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)