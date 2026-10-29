import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import jd_prescan as jp  # noqa: E402
import keyword_delta as kd  # noqa: E402
import output_name as on  # noqa: E402

JD = """Machine Learning Engineer
Responsibilities:
- Build RAG pipelines in Python on AWS
Basic Qualifications:
- Python and SQL; Kubernetes a plus
- Familiarity with Spark
Preferred Qualifications:
- LangGraph
Equal Opportunity
- Java is mentioned here and must be skipped
"""


def draft():
    a = jp.analyze(JD, jp.load_terms())
    return jp.build_draft(a, {"python", "sql", "rag", "langgraph"}, {jp.norm_key("Spark"), jp.norm_key("Kubernetes")})


def test_sections_and_gaps():
    d = draft()
    assert "Python" in d["required_skills"] and "SQL" in d["required_skills"]
    assert "LangGraph" in d["preferred_skills"]
    assert set(d["gaps_to_state_plainly"]) == {"Spark", "Kubernetes"}
    assert "Java" not in [t["name"] for t in d["terms"]]  # EEO section skipped


def test_gap_never_counts_toward_coverage():
    d = draft()
    scored = [t for t in d["terms"] if t["claim_status"] != "gap"]
    assert all(t["name"] not in {"Spark", "Kubernetes"} for t in scored)
    assert kd.coverage(scored, "Machine Learning Python SQL RAG LangGraph AWS")["pct"] == 100


def test_plain_text_strips_latex():
    assert "Python" in kd.plain_text(r"\begin{document}\textbf{Python} \& SQL % hidden")
    assert "hidden" not in kd.plain_text("\\begin{document}x % hidden")


def test_short_terms_case_sensitive():
    names = [t["name"] for t in jp.analyze("ML Engineer\n- we use go every day\n- Go and C", jp.load_terms())["terms"]]
    assert "Go" in names and names.count("Go") == 1


def test_output_name():
    assert on.file_base("Yogvid Wankhede", "Study.com") == "Yogvid_Wankhede_Resume_Study.com"
    assert on.file_base("Yogvid Wankhede", "Ünï Corp", "CoverLetter") == "Yogvid_Wankhede_CoverLetter_Uni-Corp"


def test_cli_roundtrip(tmp_path):
    jd = tmp_path / "jd.txt"; jd.write_text(JD)
    out = tmp_path / "p.json"
    subprocess.run([sys.executable, str(ROOT / "scripts/jd_prescan.py"), "--jd", str(jd), "--out", str(out)], check=True, capture_output=True)
    assert json.loads(out.read_text())["role_title"] == "Machine Learning Engineer"
