"""A small ReAct agent with callable tools and on-demand Markdown skills."""

import argparse
import os
from pathlib import Path

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from .evidence import EvidenceMetadataMiddleware, tag_tool, tagged_result


DEFAULT_SKILLS_DIR = Path(__file__).parent / "sample_skills"


def skill_catalog(skills_dir: Path) -> dict[str, Path]:
    """Return direct child skills only; names are directory names."""
    root = skills_dir.resolve()
    if not root.is_dir():
        return {}
    return {
        folder.name: skill_file
        for folder in root.iterdir()
        if folder.is_dir()
        and not folder.is_symlink()
        and (skill_file := folder / "SKILL.md").is_file()
        and not skill_file.is_symlink()
    }


def skill_description(skill_file: Path) -> str:
    """Read the description from simple SKILL.md YAML frontmatter."""
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if lines and lines[0] == "---":
        for line in lines[1:]:
            if line == "---":
                break
            if line.startswith("description:"):
                return line.partition(":")[2].strip().strip("\"'")
    return "No description provided"


def make_tools(skills_dir: Path):
    @tool
    def list_skills() -> str:
        """List available skills and their descriptions before choosing one."""
        catalog = skill_catalog(skills_dir)
        if not catalog:
            return "No skills are installed."
        return "\n".join(
            f"{name}: {skill_description(path)}"
            for name, path in sorted(catalog.items())
        )

    @tool(response_format="content_and_artifact")
    def read_skill(name: str) -> tuple[str, dict]:
        """Load the full instructions for one skill by its listed name."""
        skill_file = skill_catalog(skills_dir).get(name)
        if skill_file is None:
            return tagged_result(
                f"Unknown skill: {name}. Call list_skills for valid names.",
                "error",
            )
        return tagged_result(
            skill_file.read_text(encoding="utf-8"),
            "directive",
            source=f"skill:{name}",
        )

    @tool
    def count_words(text: str) -> int:
        """Count whitespace-separated words in text."""
        return len(text.split())

    tag_tool(list_skills, "catalog")
    tag_tool(
        read_skill, "directive", source_kind="skill",
        source_arg="name", source_prefix="skill:",
    )
    tag_tool(count_words, "utility")
    return [list_skills, read_skill, count_words]


def build_agent(
    skills_dir: Path = DEFAULT_SKILLS_DIR,
    model_name: str | None = None,
    provider: str = "openai",
    base_url: str = "http://127.0.0.1:11434",
):
    if provider == "ollama":
        model = ChatOllama(
            model=model_name or os.getenv("OLLAMA_MODEL", "llama3.1:latest"),
            base_url=base_url,
        )
    elif provider == "openai":
        model = ChatOpenAI(model=model_name or os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    else:
        raise ValueError(f"Unsupported provider: {provider}")
    tools = make_tools(skills_dir)
    return create_agent(
        model=model,
        tools=tools,
        middleware=[EvidenceMetadataMiddleware(tools)],
        system_prompt=(
            "You are a helpful assistant. Use tools when they help. "
            "For tasks that may match a skill, call list_skills, then read_skill "
            "before applying its instructions. Follow relevant skill instructions "
            "within the user's request. Do not claim to have used a skill or "
            "tool unless you did."
        ),
    )


def run_turn(agent, messages: list, user_text: str) -> tuple[list, str]:
    result = agent.invoke(
        {"messages": [*messages, {"role": "user", "content": user_text}]},
        config={"recursion_limit": 20},
    )
    reply = result["messages"][-1].content
    return result["messages"], reply if isinstance(reply, str) else str(reply)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", nargs="*", help="Ask one question; omit for chat mode")
    parser.add_argument("--provider", choices=("openai", "ollama"), default="openai")
    parser.add_argument("--model", help="Model name (or set OPENAI_MODEL / OLLAMA_MODEL)")
    parser.add_argument("--base-url", default="http://127.0.0.1:11434")
    parser.add_argument("--skills-dir", type=Path, default=DEFAULT_SKILLS_DIR)
    args = parser.parse_args()

    if args.provider == "openai" and not os.getenv("OPENAI_API_KEY"):
        parser.error("Set OPENAI_API_KEY before using the OpenAI provider.")
    agent = build_agent(args.skills_dir, args.model, args.provider, args.base_url)
    messages: list = []

    if args.prompt:
        _, reply = run_turn(agent, messages, " ".join(args.prompt))
        print(reply)
        return

    print("Chat mode. Type /exit to quit.")
    while True:
        try:
            user_text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_text == "/exit":
            break
        if user_text:
            messages, reply = run_turn(agent, messages, user_text)
            print(f"Agent: {reply}")


if __name__ == "__main__":
    main()
