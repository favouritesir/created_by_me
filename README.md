# 🚀 Created By Me | Original Algorithms & Systems Research

[![Author](https://img.shields.io/badge/Author-Ashikur_Rahman-blue.svg?style=for-the-badge&logo=github)](https://github.com/favouritesir)
[![Established](https://img.shields.io/badge/Origin-2022_--_Present-purple.svg?style=for-the-badge)](https://github.com/favouritesir/created_by_me)
[![Languages](https://img.shields.io/badge/Languages-C_|_JS_|_Python_|_Java_|_C%23-informational?style=for-the-badge)](https://github.com/favouritesir/created_by_me)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Testing Rigor](https://img.shields.io/badge/Validation-3--Tier_Stress_Tested-brightgreen.svg?style=for-the-badge)](https://github.com/favouritesir/created_by_me)

> *"Challenging textbook orthodoxies through aggressive memory optimization, in-place pointer discipline, and mathematical verification."*

Welcome to **`created_by_me`**. Unlike conventional repositories that replicate standard textbook implementations, this repository serves as a permanent research archive for **original algorithms, novel low-level optimizations, and systems programming experiments** conceived and developed by **Ashikur Rahman**.

---

## 📑 Table of Contents
- [📌 Repository Overview](#-repository-overview)
- [✨ Core Engineering Philosophy](#-core-engineering-philosophy)
- [📂 Featured Projects Catalog](#-featured-projects-catalog)
- [🗺️ Upcoming Research & Projects Roadmap](#️-upcoming-research--projects-roadmap-inshaallah)
- [🏛️ Repository Structure](#️-repository-structure)
- [📬 Author & Contact](#-author--contact)

---

## 📌 Repository Overview

This repository archives original algorithmic contributions designed to solve foundational computer science challenges with **extreme memory efficiency**:

1. **Zero-Allocation Execution ($O(1)$ Auxiliary Space):** Eliminating unnecessary buffer allocations in algorithms that traditionally demand $O(N)$ auxiliary heap or stack memory.
2. **Embedded & Systems Readiness:** Crafting algorithms that run safely in severely memory-constrained environments (bare-metal microcontrollers, IoT firmware, real-time operating systems).
3. **Multi-Tier Mathematical Verification:** Ensuring every design is verified through formal invariant proofs, differential cross-testing, and large-scale automated stress testing.

---

## ✨ Core Engineering Philosophy

| Principle | Traditional Approach | Our Philosophy |
| :--- | :--- | :--- |
| **Memory Footprint** | Lazy allocation of intermediate string/array buffers ($O(N)$) | **Aggressive In-Place Transformation ($O(1)$ auxiliary space)** |
| **Pass Count** | Multi-pass reductions (e.g., Reverse $\rightarrow$ Postfix $\rightarrow$ Reverse) | **Single-pass directional scanning with dual pointers** |
| **Verification** | 5–10 hand-crafted test cases | **Multi-tier automated fuzzing across 40,000+ random inputs** |
| **Portability** | Language-bound snippets | **Reference C with idiomatic ports across modern languages** |

---

## 📂 Featured Projects Catalog

### 1. 🔄 [In-Place Infix to Prefix Converter](✅%20infix%20to%20prefix/)
*A novel dual-pointer right-to-left scan that overwrites the input buffer in-place with zero auxiliary string allocation.*

- **Origin & Provenance:** Conceived and submitted as **Lab Report No. 01 (Problem 2)** in **December 2022** for Course *CSE-104: Structured Programming Lab* at the **Department of CSE, Green University of Bangladesh** (Student: Ashikur Rahman, ID: 221902131; Lecturer: Md. Abu Rumman Refat).
  - 📑 [View Original 2022 Lab Report Presentation (Google Slides)](https://docs.google.com/presentation/d/1ogiW8eGX2eApdnQU1bEeGhEWsG034DrZ7xZPR5uvhVY/edit?usp=sharing)
- **The Breakthrough:** Traditional textbook algorithms require 3 full string passes and an extra $O(N)$ buffer (Reverse $\rightarrow$ Postfix $\rightarrow$ Reverse). This algorithm performs the complete conversion **in-place** directly inside the original buffer using a backward read/write pointer discipline.
- **Safety Proof:** Mathematically proves the invariant `read_idx <= write_idx`, guaranteeing unread data is never overwritten.
- **Languages Provided:** C (Reference), JavaScript (Node.js), Python 3, Java, C#.
- **Robustness:** Validated across **40,000 randomized expressions** across 3 independent tiers with **0% corruption and 100.00% accuracy**.
- 👉 **[Explore Project & Full Documentation &raquo;](✅%20infix%20to%20prefix/)**

---

## 🗺️ Upcoming Research & Projects Roadmap (Insha'Allah)

This repository is continuously expanding with ongoing research and original algorithmic designs:

| Project | Domain | Core Innovation / Research Goal | Status |
| :--- | :--- | :--- | :---: |
| **Cloud Merge Sort** | External Sorting & Distributed Data | Optimizing disk/network memory footprint during large-scale external merges with in-place streaming buffers. | 🔬 In Research |
| **JSON Boundary Tracker** | High-Throughput Parsing | Zero-copy stream tokenization and lexical boundary detection without AST heap overhead. | 🔬 In Design |
| **Adaptive In-Place Cache Eviction** | Operating Systems & Caching | Low-overhead pointer-indexed cache replacement for resource-constrained micro-kernels. | 💡 Planned |
| **Bounded Stack Math Evaluator** | Embedded Firmware | Fixed-depth evaluation of mathematical trees with guaranteed zero-overflow guarantees. | 💡 Planned |

---

## 🏛️ Repository Structure

```text
created_by_me/
│
├── README.md                          # Main repository overview & research catalog
├── .gitignore                         # Excludes OS metadata & private publication drafts
│
└── ✅ infix to prefix/                 # Project: In-Place Infix to Prefix Converter
    ├── README.md                      # Comprehensive academic & practical documentation
    ├── infix to prefix.c              # Core reference implementation in C (memory-guarded)
    │
    ├── implementations/               # Idiomatic multi-language ports
    │   ├── infix_to_prefix.js         # JavaScript (Node.js) implementation
    │   ├── infix_to_prefix.py         # Python 3 implementation
    │   ├── InfixToPrefix.java         # Java implementation
    │   └── InfixToPrefix.cs           # C# / .NET implementation
    │
    └── tests/                         # Public test suite & validation harness
        ├── test_vectors.json          # 27 verified golden test vectors
        ├── test_suite.js              # Vector suite + differential random harness (JS)
        └── test_stress.py             # Full 40,000-expression 3-layer stress harness (Python)
```

---

## 🧪 Testing & Reproduction

Anyone can independently reproduce and verify the algorithms in this repository in seconds:

```bash
# Clone the repository
git clone https://github.com/favouritesir/created_by_me.git
cd created_by_me/"✅ infix to prefix"

# Run fast JavaScript validation (vectors + differential + invariants)
node tests/test_suite.js

# Run full 3-layer Python stress harness (40,000 expressions)
python tests/test_stress.py
```

---

## 📬 Author & Contact

**Ashikur Rahman**  
*Computer Systems & Algorithms Researcher / Software Engineer*  
- **GitHub:** [@favouritesir](https://github.com/favouritesir)  
- **Email:** [ashikur.gub@gmail.com](mailto:ashikur.gub@gmail.com)  

---

<p align="center">
  <i>"Simplicity and extreme memory efficiency are not accidents; they are the result of disciplined mathematical design."</i>
</p>
