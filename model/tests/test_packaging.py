"""Grant-packaging tests: archive creation, manifest, sha256 stability, CSV fallback."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest

from electicity_model.packaging import (
    PACKAGE_MANIFESTS,
    available_schemes,
    package_grant,
)


def test_available_schemes_complete():
    schemes = available_schemes()
    assert set(schemes) == set(PACKAGE_MANIFESTS)
    assert "horizon_europe" in schemes
    assert "arpa_e" in schemes


def test_unknown_scheme_raises():
    with pytest.raises(ValueError, match="unknown scheme"):
        package_grant("atlantis_council", Path("/tmp"))


@pytest.mark.parametrize("scheme", sorted(PACKAGE_MANIFESTS))
def test_package_creates_archive(scheme, tmp_path):
    archive = package_grant(scheme, tmp_path)
    assert archive.exists()
    assert archive.suffix == ".zip"
    with zipfile.ZipFile(archive) as zf:
        names = set(zf.namelist())
    assert "manifest.json" in names
    for f in PACKAGE_MANIFESTS[scheme]:
        assert f in names


def test_manifest_lists_every_file_with_sha(tmp_path):
    archive = package_grant("horizon_europe", tmp_path)
    with zipfile.ZipFile(archive) as zf:
        manifest = json.loads(zf.read("manifest.json"))
    files = {entry["path"] for entry in manifest["files"]}
    for required in PACKAGE_MANIFESTS["horizon_europe"]:
        assert required in files
    for entry in manifest["files"]:
        assert "sha256" in entry
        assert len(entry["sha256"]) == 64
        assert entry["size_bytes"] > 0


def test_budget_present_csv_or_xlsx(tmp_path):
    archive = package_grant("arpa_e", tmp_path)
    with zipfile.ZipFile(archive) as zf:
        names = zf.namelist()
        budget = [n for n in names if n.startswith("budget_")]
    assert len(budget) == 1
    assert budget[0].endswith((".xlsx", ".csv"))


def test_total_usd_override_propagates(tmp_path):
    archive = package_grant("horizon_europe", tmp_path, total_usd=12_345_678)
    with zipfile.ZipFile(archive) as zf:
        manifest = json.loads(zf.read("manifest.json"))
    assert manifest["total_usd"] == 12_345_678


def test_archive_contents_byte_identical_for_same_inputs(tmp_path):
    a = package_grant("eeca_callaghan", tmp_path / "a")
    b = package_grant("eeca_callaghan", tmp_path / "b")
    with zipfile.ZipFile(a) as za, zipfile.ZipFile(b) as zb:
        for n in za.namelist():
            if n == "manifest.json":
                # manifest.json carries today's date which is identical for the same run
                continue
            assert za.read(n) == zb.read(n), f"file {n} differs across runs"


def test_disclaimer_included_in_every_package(tmp_path):
    for scheme in available_schemes():
        archive = package_grant(scheme, tmp_path / scheme)
        with zipfile.ZipFile(archive) as zf:
            assert "DISCLAIMER.md" in zf.namelist()
