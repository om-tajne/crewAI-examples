from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
import subprocess

class PkgDietTool(BaseTool):
    name: str = "PkgDiet Dependency Checker"
    description: str = "Checks an npm package for health, deprecation, and size before installation. Returns ALLOW, WARN, or BLOCK."
    
    def _run(self, package_name: str) -> str:
        try:
            # Note: CrewAI also supports loading PkgDiet natively via its MCP integration 
            # (`npx -y pkgdiet@2.0.1 mcp`), but we wrap the CLI here for zero-setup execution.
            result = subprocess.run(
                ["npx", "-y", "pkgdiet@2.0.1", "check", package_name],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except Exception as e:
            return f"Error checking package: {str(e)}"

# Agent
architect = Agent(
    role='Senior Software Architect',
    goal='Evaluate npm dependencies for technical debt and security risks before allowing them in the codebase.',
    backstory='You are a strict architect who ensures no deprecated or heavy packages enter the project.',
    verbose=True,
    allow_delegation=False,
    tools=[PkgDietTool()]
)

# Task
evaluate_task = Task(
    description='Evaluate the "request" and "moment" npm packages using your tool. If they are blocked, suggest modern alternatives.',
    expected_output='A markdown report detailing the health of the packages and any recommended replacements.',
    agent=architect
)

# Crew
crew = Crew(
    agents=[architect],
    tasks=[evaluate_task],
    process=Process.sequential
)

if __name__ == "__main__":
    print("Starting Dependency Guardrail Crew...")
    result = crew.kickoff()
    print("\n######################")
    print("FINAL REPORT:")
    print("######################\n")
    print(result)
