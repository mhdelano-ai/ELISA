"""The analysis entry point prints the gate quantities from a folder of results (simulated runs + templates)."""
import shutil
from pathlib import Path

from elisa_auto.analyze import analyze_folder, main
from elisa_auto.run_sim import parse_samples, simulate

AUTO = Path(__file__).resolve().parents[1]


def test_analyze_simulated_runs(tmp_path):
    res = simulate(AUTO / "config" / "cycle_primary.yaml",
                   parse_samples("blank:8,1:2,2:2,5:2,10:2,1000:1,blank:2"), tmp_path / "runs")
    assert all(r.status == "ok" for r in res)
    out = "\n".join(analyze_folder(tmp_path))
    assert "LOD (mean + 3 SD, docs/00)" in out and "carry-over" in out and "time to result max = 52.10" in out


def test_analyze_templates(tmp_path, capsys):
    for p in (AUTO / "templates").glob("*.csv"):
        shutil.copy(p, tmp_path / p.name)
    main([str(tmp_path), "--report"])
    out = capsys.readouterr().out
    assert "[U1] D1_Fab2_ALP: label factor" in out
    assert "[U3] HQDP 1 mM: free HQ" in out
    assert "[U2 BLI]" in out and "[E1.4] detection-on-capture ratio" in out
    assert "could not analyse" not in out
    assert (tmp_path / "analysis_report.md").exists()
