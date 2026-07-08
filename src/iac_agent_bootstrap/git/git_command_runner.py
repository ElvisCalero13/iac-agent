import subprocess
from pathlib import Path


class GitCommandRunner:
    def run(
        self,
        command: list[str],
        cwd: Path,
        timeout: int = 180,
    ) -> dict:
        result = subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Command failed: {' '.join(command)}\n"
                f"{result.stderr}"
            )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }