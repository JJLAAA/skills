import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_index.py"
SPEC = importlib.util.spec_from_file_location("audit_index", SCRIPT)
audit_index = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = audit_index
SPEC.loader.exec_module(audit_index)


def card(title: str, *, source: str = "source.md", extra: str = "") -> str:
    return f"""## {title}

- 核心判断：{title} 的核心判断。
- 适用场景：测试场景。
- 触发关键词：测试、{title}
- 开发时怎么用：执行对应动作。
- 常见反例：忽略边界。
- 来源文档：[来源]({source})
{extra}
"""


class AuditIndexTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "source.md").write_text("# source\n", encoding="utf-8")
        self.config = {
            "preamble_headings": ["使用方式"],
            "thresholds": {
                "card_chars_review": 300,
                "keyword_count_review": 4,
                "keyword_jaccard_review": 0.3,
            },
            "schedule": {"trigger_after_new_cards": 5, "trigger_growth_percent": 20},
        }

    def tearDown(self):
        self.temp.cleanup()

    def run_audit(self, text: str, *, evals=None, mode="full"):
        index = self.root / "关键认知索引.md"
        index.write_text("# 索引\n\n## 使用方式\n说明\n\n" + text, encoding="utf-8")
        return audit_index.audit(index, self.config, {}, evals or {"evals": []}, mode)

    def test_broken_source_is_p0(self):
        report = self.run_audit(card("失效来源", source="missing.md"), mode="quick")
        findings = {(item["severity"], item["kind"]) for item in report["findings"]}
        self.assertIn(("P0", "broken_source"), findings)

    def test_long_card_and_many_keywords_are_review_signals(self):
        text = card("膨胀卡片", extra="补充" * 200).replace("测试、膨胀卡片", "一、二、三、四、五")
        report = self.run_audit(text, mode="quick")
        kinds = {item["kind"] for item in report["findings"]}
        self.assertIn("long_card", kinds)
        self.assertIn("many_keywords", kinds)

    def test_unknown_eval_card_is_p1(self):
        evals = {
            "evals": [
                {
                    "id": "unknown",
                    "expected_cards": ["不存在的卡片"],
                    "must_not_trigger": [],
                }
            ]
        }
        report = self.run_audit(card("真实卡片"), evals=evals)
        findings = {(item["severity"], item["kind"]) for item in report["findings"]}
        self.assertIn(("P1", "unknown_eval_card"), findings)
        self.assertFalse(report["retrieval_eval"]["valid_references"])

    def test_keyword_overlap_only_creates_review_candidate(self):
        left = card("卡片甲").replace("测试、卡片甲", "索引、召回、边界")
        right = card("卡片乙").replace("测试、卡片乙", "索引、召回、治理")
        report = self.run_audit(left + "\n" + right)
        self.assertEqual(1, len(report["duplicate_candidates"]))
        self.assertFalse(any(item["kind"] == "duplicate_card" for item in report["findings"]))


if __name__ == "__main__":
    unittest.main()
