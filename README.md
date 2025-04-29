
Let me create a detailed README for this experiment repository. First, I'll explore the codebase to understand its structure and purpose.

Ran tool
Now let me look at the key files to understand what experiments this repository is conducting.

Read file: experiments.py

Read file: Cargo.toml

Read file: pyproject.toml

Ran tool

Read file: src/lib.rs

Ran tool

Read file: src/pyo3_interior_mutability_experiment/__init__.py
Based on my exploration of the repository, here's the README I'm creating:

# PyO3 Interior Mutability Experiment

This repository demonstrates a Python-Rust integration experiment focusing on interior mutability patterns using PyO3. It shows how to expose Rust structs with interior mutability to Python while preserving proper reference semantics.

## Overview

The experiment explores how to implement Python bindings for Rust structures that need interior mutability, ensuring that:

1. Multiple Python references to the same Rust object share state correctly
2. Objects stored in containers can be mutated through any reference
3. Proper Python semantics are maintained across all reference points

## Implementation Details

The project uses:
- **PyO3**: A Rust library for creating Python extensions
- **RwLock**: For thread-safe interior mutability in Rust
- **Maturin**: For building and developing Python extensions written in Rust

### Key Components

- **PyOtherStruct**: A Python-exposable wrapper around a basic Rust struct with interior mutability
- **PyMyStruct**: A container class that demonstrates proper reference semantics when storing mutable objects

## Experiments

The `experiments.py` file contains various test cases demonstrating:
- Basic mutation of Python-wrapped Rust objects
- Reference sharing behavior between multiple variables
- Container storage and reference semantics
- Object sharing between multiple containers
- In-place modification through iteration

## Getting Started

### Prerequisites
- Rust (latest stable)
- Python 3.7+
- Maturin (`pip install maturin`)

### Building the Project
```bash
maturin develop
```

### Running the Experiments
```bash
python experiments.py
```

## Project Structure

- `src/lib.rs`: Contains the Rust implementation of PyO3 bindings
- `experiments.py`: Python script with test cases demonstrating proper behavior
- `pyproject.toml`: Python project configuration for Maturin
- `Cargo.toml`: Rust project configuration

## Use Cases

This pattern is particularly useful for:
- Wrapping Rust data structures that require interior mutability
- Creating Python bindings for Rust objects that need shared mutability
- Implementing Python extensions where objects may be stored in collections but need to maintain shared state
