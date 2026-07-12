#!/usr/bin/env python3
"""Deterministic audit for a Markdown key-knowledge index.

The script deliberately limits itself to mechanical evidence. Semantic claims,
source fidelity, contradictions, and retrieval quality remain review tasks in
SKILL.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import unquote


FIELD_PATTERN = re.compile(
    r"^-\s*(核心判断|适用场景|触发关键词|开发时怎么用|常见反例|来源文档)\s*[：:]\s*(.*)$"
)
HEADING_PATTERN = re.compile(r"^##\s+(.+?)\s*$")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REQUIRED_FIELDS = (
    "核心判断",
    "适用场景",
    "触发关键词",
    "开发时怎么用",
    "常见反例",
    "来源文档",
)
SEVERITY_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


@dataclass
class Card:
    title: str
    start_line: int
    end_line: int
    char_count: int
    fields: dict[str, str]
    keywords: list[str]


@dataclass
class Finding:
    severity: str
    kind: str
    card: str
    evidence: str
    recommendation: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", default="关键认知索引.md")
    parser.add_argument("--config", default=".wiki-audit/config.json")
    parser.add_argument("--baseline", default=".wiki-audit/baseline.json")
    parser.add_argument("--evals", default=".wiki-audit/retrieval-evals.json")
    parser.add_argument("--mode", choices=("quick", "full"), default="full")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", help="Write report to this path instead of stdout")
    parser.add_argument("--update-baseline", action="store_true")
    parser.add_argument("--fail-on", choices=("P0", "P1", "P2", "P3"))
    return parser.parse_args()


def load_json(path: Path, *, required: bool) -> dict[str, Any]:
    if not path.exists():
        if required:
            raise ValueError(f"required file does not exist: {path}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def parse_cards(index_path: Path, preamble_headings: list[str]) -> tuple[str, list[Card]]:
    text = index_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    headings: list[tuple[int, str]] = []
    for idx, line in enumerate(lines):
        match = HEADING_PATTERN.match(line)
        if match and match.group(1) not in preamble_headings:
            headings.append((idx, match.group(1)))

    cards: list[Card] = []
    for position, (start, title) in enumerate(headings):
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        block = lines[start:end]
        fields: dict[str, str] = {}
        for line in block[1:]:
            match = FIELD_PATTERN.match(line.strip())
            if match:
                fields[match.group(1)] = match.group(2).strip()
        keywords = split_keywords(fields.get("触发关键词", ""))
        cards.append(
            Card(
                title=title,
                start_line=start + 1,
                end_line=end,
                char_count=len("\n".join(block)),
                fields=fields,
                keywords=keywords,
            )
        )
    return text, cards


def split_keywords(value: str) -> list[str]:
    value = value.rstrip("。.;；")
    return [part.strip(" `\t") for part in re.split(r"[、,，；;]", value) if part.strip(" `\t")]


def resolve_local_link(index_path: Path, raw_target: str) -> Path | None:
    target = raw_target.split("#", 1)[0]
    if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", target):
        return None
    return (index_path.parent / unquote(target)).resolve()


def jaccard(left: list[str], right: list[str]) -> float:
    a = {item.casefold() for item in left}
    b = {item.casefold() for item in right}
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def audit(
    index_path: Path,
    config: dict[str, Any],
    baseline: dict[str, Any],
    retrieval_evals: dict[str, Any],
    mode: str,
) -> dict[str, Any]:
    thresholds = config.get("thresholds", {})
    preamble = config.get("preamble_headings", ["使用方式"])
    text, cards = parse_cards(index_path, preamble)
    findings: list[Finding] = []

    title_counts: dict[str, int] = {}
    for card in cards:
        title_counts[card.title] = title_counts.get(card.title, 0) + 1
        missing = [field for field in REQUIRED_FIELDS if not card.fields.get(field)]
        if missing:
            findings.append(Finding("P1", "missing_fields", card.title, f"缺少字段：{', '.join(missing)}", "补齐卡片契约字段"))

        max_chars = int(thresholds.get("card_chars_review", 1200))
        if card.char_count > max_chars:
            findings.append(Finding("P2", "long_card", card.title, f"{card.char_count} 字符，审查阈值 {max_chars}", "检查是否应缩短、拆分或下沉专题页"))

        max_keywords = int(thresholds.get("keyword_count_review", 20))
        if len(card.keywords) > max_keywords:
            findings.append(Finding("P2", "many_keywords", card.title, f"{len(card.keywords)} 个关键词，审查阈值 {max_keywords}", "删除泛词并重写任务触发边界"))

        for target in LINK_PATTERN.findall(card.fields.get("来源文档", "")):
            resolved = resolve_local_link(index_path, target)
            if resolved is not None and not resolved.exists():
                findings.append(Finding("P0", "broken_source", card.title, f"来源不存在：{target}", "修复来源链接或重新核验核心判断"))

    for title, count in title_counts.items():
        if count > 1:
            findings.append(Finding("P1", "duplicate_title", title, f"同名卡片 {count} 张", "合并卡片或重写独立边界"))

    eval_summary = {"eval_count": 0, "valid_references": True}
    if mode == "full":
        eval_items = retrieval_evals.get("evals", [])
        if not isinstance(eval_items, list):
            findings.append(Finding("P1", "invalid_eval_schema", "retrieval eval", "evals 必须是数组", "修复 retrieval-evals.json"))
            eval_items = []
        eval_summary["eval_count"] = len(eval_items)
        known_titles = set(title_counts)
        for item in eval_items:
            if not isinstance(item, dict):
                findings.append(Finding("P1", "invalid_eval_schema", "retrieval eval", "eval 条目必须是对象", "修复 retrieval-evals.json"))
                eval_summary["valid_references"] = False
                continue
            eval_id = str(item.get("id", "missing-id"))
            referenced = item.get("expected_cards", []) + item.get("must_not_trigger", [])
            unknown = [title for title in referenced if title not in known_titles]
            if unknown:
                findings.append(Finding("P1", "unknown_eval_card", f"retrieval eval:{eval_id}", f"引用不存在的卡片：{', '.join(unknown)}", "改为真实卡片标题或补齐受来源支持的卡片"))
                eval_summary["valid_references"] = False

    duplicate_candidates: list[dict[str, Any]] = []
    if mode == "full":
        threshold = float(thresholds.get("keyword_jaccard_review", 0.35))
        for left_index, left in enumerate(cards):
            for right in cards[left_index + 1 :]:
                score = jaccard(left.keywords, right.keywords)
                if score >= threshold:
                    duplicate_candidates.append(
                        {
                            "left": left.title,
                            "right": right.title,
                            "keyword_jaccard": round(score, 3),
                            "shared_keywords": sorted(set(left.keywords) & set(right.keywords)),
                            "review": "只作为语义复核候选，不能据此自动合并",
                        }
                    )

    baseline_cards = baseline.get("card_count")
    baseline_chars = baseline.get("index_chars")
    delta = {
        "card_count": len(cards) - baseline_cards if isinstance(baseline_cards, int) else None,
        "index_chars": len(text) - baseline_chars if isinstance(baseline_chars, int) else None,
        "growth_percent": None,
    }
    if isinstance(baseline_chars, int) and baseline_chars > 0:
        delta["growth_percent"] = round((len(text) - baseline_chars) / baseline_chars * 100, 2)

    trigger_growth = float(config.get("schedule", {}).get("trigger_growth_percent", 20))
    if delta["growth_percent"] is not None and delta["growth_percent"] > trigger_growth:
        findings.append(Finding("P2", "growth_trigger", "整个索引", f"相比基线增长 {delta['growth_percent']}%，触发阈值 {trigger_growth}%", "执行完整语义审计与召回测试"))

    trigger_cards = int(config.get("schedule", {}).get("trigger_after_new_cards", 5))
    if delta["card_count"] is not None and delta["card_count"] >= trigger_cards:
        findings.append(Finding("P2", "new_cards_trigger", "整个索引", f"相比基线新增 {delta['card_count']} 张卡片，触发阈值 {trigger_cards}", "执行完整语义审计与召回测试"))

    finding_counts = {severity: sum(1 for finding in findings if finding.severity == severity) for severity in SEVERITY_RANK}
    status = "healthy"
    if finding_counts["P0"] or finding_counts["P1"]:
        status = "serious_findings"
    elif finding_counts["P2"] or finding_counts["P3"] or duplicate_candidates:
        status = "review_needed"

    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "index": str(index_path),
        "status": status,
        "summary": {
            "card_count": len(cards),
            "index_chars": len(text),
            "finding_counts": finding_counts,
            "duplicate_candidate_count": len(duplicate_candidates),
            "baseline_delta": delta,
        },
        "findings": [asdict(finding) for finding in findings],
        "duplicate_candidates": duplicate_candidates,
        "retrieval_eval": eval_summary,
        "cards": [asdict(card) for card in cards],
        "semantic_checks_pending": [
            "候选卡片是否表达相同实际行动",
            "来源正文是否支撑核心判断",
            "卡片之间及卡片与来源之间是否矛盾",
            "retrieval eval 是否命中预期卡片且避免误召回",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    counts = summary["finding_counts"]
    lines = [
        "# Wiki Index Audit",
        "",
        f"- 审计模式：{report['mode']}",
        f"- 卡片数量：{summary['card_count']}",
        f"- 索引字符数：{summary['index_chars']}",
        f"- 结论：{report['status']}",
        f"- Findings：P0={counts['P0']}，P1={counts['P1']}，P2={counts['P2']}，P3={counts['P3']}",
        "",
        "## 确定性检查发现",
        "",
        "| 严重度 | 卡片 | 问题 | 证据 | 建议动作 |",
        "|---|---|---|---|---|",
    ]
    if report["findings"]:
        for finding in report["findings"]:
            lines.append(
                f"| {finding['severity']} | {finding['card']} | {finding['kind']} | {finding['evidence']} | {finding['recommendation']} |"
            )
    else:
        lines.append("| - | - | 未发现机械问题 | 已检查字段、标题、来源链接、规模与基线变化 | - |")
    lines.extend(["", "## 候选语义复核", ""])
    if report["duplicate_candidates"]:
        for candidate in report["duplicate_candidates"]:
            lines.append(
                f"- `{candidate['left']}` ↔ `{candidate['right']}`：关键词 Jaccard={candidate['keyword_jaccard']}；需人工判断实际行动是否相同。"
            )
    else:
        lines.append("- 未发现达到配置阈值的关键词重叠候选。")
    lines.extend(["", "## 尚需完成的语义检查", ""])
    lines.extend(f"- {item}" for item in report["semantic_checks_pending"])
    return "\n".join(lines) + "\n"


def write_baseline(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    summary = report["summary"]
    baseline = {
        "schema_version": 1,
        "updated_at": report["generated_at"],
        "index": report["index"],
        "card_count": summary["card_count"],
        "index_chars": summary["index_chars"],
        "status_at_update": report["status"],
        "finding_counts_at_update": summary["finding_counts"],
        "duplicate_candidate_count_at_update": summary["duplicate_candidate_count"],
    }
    path.write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    index_path = Path(args.index).resolve()
    config_path = Path(args.config).resolve()
    baseline_path = Path(args.baseline).resolve()
    evals_path = Path(args.evals).resolve()
    try:
        if not index_path.exists():
            raise ValueError(f"index does not exist: {index_path}")
        config = load_json(config_path, required=True)
        baseline = load_json(baseline_path, required=False)
        retrieval_evals = load_json(evals_path, required=args.mode == "full")
        report = audit(index_path, config, baseline, retrieval_evals, args.mode)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

    if args.update_baseline:
        write_baseline(baseline_path, report)

    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else render_markdown(report)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    else:
        print(output, end="")

    if args.fail_on:
        threshold = SEVERITY_RANK[args.fail_on]
        if any(SEVERITY_RANK[item["severity"]] <= threshold for item in report["findings"]):
            return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
