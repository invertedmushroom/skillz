# /// script
# requires-python = ">=3.10"
# dependencies = ["PyYAML==6.0.3"]
# ///
"""Read-only checks for the template's skill files, not live harness discovery."""

import argparse
import re
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


class UniqueKeysLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str):
            raise ValueError("YAML mapping keys must be strings")
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node)
    return result


UniqueKeysLoader.add_constructor("tag:yaml.org,2002:map", unique_mapping)


def load_mapping(text):
    value = yaml.load(text, Loader=UniqueKeysLoader)
    if not isinstance(value, dict):
        raise ValueError("expected a YAML mapping")
    return value


def check_openai(data, frontmatter):
    """Check the adapter fields used here, not the full vendor schema."""
    unknown = data.keys() - {"interface", "policy", "dependencies"}
    if unknown:
        raise ValueError(f"unsupported OpenAI adapter fields: {sorted(unknown)}")
    for section in data:
        if not isinstance(data[section], dict):
            raise ValueError(f"{section} must be a mapping")
    interface = data.get("interface", {})
    if any(not isinstance(value, str) for value in interface.values()):
        raise ValueError("interface values must be strings")
    if "short_description" in interface:
        if not 25 <= len(interface["short_description"]) <= 64:
            raise ValueError("interface.short_description must have 25–64 characters")
    if "default_prompt" in interface and frontmatter:
        if f"${frontmatter['name']}" not in interface["default_prompt"]:
            raise ValueError("interface.default_prompt must mention $skill-name")
    implicit = data.get("policy", {}).get("allow_implicit_invocation", True)
    if not isinstance(implicit, bool):
        raise ValueError("policy.allow_implicit_invocation must be a boolean")
    if frontmatter and "disable-model-invocation" in frontmatter:
        if implicit != (not frontmatter["disable-model-invocation"]):
            raise ValueError("invocation policy contradicts explicit frontmatter policy")


def validate(root):
    errors = []
    stats = dict(skills=0, adapters=0, links=0, metadata_bytes=0, entrypoint_bytes=0)
    skills = sorted((root / ".agents/skills").glob("*/SKILL.md"))
    skills_root = root / ".agents/skills"
    if skills_root.is_dir():
        for directory in sorted(skills_root.iterdir()):
            if directory.is_dir() and not (directory / "SKILL.md").is_file():
                errors.append(f"{directory.relative_to(root)}: missing SKILL.md")
    if not skills:
        errors.append(".agents/skills: no skill entrypoints found")
    for path in skills:
        stats["skills"] += 1
        stats["entrypoint_bytes"] += path.stat().st_size
        frontmatter = None
        try:
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines()
            if not lines or lines[0] != "---":
                raise ValueError("missing opening frontmatter delimiter")
            end = lines.index("---", 1)
            frontmatter = load_mapping("\n".join(lines[1:end]))
            name = frontmatter.get("name")
            if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                raise ValueError("name must be lowercase hyphen-case")
            if name != path.parent.name or len(name) > 64:
                raise ValueError("name must match its directory and have at most 64 characters")
            description = frontmatter.get("description")
            if not isinstance(description, str) or not description.strip() or len(description) > 1024:
                raise ValueError("description must be a nonempty string of at most 1024 characters")
            if "disable-model-invocation" in frontmatter:
                if not isinstance(frontmatter["disable-model-invocation"], bool):
                    raise ValueError("disable-model-invocation must be a boolean")
            stats["metadata_bytes"] += len((name + description).encode("utf-8"))
            for doc in sorted(path.parent.rglob("*.md")):
                body = "\n".join(lines[end + 1:]) if doc == path else doc.read_text(encoding="utf-8")
                body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
                for href in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", body):
                    target = urlsplit(href)
                    if target.scheme or target.netloc or not target.path:
                        continue
                    stats["links"] += 1
                    if not (doc.parent / unquote(target.path)).is_file():
                        errors.append(f"{doc.relative_to(root)}: missing linked file: {href}")
        except (OSError, ValueError, yaml.YAMLError) as error:
            errors.append(f"{path.relative_to(root)}: {error}")
            frontmatter = None
        for adapter in sorted((path.parent / "agents").glob("*")):
            if not adapter.is_file() or adapter.suffix not in {".yaml", ".yml"}:
                continue
            stats["adapters"] += 1
            try:
                data = load_mapping(adapter.read_text(encoding="utf-8"))
                if adapter.name == "openai.yaml":
                    check_openai(data, frontmatter)
            except (OSError, ValueError, yaml.YAMLError) as error:
                errors.append(f"{adapter.relative_to(root)}: {error}")
    return errors, stats


def self_test():
    with tempfile.TemporaryDirectory(prefix="template-skills-") as directory:
        root = Path(directory)
        skill = root / ".agents/skills/example"
        (skill / "agents").mkdir(parents=True)
        entry = skill / "SKILL.md"
        adapter = skill / "agents/openai.yaml"
        valid = (
            "---\nname: example\ndescription: Example workflow.\n---\n[Guide](guide.md)\n\n"
            "```markdown\n[Illustrative only](fenced-example.md)\n```\n"
        )
        native = 'interface:\n  short_description: "A useful example workflow for validation"\n'
        entry.write_text(valid, encoding="utf-8")
        adapter.write_text(native, encoding="utf-8")
        (skill / "guide.md").write_text("Evidence", encoding="utf-8")
        (skill / "notes.md").write_text("[Entry](SKILL.md)\n", encoding="utf-8")
        before = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
        if validate(root)[0] or before != {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}:
            raise RuntimeError("valid fixture failed or validation changed its files")
        cases = [
            (entry, valid.replace("Example workflow.", "Triggers on: example")),
            (entry, valid.replace("guide.md", "missing.md")),
            (entry, valid.replace("name: example", "name: different")),
            (entry, valid.replace("name: example", "name: example\nname: example")),
            (entry, valid.replace("description:", "disable-model-invocation: true\ndescription:")),
            (adapter, "name: example\nmodel_invocation: true\n"),
            (adapter, native + 'policy:\n  allow_implicit_invocation: "false"\n'),
            (skill / "notes.md", "[Broken](nope.md)\n"),
        ]
        for path, broken in cases:
            original = path.read_text(encoding="utf-8")
            path.write_text(broken, encoding="utf-8")
            if not validate(root)[0]:
                raise RuntimeError(f"invalid fixture passed: {broken!r}")
            path.write_text(original, encoding="utf-8")
        if not validate(root / "absent")[0]:
            raise RuntimeError("empty discovery passed")
        (root / ".agents/skills/incomplete").mkdir()
        if not validate(root)[0]:
            raise RuntimeError("skill directory without an entrypoint passed")
    print("PASS: valid read-only fixture and 10 failing fixtures")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--self-test", action="store_true", help="also exercise valid and invalid temporary fixtures")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    root = args.root.resolve()
    errors, stats = validate(root)
    for error in errors:
        print(f"FAIL: {error}")
    print(f"{'FAIL' if errors else 'PASS'}: {stats['skills']} skills, {stats['adapters']} adapter YAML files, {stats['links']} local links")
    instructions = root / "AGENTS.md"
    print(f"Inventory bytes: AGENTS.md={instructions.stat().st_size if instructions.exists() else 0}, name+description={stats['metadata_bytes']}, full entrypoints={stats['entrypoint_bytes']}")
    print("Live harness discovery: NOT RUN. Inventory bytes are not session token counts.")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
