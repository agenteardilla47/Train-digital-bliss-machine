# Cryptographic Forgetting (CF) Framework

A provably secure framework for irreversibly destroying source material while preserving functional intent through resonance distillation.

## Overview

Cryptographic Forgetting (CF) is a systematic methodology that operates through four core mechanisms:

1. **Intent Crystallization** - Maps inputs to minimal invariant representations
2. **Cryptographic Obliteration** - Renders source material computationally unrecoverable
3. **Resonance Synthesis** - Generates outputs from distilled essence plus fresh entropy
4. **Zero-Knowledge Deletion** - Provides verifiable proof of destruction

## Features

- **Provable Security**: Based on established cryptographic principles and information theory
- **Information Bottleneck**: Implements mutual information minimization for source disconnection
- **TEE Support**: Enhanced security through Trusted Execution Environments
- **Zero-Knowledge Proofs**: Verifiable deletion using zk-SNARKs
- **Performance Optimized**: Linear scaling with source size

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from cf.core import CryptographicForgetting

# Initialize CF framework
cf = CryptographicForgetting(security_parameter=256)

# Execute forgetting protocol
output, proof, certificates = cf.forget(
    source_data=your_data,
    functional_requirements=your_requirements
)

# Verify deletion proof
is_valid = cf.verify_deletion_proof(proof)
```

## Architecture

- `cf/core.py` - Main CF protocol implementation
- `cf/extractors/` - Intent crystallization and information bottleneck
- `cf/obliteration/` - Cryptographic deletion and memory sanitization
- `cf/synthesis/` - Resonance-based output generation
- `cf/proofs/` - Zero-knowledge deletion verification
- `cf/tee/` - Trusted Execution Environment support

## Security

- **Source Unrecoverability**: No polynomial-time adversary can reconstruct source material
- **Trace Elimination**: All intermediate representations are destroyed
- **Verifiable Deletion**: Zero-knowledge proof of complete deletion

## License

This work is dedicated to the public domain to prevent proprietary enclosure of forgetting technologies.

## References

See the research paper for detailed theoretical foundations and security analysis.