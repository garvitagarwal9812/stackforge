# Contributing to StackForge

First off, thank you for considering contributing to StackForge! 🎉

Every contribution — whether it's fixing a typo, adding a new template, reporting a bug, or proposing a feature — makes StackForge better for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by the [StackForge Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to **garvit@stackforge.dev**.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/stackforge.git
   cd stackforge
   ```
3. **Create a branch** for your work:
   ```bash
   git checkout -b feature/my-new-feature
   ```

## How to Contribute

### 🐛 Reporting Bugs

- Use the [GitHub Issues](https://github.com/garvitagarwal9812/stackforge/issues) page
- Include your OS, Python version, and steps to reproduce
- Paste the full error traceback if applicable
- Check existing issues first to avoid duplicates

### 💡 Suggesting Features

- Open an issue with the `enhancement` label
- Describe the use case and expected behavior
- Explain why this would be useful to other users

### 🛠️ Adding New Templates

StackForge is template-driven. To add a new backend, frontend, database, or pipeline:

1. Add the template function in the appropriate file under `stackforge/templates/`
2. Register the option in `stackforge/core/config.py`
3. Add handling in `stackforge/core/generator.py`
4. Write tests in `tests/`

### 📝 Improving Documentation

Documentation improvements are always welcome! This includes:
- README enhancements
- Docstring improvements
- Adding usage examples
- Fixing typos

## Development Setup

```bash
# Clone and enter the project
git clone https://github.com/garvitagarwal9812/stackforge.git
cd stackforge

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dependencies
pip install -e .

# Verify installation
stackforge --version

# Run the test suite
python -m unittest discover tests -v
```

## Coding Standards

- **Python 3.9+** compatibility required
- Follow **PEP 8** style guidelines
- Use **type hints** for all function signatures
- Add **docstrings** to all public functions and classes
- Keep imports organized: stdlib → third-party → local
- Use `rich` for all terminal output (no bare `print()` in the CLI)

## Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>

[optional body]
[optional footer]
```

**Types:**
| Type | Description |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation changes |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring, no feature change |
| `test` | Adding or updating tests |
| `chore` | Build process, tooling, dependencies |

**Examples:**
```
feat(templates): add Django REST Framework backend template
fix(generator): handle spaces in project names on Windows
docs(readme): add npm installation instructions
test(presets): add validation tests for MERN preset
```

## Pull Request Process

1. **Update tests** — Ensure all existing tests pass and add new ones for your changes
2. **Update documentation** — If your change affects usage, update the README or docstrings
3. **Keep PRs focused** — One feature or fix per pull request
4. **Fill out the PR template** — Describe what, why, and how
5. **Link related issues** — Reference any issues your PR addresses

### PR Checklist

- [ ] Code follows the project's coding standards
- [ ] All tests pass (`python -m unittest discover tests -v`)
- [ ] Documentation is updated (if applicable)
- [ ] Commit messages follow Conventional Commits
- [ ] No unrelated changes are included

### Review Process

- All PRs require at least one approving review before merge
- Maintainers may request changes — this is normal and collaborative
- Once approved, a maintainer will merge your PR

---

## 🙏 Thank You!

Your contributions make StackForge better. Whether it's a one-line fix or a brand new template, we appreciate your time and effort.

If you have questions, feel free to open a [Discussion](https://github.com/garvitagarwal9812/stackforge/discussions) or reach out at **garvit@stackforge.dev**.
