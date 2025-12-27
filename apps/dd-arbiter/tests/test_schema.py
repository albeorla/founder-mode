"""Tests for DD-Arbiter domain schemas."""

import pytest

from ddarbiter.domain.schema import Claim, DiligenceReport, Disagreement, UncertaintyResult


class TestClaim:
    """Tests for Claim schema."""

    def test_claim_creation(self):
        """Test basic claim creation."""
        claim = Claim(
            text="Revenue grew 15% YoY",
            confidence=0.85,
            supporting_models=["gpt-4o", "claude-3-5-sonnet"],
            contradicting_models=[],
        )
        assert claim.text == "Revenue grew 15% YoY"
        assert claim.confidence == 0.85
        assert len(claim.supporting_models) == 2

    def test_claim_confidence_bounds(self):
        """Test confidence must be between 0 and 1."""
        with pytest.raises(ValueError):
            Claim(text="Test", confidence=1.5)

        with pytest.raises(ValueError):
            Claim(text="Test", confidence=-0.1)


class TestDisagreement:
    """Tests for Disagreement schema."""

    def test_disagreement_creation(self):
        """Test basic disagreement creation."""
        disagreement = Disagreement(
            claim_1={"model": "gpt-4o", "role": "bull", "claim": "Revenue growing"},
            claim_2={"model": "claude", "role": "bear", "claim": "Revenue declining"},
            disagreement_type="contradiction",
            severity="high",
        )
        assert disagreement.severity == "high"
        assert disagreement.disagreement_type == "contradiction"


class TestUncertaintyResult:
    """Tests for UncertaintyResult schema."""

    def test_uncertainty_result_creation(self):
        """Test basic uncertainty result creation."""
        result = UncertaintyResult(
            answer="The company shows moderate growth potential",
            confidence=0.72,
            semantic_entropy=0.45,
            consistency_score=0.80,
            num_semantic_clusters=2,
            verbalized_confidence_avg=78.5,
        )
        assert result.confidence == 0.72
        assert result.num_semantic_clusters == 2


class TestDiligenceReport:
    """Tests for DiligenceReport schema."""

    def test_diligence_report_creation(self):
        """Test basic report creation."""
        report = DiligenceReport(
            thesis_confidence_score=72.5,
            executive_summary="The investment shows promise but requires verification.",
            consensus_claims=[
                Claim(text="Market is growing", confidence=0.9),
            ],
            disputed_claims=[
                Claim(text="Margins sustainable", confidence=0.5),
            ],
            key_risks=["Regulatory uncertainty", "Competition"],
            deal_breakers=[],
            diligence_questions=["What is the customer concentration?"],
            needs_human_review=True,
            review_reason="High uncertainty on margin sustainability",
        )
        assert report.thesis_confidence_score == 72.5
        assert len(report.key_risks) == 2
        assert report.needs_human_review is True

    def test_thesis_confidence_bounds(self):
        """Test thesis confidence must be between 0 and 100."""
        with pytest.raises(ValueError):
            DiligenceReport(
                thesis_confidence_score=150,
                executive_summary="Test",
                needs_human_review=False,
            )
