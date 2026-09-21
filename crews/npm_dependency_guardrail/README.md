# NPM Dependency Guardrail Crew

This example demonstrates how to use **CrewAI** combined with the **PkgDiet** evaluation engine to create a "Software Architect" agent that actively blocks deprecated or unhealthy npm packages before they are installed.

## Scenario
A team of AI coding agents often hallucinates legacy packages (like `request` or `moment`). Instead of allowing those into the codebase, we pass the package name to a strict "Architect Agent" equipped with PkgDiet.

The agent queries the registry, reads the health score and deprecation status, and dynamically suggests modern alternatives (like `undici` or `dayjs`) if the original package is blocked.

## Usage

1. Install requirements:
```bash
pip install crewai
```

2. Run the crew:
```bash
python main.py
```

*(Note: This example uses `subprocess` to call `npx pkgdiet` directly for zero-setup execution, but you can also connect to PkgDiet using CrewAI's native MCP support via `npx pkgdiet mcp`)*
