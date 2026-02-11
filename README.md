# 🚀 Python Intensive: 14-Day Training Program

**From Zero to Production-Ready FastAPI CRUD Application**

A comprehensive, hands-on Python training program designed for freshers, transitioning you from basic Python fundamentals to building production-ready FastAPI applications with 100% test coverage.

## 📚 Program Overview

This 14-day intensive training follows a **Test-Driven Development (TDD)** approach, where you'll learn by implementing solutions that pass comprehensive test suites. Each day builds upon previous concepts, using a realistic business context: **Consulting Timesheet Tracker**.

### 🎯 Learning Philosophy

- **TDD First**: Tests are provided; you implement solutions to make them pass
- **Incremental Complexity**: Each day introduces new concepts while reinforcing previous ones
- **Business Context**: All exercises based on realistic consulting timesheet tracking scenarios
- **Production-Ready**: By Day 14, you'll have a fully functional, deployable API

---

## 🗓️ Training Schedule

### **Week 1: Python Fundamentals** (Days 1-7)

| Day | Topic | Key Concepts |
|-----|-------|--------------|
| **01** | Type Hinting & Basic Functions | Type annotations, function signatures, mypy |
| **02** | Collections (Lists & Dicts) | List operations, dict manipulation, data structures |
| **03** | Comprehensions | List/dict/set comprehensions, transformations |
| **04** | Error Handling | try/except, custom exceptions, validation |
| **05** | File I/O | JSON/CSV reading/writing, file operations |
| **06** | Object-Oriented Programming | Classes, inheritance, encapsulation |
| **07** | **Week 1 Integration** | Complete CLI timesheet application |

### **Week 2: FastAPI & Production Skills** (Days 8-14)

| Day | Topic | Key Concepts |
|-----|-------|--------------|
| **08** | Async Programming | async/await, asyncio, concurrent execution |
| **09** | Pydantic Models | Data validation, Field constraints, custom validators |
| **10** | FastAPI Basics | HTTP methods, routing, request/response models |
| **11** | FastAPI Advanced CRUD | Database integration, filtering, background tasks |
| **12** | Dependency Injection | FastAPI Depends(), service layers, authentication |
| **13** | Testing & Mocking | pytest-mock, httpx mocking, 100% coverage |
| **14** | **Production App** | Complete CRUD API with all best practices |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Git (optional, for version control)
- Code editor (VS Code recommended)

### Installation

1. **Clone or download this repository**:
   ```bash
   git clone <repository-url>
   cd python-excercises
   ```

2. **Install dependencies**:
   ```bash
   make install
   # or manually:
   pip install -e .
   ```

3. **Verify installation**:
   ```bash
   make test
   ```

---

## 📖 How to Use This Training

### Daily Workflow

Each day follows this structure:

```
days/
├── day_01_type_hinting/
│   ├── task.py          # ← Implement functions here (empty stubs with docstrings)
│   └── test_task.py     # ← Comprehensive tests (already complete)
```

### Step-by-Step Process

1. **Navigate to the day's folder**:
   ```bash
   cd days/day_01_type_hinting
   ```

2. **Read the task.py file**:
   - Review function signatures
   - Read docstrings for requirements
   - Understand type hints

3. **Read the tests** to understand expected behavior:
   ```bash
   cat test_task.py
   ```

4. **Run tests** (they will fail initially):
   ```bash
   make test-day DAY=01
   ```

5. **Implement functions** in `task.py` until tests pass:
   ```python
   def calculate_billable_hours(regular_hours: float, overtime_hours: float) -> float:
       """Calculate total billable hours"""
       return regular_hours + (overtime_hours * 1.5)  # Your implementation
   ```

6. **Re-run tests** to verify:
   ```bash
   make test-day DAY=01
   ```

7. **Check coverage**:
   ```bash
   make coverage DAY=01
   ```

8. **Move to the next day** once all tests pass!

---

## 🛠️ Available Commands

The `Makefile` provides convenient shortcuts:

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install dependencies |
| `make test` | Run all tests with coverage |
| `make test-day DAY=XX` | Run tests for specific day (e.g., `DAY=01`) |
| `make coverage` | Generate HTML coverage report |
| `make lint` | Run Ruff linter |
| `make format` | Format code with Black |
| `make type-check` | Run mypy type checking |
| `make clean` | Remove cache and generated files |

### Examples

```bash
# Test only Day 5
make test-day DAY=05

# Format all code
make format

# Check types
make type-check

# Full quality check
make lint && make type-check && make test
```

---

## 📂 Project Structure

```
python-excercises/
├── days/                      # Daily exercises
│   ├── day_01_type_hinting/
│   ├── day_02_collections/
│   ├── ...
│   └── day_14_production_app/
├── pyproject.toml             # Project configuration & dependencies
├── Makefile                   # Convenience commands
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

Each day's folder contains:
- `task.py`: Functions to implement (with type hints and docstrings)
- `test_task.py`: Comprehensive test suite

---

## 🎓 Learning Path Details

### Days 1-3: Python Basics

**Goal**: Master Python fundamentals with type safety

- Type hints for static analysis
- Working with collections (lists, dicts, sets)
- Data transformations with comprehensions

**Key Takeaway**: Write clean, type-safe Python code

### Days 4-6: Intermediate Python

**Goal**: Handle errors and build reusable components

- Custom exceptions and validation
- File operations (JSON, CSV)
- Object-oriented design patterns

**Key Takeaway**: Build robust, maintainable code

### Day 7: Week 1 Integration

**Goal**: Combine all Week 1 concepts

- Build complete CLI application
- Integrate types, collections, OOP, file I/O
- Practice real-world problem-solving

**Milestone**: Functional timesheet tracker CLI

### Days 8-10: Async & Web APIs

**Goal**: Learn modern async programming and FastAPI basics

- Async/await patterns with asyncio
- Pydantic for data validation
- FastAPI routing and CRUD operations

**Key Takeaway**: Build async web APIs

### Days 11-13: Advanced FastAPI

**Goal**: Master professional API development

- Database patterns and advanced queries
- Dependency injection for modularity
- Comprehensive testing with mocks

**Key Takeaway**: Write production-quality APIs

### Day 14: Production Deployment

**Goal**: Build complete, deploy-ready application

- Environment configuration
- Logging and error handling
- CORS and security
- 100% test coverage

**🏆 Final Milestone**: Production-ready FastAPI CRUD application

---

## 🧪 Testing Philosophy

This program emphasizes **Test-Driven Development (TDD)**:

1. **Tests are provided**: You know exactly what's expected
2. **Red-Green-Refactor**:
   - 🔴 **Red**: Tests fail initially
   - 🟢 **Green**: Implement to make tests pass
   - 🔵 **Refactor**: Improve code while tests stay green
3. **100% Coverage Goal**: All code paths are tested

### Test Organization

Each `test_task.py` contains:
- **Test classes**: Group related tests
- **Multiple test methods**: Cover different scenarios
- **Edge cases**: Boundary conditions, errors, invalid inputs
- **Realistic data**: Based on consulting timesheet domain

---

## 📊 Progress Tracking

### Recommended Daily Schedule

- **Morning** (2-3 hours):
  - Read day's task.py and test_task.py
  - Understand requirements
  - Plan implementation

- **Afternoon** (3-4 hours):
  - Implement solutions
  - Run tests iteratively
  - Refactor for clarity

- **Evening** (1 hour):
  - Review what you learned
  - Preview next day
  - Note questions or challenges

### Checkpoints

- **After Day 3**: Should be comfortable with Python basics
- **After Day 7**: Should can build CLI applications
- **After Day 10**: Should understand async and FastAPI fundamentals
- **After Day 14**: Should can build production APIs

---

## 🏗️ Technologies Used

### Core Framework
- **FastAPI** (>=0.109.0): Modern, fast web framework
- **Pydantic** (>=2.5.0): Data validation using Python type hints

### Testing
- **pytest** (>=7.4.0): Testing framework
- **pytest-asyncio**: Testing async code
- **pytest-cov**: Coverage reports
- **pytest-mock**: Mocking external dependencies

### Code Quality
- **Black**: Code formatter
- **Ruff**: Fast Python linter
- **Mypy**: Static type checker

### Async & HTTP
- **httpx**: Async HTTP client
- **asyncio**: Built-in async framework

---

## 🎯 Success Criteria

By completing this program, you will:

✅ Write type-safe Python code with modern best practices  
✅ Build RESTful APIs with FastAPI  
✅ Implement async operations efficiently  
✅ Use Pydantic for robust data validation  
✅ Write comprehensive test suites with pytest  
✅ Mock external dependencies for isolated testing  
✅ Apply dependency injection patterns  
✅ Handle errors gracefully with proper logging  
✅ Achieve high test coverage (targeting 100%)  
✅ Deploy production-ready applications  

---

## 💡 Tips for Success

1. **Don't skip days**: Each builds on previous knowledge
2. **Read tests carefully**: They're your specification
3. **Start simple**: Get basic cases working first
4. **Iterate**: Make tests pass, then refactor
5. **Use type hints**: Catch errors during development
6. **Ask "why"**: Understand concepts, don't just copy code
7. **Experiment**: Try different approaches
8. **Keep notes**: Document your learning journey

---

## 🐛 Troubleshooting

### Tests won't run
```bash
# Ensure dependencies are installed
make install

# Check Python version
python --version  # Should be 3.10+
```

### Import errors
```bash
# Install in editable mode
pip install -e .
```

### Type errors from mypy
```bash
# Run type checker
make type-check

# Review function signatures and return types
```

### Coverage not 100%
```bash
# Generate HTML report
make coverage

# Open htmlcov/index.html to see uncovered lines
```

---

## 📚 Additional Resources

### Official Documentation
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pytest Documentation](https://docs.pytest.org/)

### Recommended Reading
- "Fluent Python" by Luciano Ramalho
- "Python Testing with pytest" by Brian Okken
- "FastAPI Best Practices" (FastAPI docs)

---

## 🤝 Contributing

Found an issue or have suggestions? Feel free to:
- Open an issue
- Submit a pull request
- Suggest improvements

---

## 📄 License

This training material is provided for educational purposes.

---

## 🎉 Congratulations!

You're about to embark on an intensive journey to become a proficient Python backend developer. Remember:

> "The expert in anything was once a beginner." — Helen Hayes

**Start with Day 1 and build your skills one day at a time. Good luck! 🚀**

---

## Quick Reference Card

```bash
# Daily routine
cd days/day_XX_topic_name
make test-day DAY=XX          # See failing tests
# ... implement in task.py ...
make test-day DAY=XX          # Verify passing tests
make coverage DAY=XX          # Check coverage

# Quality checks before moving on
make format                   # Format code
make lint                     # Check style
make type-check               # Verify types
```

---

**Ready to start? Navigate to [days/day_01_type_hinting](days/day_01_type_hinting/) and begin your journey!** 🎯
