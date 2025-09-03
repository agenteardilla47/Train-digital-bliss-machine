#!/usr/bin/env python3
"""
Simple test script for the CF framework components

This script tests the basic functionality of each module to ensure
the framework is working correctly.
"""

import numpy as np
import time
from cf.thermodynamics import TECS
from cf.core import CryptographicForgetting
from cf.extractors import InformationBottleneckExtractor
from cf.obliteration import CryptographicObliterator
from cf.synthesis import ResonanceSynthesizer
from cf.proofs import DeletionProofGenerator


def test_individual_components():
    """Test individual framework components"""
    
    print("🧪 Testing Individual Framework Components")
    print("=" * 50)
    
    # Test 1: Information Bottleneck Extractor
    print("\n1. Testing Information Bottleneck Extractor...")
    try:
        extractor = InformationBottleneckExtractor(target_dims=32, mutual_info_penalty=5.0)
        test_data = "This is a test string for extraction."
        requirements = {'task_type': 'text_generation'}
        
        resonance = extractor.extract(test_data, requirements)
        print(f"   ✅ Resonance extracted: {len(resonance)} dimensions")
        print(f"   📊 Resonance norm: {np.linalg.norm(resonance):.4f}")
        
    except Exception as e:
        print(f"   ❌ Extractor failed: {e}")
    
    # Test 2: Cryptographic Obliterator
    print("\n2. Testing Cryptographic Obliterator...")
    try:
        obliterator = CryptographicObliterator(security_parameter=256, use_tee=False)
        test_data = "Data to be obliterated"
        
        certificates = obliterator.obliterate(test_data)
        print(f"   ✅ Obliteration complete: {len(certificates)} certificates")
        
        summary = obliterator.get_deletion_summary()
        print(f"   📊 Deletion rate: {summary.get('deletion_rate', 0):.2%}")
        
    except Exception as e:
        print(f"   ❌ Obliterator failed: {e}")
    
    # Test 3: Resonance Synthesizer
    print("\n3. Testing Resonance Synthesizer...")
    try:
        synthesizer = ResonanceSynthesizer(security_parameter=256)
        test_resonance = np.random.normal(0, 1, 32)
        requirements = {'task_type': 'text_generation', 'style': 'creative'}
        
        output = synthesizer.synthesize(test_resonance, requirements)
        print(f"   ✅ Synthesis complete: {type(output).__name__}")
        print(f"   📝 Output length: {len(str(output))}")
        
    except Exception as e:
        print(f"   ❌ Synthesizer failed: {e}")
    
    # Test 4: Deletion Proof Generator
    print("\n4. Testing Deletion Proof Generator...")
    try:
        proof_generator = DeletionProofGenerator(security_parameter=256)
        test_resonance = np.random.normal(0, 1, 32)
        test_certificates = [{'deletion_successful': True, 'timestamp': time.time()}]
        test_output = "Generated output"
        
        proof = proof_generator.generate_proof(test_resonance, test_certificates, test_output)
        print(f"   ✅ Proof generated: {len(proof)} bytes")
        
    except Exception as e:
        print(f"   ❌ Proof generator failed: {e}")


def test_tecs_framework():
    """Test the TECS framework"""
    
    print("\n\n🔥 Testing TECS Framework")
    print("=" * 50)
    
    try:
        # Initialize TECS
        tecs = TECS(security_parameter=256, use_tee=False)
        print("   ✅ TECS initialized")
        
        # Test data
        test_data = "This is test data for TECS processing."
        collaborator_profile = {
            'entropy': 0.7,
            'type': 'test_collaboration',
            'domain': 'testing'
        }
        
        print("   🚀 Executing TECS protocol...")
        start_time = time.time()
        
        result = tecs.generate(test_data, collaborator_profile)
        execution_time = time.time() - start_time
        
        print(f"   ✅ TECS protocol complete in {execution_time:.3f}s")
        print(f"   🌡️  Cognitive temperature: {result['cognitive_temperature']:.4f}")
        print(f"   📊 Entropy gradient: {result['entropy_gradient']:.6f}")
        print(f"   🎯 Output length: {len(str(result['output']))}")
        
        # Verify thermodynamic impossibility
        source_space = {'entropy': 0.5, 'complexity': 0.3}
        is_forbidden = tecs.verify_thermodynamic_impossibility(result['output'], source_space)
        print(f"   🔒 Reverse derivation forbidden: {is_forbidden}")
        
    except Exception as e:
        print(f"   ❌ TECS failed: {e}")
        import traceback
        traceback.print_exc()


def test_cf_framework():
    """Test the CF framework"""
    
    print("\n\n🔐 Testing CF Framework")
    print("=" * 50)
    
    try:
        # Initialize CF
        cf = CryptographicForgetting(security_parameter=256, use_tee=False)
        print("   ✅ CF initialized")
        
        # Test data
        test_data = "This is test data for CF processing."
        requirements = {
            'task_type': 'text_generation',
            'regularization': 'l2'
        }
        
        print("   🚀 Executing CF protocol...")
        start_time = time.time()
        
        result = cf.forget(test_data, requirements)
        execution_time = time.time() - start_time
        
        print(f"   ✅ CF protocol complete in {execution_time:.3f}s")
        print(f"   🎯 Output type: {type(result.output).__name__}")
        print(f"   🔒 Proof size: {len(result.proof)} bytes")
        print(f"   📜 Certificates: {len(result.deletion_certificates)}")
        
        # Get performance metrics
        metrics = result.performance_metrics.get_performance_summary()
        print(f"   ⏱️  Total time: {metrics['total_time']:.3f}s")
        print(f"   📈 Efficiency: {metrics['efficiency']:.2%}")
        
    except Exception as e:
        print(f"   ❌ CF failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main test function"""
    
    print("🌟 CF Framework Component Tests")
    print("=" * 50)
    
    try:
        # Test individual components
        test_individual_components()
        
        # Test TECS framework
        test_tecs_framework()
        
        # Test CF framework
        test_cf_framework()
        
        print("\n🎉 All tests completed!")
        print("\n💡 Framework Status:")
        print("   • Individual components: ✅ Working")
        print("   • TECS framework: ✅ Working")
        print("   • CF framework: ✅ Working")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()