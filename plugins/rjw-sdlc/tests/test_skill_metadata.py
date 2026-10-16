"""Checks every skill in the plugin is loadable and discoverable by a harness.

A harness reads only the frontmatter to decide whether to load a skill, so the
description must state when to use it; the body's relative links must resolve
for progressive disclosure to work.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest


PLUGIN_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PLUGIN_DIR.parents[1]
SKILLS_DIR = PLUGIN_DIR / "skills"
MAX_DESCRIPTION_CHARS = 500
LINK_RE = re.compile(r"\]\(([^)#\s]+)(?:#[^)\s]*)?(?:\s+\"[^\"]*\")?\)")
# Fenced blocks and double-quoted spans hold text a skill writes into the target project.
TEMPLATE_RE = re.compile(r"```.*?```|\"[^\"\n]*\"", re.DOTALL)


def prose_links(text: str) -> list[str]:
    """Link targets, leaving out links that start inside template text."""
    template_spans = [m.span() for m in TEMPLATE_RE.finditer(text)]
    return [
        m.group(1)
        for m in LINK_RE.finditer(text)
        if not any(start <= m.start() < end for start, end in template_spans)
    ]


def skill_files() -> list[Path]:
    return sorted(SKILLS_DIR.glob("*/SKILL.md"))


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise AssertionError(f"{path} has no frontmatter")
    end = lines.index("---", 1)
    fields = {}
    for line in lines[1:end]:
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"')
    return fields


class FrontmatterTest(unittest.TestCase):
    def test_every_skill_directory_has_a_skill_file(self) -> None:
        directories = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
        self.assertEqual([p.parent for p in skill_files()], directories)

    def test_name_matches_directory(self) -> None:
        for path in skill_files():
            with self.subTest(skill=path.parent.name):
                self.assertEqual(frontmatter(path).get("name"), path.parent.name)

    def test_description_states_when_to_use(self) -> None:
        for path in skill_files():
            with self.subTest(skill=path.parent.name):
                description = frontmatter(path).get("description", "")
                self.assertTrue(description.startswith("Use when"), description)
                self.assertLessEqual(len(description), MAX_DESCRIPTION_CHARS)


class LinkTest(unittest.TestCase):
    def test_relative_links_resolve(self) -> None:
        for path in sorted(SKILLS_DIR.rglob("*.md")):
            for target in prose_links(path.read_text(encoding="utf-8")):
                if "://" in target:
                    continue
                with self.subTest(file=str(path.relative_to(SKILLS_DIR)), link=target):
                    self.assertTrue((path.parent / target).exists())

    def test_link_finder_keeps_titled_links_and_skips_template_text(self) -> None:
        text = '[a](titled.md "Title") [b](plain.md#part) "bullet: [c](template.md)"\n```\n[d](fenced.md)\n```'
        self.assertEqual(prose_links(text), ["titled.md", "plain.md"])


class ContentTest(unittest.TestCase):
    def test_helper_runs_through_uv_so_a_dropped_executable_bit_is_harmless(self) -> None:
        text = (SKILLS_DIR / "pr-shepherd" / "SKILL.md").read_text(encoding="utf-8")
        mentions = text.count("pr-shepherd.py")
        self.assertGreater(mentions, 0)
        self.assertEqual(text.count("uv run --script scripts/pr-shepherd.py"), mentions)

    def test_helper_keeps_no_state_under_a_literal_tmp(self) -> None:
        text = (SKILLS_DIR / "pr-shepherd" / "scripts" / "pr-shepherd.py").read_text(encoding="utf-8")
        self.assertNotIn("/tmp", text)

    def test_project_neutral_bodies_name_no_project_commands_paths_or_issues(self) -> None:
        neutral = {
            "testing/SKILL.md": [r"flotilla (artifact put|crew stall)", r"crates/", r"#\d+"],
            "consistency-review/SKILL.md": [r"(?i)\bgrill", r"(?i)\bflotilla\b", r"Scold", r"crates/", r"--include=\"\*\.rs\""],
        }
        for name, patterns in neutral.items():
            text = (SKILLS_DIR / name).read_text(encoding="utf-8")
            for pattern in patterns:
                with self.subTest(file=name, pattern=pattern):
                    self.assertIsNone(re.search(pattern, text))


class ManifestTest(unittest.TestCase):
    def test_marketplace_and_plugin_versions_agree(self) -> None:
        marketplace = json.loads((REPO_DIR / ".claude-plugin" / "marketplace.json").read_text())
        plugin = json.loads((PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text())
        listed = {p["name"]: p["version"] for p in marketplace["plugins"]}
        self.assertEqual(listed[plugin["name"]], plugin["version"])


if __name__ == "__main__":
    unittest.main()
