"""Validation gates V1-V3, V6 — pinned reference cases per plan."""

from __future__ import annotations

from electicity_model.lcoe import LcoeInputs, annual_energy_mwh, lcoe, lcoh_pem, lcos


def test_v1_utility_solar_lcoe_within_irena_band():
    """Utility solar 25 yr, capex $1100/kW, opex $18/kW/yr, CF 0.22, r=0.07.
    IRENA RPGC 2023 global range: ~$30-60/MWh (LCOE).
    """
    capacity_kw = 1.0
    inputs = LcoeInputs(
        capex_total=1100 * capacity_kw,
        opex_yr=18 * capacity_kw,
        fuel_yr=0.0,
        energy_mwh_yr=annual_energy_mwh(capacity_kw, 0.22),
        lifetime_years=25,
        discount_rate=0.07,
    )
    result = lcoe(inputs)
    assert 30.0 <= result <= 60.0, f"V1 solar LCOE out of band: {result:.2f} USD/MWh"


def test_v2_pem_electrolyzer_lcoh_unsubsidised():
    """PEM @ $1500/kW, $30/MWh power, eff 0.60 LHV, CF 0.50, 20 yr, r=0.08.
    IEA GHR 2024 green H2 range: ~$4-7/kg in 2023; subset $4-6 for these inputs.
    """
    result = lcoh_pem(
        electrolyzer_capex_per_kw=1500,
        electrolyzer_kw=1.0,
        electrolyzer_opex_per_kw_yr=45,
        electricity_price_per_mwh=30.0,
        efficiency_lhv=0.60,
        capacity_factor=0.50,
        lifetime_years=20,
        discount_rate=0.08,
    )
    assert 4.0 <= result <= 6.0, f"V2 LCOH unsubsidised out of band: {result:.2f} USD/kg"


def test_v3_pem_electrolyzer_lcoh_with_45v_credit():
    """V2 inputs minus full IRA 45V credit ($3/kg). Result must land in $1-3/kg net."""
    result = lcoh_pem(
        electrolyzer_capex_per_kw=1500,
        electrolyzer_kw=1.0,
        electrolyzer_opex_per_kw_yr=45,
        electricity_price_per_mwh=30.0,
        efficiency_lhv=0.60,
        capacity_factor=0.50,
        lifetime_years=20,
        discount_rate=0.08,
        ira_45v_credit_per_kg=3.0,
    )
    assert 1.0 <= result <= 3.0, f"V3 LCOH with 45V out of band: {result:.2f} USD/kg"


def test_v6_pumped_hydro_lcos_within_atb_band():
    """PHES, 100 MWh / 10 MW (10 h), 250 cycles/yr, $30/MWh charge, 50 yr, r=0.07.
    NREL ATB 2024 long-duration storage LCOS range ~$150-250/MWh.
    """
    result = lcos(
        capex_per_kwh=130,
        capacity_kwh=100_000,
        capex_per_kw=1800,
        capacity_kw=10_000,
        opex_per_kw_yr=25,
        cycles_per_year=250,
        roundtrip_efficiency=0.78,
        charge_electricity_price_per_mwh=30.0,
        lifetime_years=50,
        discount_rate=0.07,
    )
    assert 150.0 <= result <= 250.0, f"V6 PHES LCOS out of band: {result:.2f} USD/MWh"
