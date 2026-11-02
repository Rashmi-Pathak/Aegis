"""AEGIS Board Dossier & Global Trade War Simulation Test Suite."""
import pytest
from app.reporting.board_risk_dossier import BoardRiskDossierGenerator
from app.reporting.sec_10k_risk_factor_generator import SECRiskFactorDraftsman
from app.simulation.tariff_trade_war_simulation import TradeWarSimulationEngine
from app.simulation.panama_suez_simultaneous_blockade import DualCanalMaritimeBlockadeEngine
from app.synthetic.construction_megaproject_generator import ConstructionEPCGenerator

def test_board_dossier_generator():
    res = BoardRiskDossierGenerator.generate_board_pack(
        organization_name="PrimeLogix Global",
        industry="Freight Logistics",
        health_score=78.2,
        critical_risks=[{"title": "Fuel Spike", "category": "financial", "score": 85}],
        financial_kpis={"gross_revenue": "$148.2M"},
        stress_scenarios=[{"name": "Energy Crisis", "ebitda_impact_delta": "-$12M"}],
        decisions=[{"title": "Hedge Diesel", "cost": "$250K"}],
    )
    assert res["status"] == "RATIFIED_FOR_AUDIT_COMMITTEE"
    assert "BOARD AUDIT & RISK COMMITTEE DOSSIER" in res["markdown_content"]

def test_sec_10k_risk_factors():
    threats = [{"title": "Diesel Price Escalation", "category": "Supply Chain"}]
    res = SECRiskFactorDraftsman.draft_item_1a_disclosures("PrimeLogix Global", threats)
    assert res["disclosure_count"] == 1
    assert "Form 10-K" in res["document_title"]

def test_trade_war_simulation():
    res = TradeWarSimulationEngine.simulate_bilateral_tariff_shock(
        annual_import_volume_usd=50000000.0,
        annual_export_volume_usd=30000000.0,
        baseline_gross_margin_pct=15.0,
    )
    assert res["gross_tariff_duty_usd"] > 0
    assert res["total_annual_ebitda_erosion_usd"] > 0

def test_dual_canal_blockade():
    res = DualCanalMaritimeBlockadeEngine.simulate_dual_choke_point_shock(
        annual_container_teus=10000.0,
    )
    assert res["total_extra_transit_days_average"] > 10.0
    assert res["total_maritime_supply_chain_surcharge_usd"] > 0

def test_construction_epc():
    df = ConstructionEPCGenerator.generate_project_schedule()
    assert not df.empty
    assert "schedule_slip_days" in df.columns
