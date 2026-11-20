import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { dirname, extname, isAbsolute, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const repositoryRoot = resolve(fileURLToPath(new URL("..", import.meta.url)));

function markdownFilesInWorktree() {
  return [
    ...new Set(
      execFileSync(
        "git",
        ["ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "*.md"],
        {
          cwd: repositoryRoot,
          encoding: "utf8",
        },
      )
        .split("\0")
        .filter(Boolean),
    ),
  ];
}

function withoutFencedCode(source) {
  let activeFence;

  return source
    .split(/\r?\n/u)
    .map((line) => {
      const fence = line.match(/^\s{0,3}(`{3,}|~{3,})/u)?.[1];
      if (!activeFence && fence) {
        activeFence = { character: fence[0], length: fence.length };
        return "";
      }
      if (
        activeFence &&
        fence?.[0] === activeFence.character &&
        fence.length >= activeFence.length
      ) {
        activeFence = undefined;
        return "";
      }
      return activeFence ? "" : line;
    })
    .join("\n");
}

function targetsIn(source) {
  const targets = [];
  const inlineLink = /!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)(?:\s+["'][^)\n]*)?\s*\)/gu;
  const referenceDefinition = /^\s{0,3}\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)/gmu;

  for (const pattern of [inlineLink, referenceDefinition]) {
    for (const match of source.matchAll(pattern)) {
      targets.push({
        line: source.slice(0, match.index).split("\n").length,
        target: match[1].replace(/^<|>$/gu, ""),
      });
    }
  }

  return targets;
}

function headingSlugs(markdownPath) {
  const slugs = new Set();
  const occurrences = new Map();
  const source = withoutFencedCode(readFileSync(markdownPath, "utf8"));
  const heading = /^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$/gmu;

  for (const match of source.matchAll(heading)) {
    const base = match[1]
      .replace(/!?\[([^\]]+)\]\([^)]*\)/gu, "$1")
      .replace(/<[^>]+>/gu, "")
      .replace(/[`*_~]/gu, "")
      .trim()
      .toLowerCase()
      .replace(/[^\p{L}\p{N}\p{M}\s_-]/gu, "")
      .replace(/\s/gu, "-");
    const count = occurrences.get(base) ?? 0;
    const slug = count === 0 ? base : `${base}-${count}`;
    occurrences.set(base, count + 1);
    slugs.add(slug);
  }

  return slugs;
}

function decoded(value) {
  try {
    return decodeURIComponent(value);
  } catch {
    return value;
  }
}

const failures = [];
let localTargetCount = 0;
const markdownFiles = markdownFilesInWorktree();

for (const sourceRelative of markdownFiles) {
  const sourcePath = resolve(repositoryRoot, sourceRelative);
  const source = withoutFencedCode(readFileSync(sourcePath, "utf8"));

  for (const { line, target } of targetsIn(source)) {
    if (/^[a-z]:[\\/]/iu.test(target) || /^file:/iu.test(target)) {
      failures.push(`${sourceRelative}:${line}: machine-local target is not portable: ${target}`);
      continue;
    }
    if (/^[a-z][a-z0-9+.-]*:/iu.test(target) || target.startsWith("//")) {
      continue;
    }

    localTargetCount += 1;
    const [rawPath, rawFragment = ""] = target.split("#", 2);
    const pathWithoutQuery = decoded(rawPath.split("?", 1)[0]);
    const targetPath = pathWithoutQuery
      ? pathWithoutQuery.startsWith("/")
        ? resolve(repositoryRoot, pathWithoutQuery.slice(1))
        : resolve(dirname(sourcePath), pathWithoutQuery)
      : sourcePath;
    const relativeTarget = relative(repositoryRoot, targetPath);

    if (
      relativeTarget === ".." ||
      relativeTarget.startsWith(`..${sep}`) ||
      isAbsolute(relativeTarget)
    ) {
      failures.push(`${sourceRelative}:${line}: target escapes the repository: ${target}`);
      continue;
    }
    if (!existsSync(targetPath)) {
      failures.push(`${sourceRelative}:${line}: target does not exist: ${target}`);
      continue;
    }

    if (rawFragment && extname(targetPath).toLowerCase() === ".md") {
      const fragment = decoded(rawFragment).toLowerCase();
      if (!headingSlugs(targetPath).has(fragment)) {
        failures.push(`${sourceRelative}:${line}: heading does not exist: ${target}`);
      }
    }
  }
}

if (failures.length > 0) {
  console.error(`Markdown link check failed with ${failures.length} error(s):`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exitCode = 1;
} else {
  console.log(
    `Markdown links valid: ${localTargetCount} local targets across ${markdownFiles.length} files.`,
  );
}
