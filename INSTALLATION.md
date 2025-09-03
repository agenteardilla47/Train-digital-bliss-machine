# Installation Guide for CF Framework

## Quick Start

### 1. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv cf_env

# Activate virtual environment
source cf_env/bin/activate  # On Linux/Mac
# or
cf_env\Scripts\activate     # On Windows
```

### 2. Install Dependencies

```bash
# Install minimal requirements
pip install -r requirements_minimal.txt

# Or install full requirements (includes development tools)
pip install -r requirements.txt
```

### 3. Test Installation

```bash
# Run basic import test
python test_imports.py

# Run full test framework
python test_framework.py
```

## Dependencies Fixed

The following dependency issues have been resolved:

### ❌ Removed (Not Actually Used)
- `mine-pytorch` - Custom MINE implementation exists
- `py_ecc` - Not imported anywhere in the code
- `scikit-learn` - Not imported anywhere in the code
- `secrets` - Built-in Python module
- `psutil` - Not imported anywhere in the code
- `black`, `flake8` - Development tools only
- `sphinx` - Documentation tool only
- `line-profiler` - Not imported anywhere

### ✅ Kept (Actually Imported)
- `numpy` - Core numerical operations
- `scipy` - Optimization and entropy calculations
- `torch` - Neural network operations (MINE)
- `cryptography` - Cryptographic primitives
- `pytest` - Testing framework

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the virtual environment
2. **CUDA Issues**: Framework automatically falls back to CPU if CUDA unavailable
3. **TEE Support**: Automatically disabled if not available (graceful fallback)

### System Requirements

- Python 3.8+
- 2GB+ RAM (for larger inputs)
- CPU: Any modern processor
- GPU: Optional (PyTorch will use if available)

## Verification

After installation, you should be able to:

```python
from cf.core import CryptographicForgetting

# Create instance
cf = CryptographicForgetting(security_parameter=256, use_tee=False)

# Check security guarantees
guarantees = cf.get_security_guarantees()
print(f"Available guarantees: {len(guarantees)}")
```

## Next Steps

1. Run the demo scripts to see the framework in action
2. Check the IMPLEMENTATION_SUMMARY.md for detailed usage
3. Explore the individual modules in the `cf/` directory