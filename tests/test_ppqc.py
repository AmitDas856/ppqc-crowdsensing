"""Offline tests: no Ethereum chain or GUI needed."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Homomorphic import decryptData, privacyData  # noqa: E402


@pytest.mark.parametrize("value", [0, 1, 37, 250, 512, 799])
def test_encrypt_then_decrypt_returns_the_location(value):
    assert decryptData(privacyData(value)) == value


def test_ciphertext_is_not_the_plain_value():
    c0, c1 = privacyData(123)
    assert len(c0) == 32 and len(c1) == 32
    assert list(c0) != [123] + [0] * 31


@pytest.fixture()
def ppqc(tmp_path, monkeypatch):
    monkeypatch.setenv("PPQC_LEDGER", str(tmp_path / "ledger.txt"))
    monkeypatch.setenv("PPQC_CHAIN_URL", "http://127.0.0.1:1")  # nothing listens here
    import importlib
    import PPQC
    return importlib.reload(PPQC)


def test_quality_check_rewards_accurate_reports(ppqc):
    noise, change = ppqc.quality_check(100, 200, 103, 204)
    assert noise == pytest.approx(5.0) and change == 1


def test_quality_check_penalises_noisy_reports(ppqc):
    noise, change = ppqc.quality_check(100, 200, 110, 200)
    assert noise == pytest.approx(10.0) and change == -1


def test_records_fall_back_to_local_ledger_without_a_chain(ppqc):
    assert ppqc.saveDataBlockChain("Participant ID : 3 Noise Value : 2.0\n") == "local file"
    assert ppqc.saveDataBlockChain("Participant ID : 4 Noise Value : 9.0\n") == "local file"
    assert "Participant ID : 4" in ppqc.readDetails()
    assert ppqc.storage_mode == "local file"
