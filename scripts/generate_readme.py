#!/usr/bin/env python3
import pathlib
import subprocess

def get_last_commit_date(repo: pathlib.Path) -> str:
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cs"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()

def main():
    repo = pathlib.Path(__file__).resolve().parent.parent
    template_path = repo / "README.template.md"
    output_path = repo / "README.md"
    date = get_last_commit_date(repo)
    content = template_path.read_text(encoding="utf-8")
    content = content.replace("{{LAST_UPDATE}}", date)
    output_path.write_text(content, encoding="utf-8")

if __name__ == "__main__":
    main()
