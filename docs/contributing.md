# Contributing to ndastro-engine

Thank you for considering contributing to ndastro-engine! This document outlines the process and guidelines for contributing.

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ndastro-core.git
   cd ndastro-core
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -e ".[dev,docs]"
   ```

## Development Workflow

### Running Tests

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=ndastro_engine --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_ayanamsa.py
```

### Code Quality

**Linting and Formatting:**
```bash
ruff check .
ruff format .
```

**Type Checking:**
```bash
mypy ndastro_engine
```

### Building Documentation

Build documentation locally:
```bash
mkdocs build
```

Serve documentation with live reload:
```bash
mkdocs serve
```

Then open http://127.0.0.1:8000/ in your browser.

## Coding Standards

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write docstrings in Google style format
- Keep functions focused and single-purpose
- Aim for 90%+ test coverage

### Example Docstring

```python
def calculate_something(value: float, factor: int = 1) -> float:
    """Calculate something based on value and factor.

    Args:
        value: The input value to process.
        factor: Multiplication factor. Defaults to 1.

    Returns:
        The calculated result.

    Raises:
        ValueError: If value is negative.

    Example:
        >>> calculate_something(10.0, 2)
        20.0
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    return value * factor
```

## Pull Request Process

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code
   - Add/update tests
   - Update documentation if needed

3. **Commit**
   ```bash
   git add .
   git commit -m "feat: add new ayanamsa calculation method"
   ```

   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test additions/changes
   - `refactor:` for code refactoring

4. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **PR Checklist**
   - [ ] Tests pass locally
   - [ ] Code is formatted with ruff
   - [ ] Type checking passes
   - [ ] Documentation is updated
   - [ ] CHANGELOG.md is updated
   - [ ] Descriptive PR title and description

## Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- ndastro-engine version
- Minimal code example reproducing the issue
- Expected vs actual behavior
- Full error traceback if applicable

## Feature Requests

Feature requests are welcome! Please:

- Check existing issues first
- Provide clear use case
- Explain expected behavior
- Consider implementation complexity

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
