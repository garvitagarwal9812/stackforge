# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | ✅ Active support  |
| < 1.0   | ❌ Not supported   |

## Reporting a Vulnerability

We take the security of StackForge seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, please send an email to **garvit@stackforge.dev** with:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Impact assessment** — what could an attacker do?
4. **Suggested fix** (if you have one)

### What to Expect

- **Acknowledgment** within 48 hours of your report
- **Assessment** and severity rating within 1 week
- **Fix timeline** communicated based on severity:
  - 🔴 **Critical**: Patch within 48 hours
  - 🟠 **High**: Patch within 1 week
  - 🟡 **Medium**: Patch within 2 weeks
  - 🟢 **Low**: Addressed in next release

### Scope

The following are in scope for security reports:

- Code injection via generated templates
- Path traversal in file generation
- Dependency vulnerabilities in bundled packages
- Arbitrary code execution through config files

### Recognition

We believe in recognizing security researchers. With your permission, we will:
- Credit you in the security advisory
- Add your name to our security hall of fame

Thank you for helping keep StackForge and its users safe! 🛡️
