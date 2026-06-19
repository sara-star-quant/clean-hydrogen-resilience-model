"""LCOE / LCOH / LCOS, discounted-cash-flow form following the IEA/IRENA convention.

LCOE = sum_t [(CapEx_t + OpEx_t + Fuel_t) / (1+r)^t]
       /  sum_t [E_t / (1+r)^t]

CapEx is booked at t=0 unless a construction profile is passed in.
"""

from __future__ import annotations

from dataclasses import dataclass

from .constants import H2_LHV_KWH_PER_KG, HOURS_PER_YEAR

__all__ = [
    "LcoeInputs",
    "lcoe",
    "lcoh_pem",
    "lcos",
    "capacity_cost_to_capex",
    "annual_energy_mwh",
]
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


@dataclass(frozen=True, slots=True)
class LcoeInputs:
    """Inputs to the LCOE calculation. All flows in USD; energy in MWh/yr."""

    capex_total: float
    opex_yr: float
    fuel_yr: float
    energy_mwh_yr: float
    lifetime_years: int
    discount_rate: float


def lcoe(i: LcoeInputs) -> float:
    args = [i]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_lcoe__mutmut_orig, x_lcoe__mutmut_mutants, args, kwargs, None)


def x_lcoe__mutmut_orig(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_1(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 and i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_2(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr < 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_3(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 1 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_4(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years < 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_5(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 1:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_6(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError(None)
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_7(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("XXenergy_mwh_yr and lifetime_years must be positiveXX")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_8(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("ENERGY_MWH_YR AND LIFETIME_YEARS MUST BE POSITIVE")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_9(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = None
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_10(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = None
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_11(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = None
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_12(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 1.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_13(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(None, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_14(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, None):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_15(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_16(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, ):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_17(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(2, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_18(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years - 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_19(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 2):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_20(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = None
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_21(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 * (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_22(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 2.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_23(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) * t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_24(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 - r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_25(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (2.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_26(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv = (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_27(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv -= (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_28(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) / df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_29(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr - i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_30(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv = i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_31(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv -= i.energy_mwh_yr * df
    return cost_pv / energy_pv


def x_lcoe__mutmut_32(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr / df
    return cost_pv / energy_pv


def x_lcoe__mutmut_33(i: LcoeInputs) -> float:
    """Return LCOE in USD/MWh."""
    if i.energy_mwh_yr <= 0 or i.lifetime_years <= 0:
        raise ValueError("energy_mwh_yr and lifetime_years must be positive")
    r = i.discount_rate
    cost_pv = i.capex_total
    energy_pv = 0.0
    for t in range(1, i.lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (i.opex_yr + i.fuel_yr) * df
        energy_pv += i.energy_mwh_yr * df
    return cost_pv * energy_pv

x_lcoe__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_lcoe__mutmut_1': x_lcoe__mutmut_1, 
    'x_lcoe__mutmut_2': x_lcoe__mutmut_2, 
    'x_lcoe__mutmut_3': x_lcoe__mutmut_3, 
    'x_lcoe__mutmut_4': x_lcoe__mutmut_4, 
    'x_lcoe__mutmut_5': x_lcoe__mutmut_5, 
    'x_lcoe__mutmut_6': x_lcoe__mutmut_6, 
    'x_lcoe__mutmut_7': x_lcoe__mutmut_7, 
    'x_lcoe__mutmut_8': x_lcoe__mutmut_8, 
    'x_lcoe__mutmut_9': x_lcoe__mutmut_9, 
    'x_lcoe__mutmut_10': x_lcoe__mutmut_10, 
    'x_lcoe__mutmut_11': x_lcoe__mutmut_11, 
    'x_lcoe__mutmut_12': x_lcoe__mutmut_12, 
    'x_lcoe__mutmut_13': x_lcoe__mutmut_13, 
    'x_lcoe__mutmut_14': x_lcoe__mutmut_14, 
    'x_lcoe__mutmut_15': x_lcoe__mutmut_15, 
    'x_lcoe__mutmut_16': x_lcoe__mutmut_16, 
    'x_lcoe__mutmut_17': x_lcoe__mutmut_17, 
    'x_lcoe__mutmut_18': x_lcoe__mutmut_18, 
    'x_lcoe__mutmut_19': x_lcoe__mutmut_19, 
    'x_lcoe__mutmut_20': x_lcoe__mutmut_20, 
    'x_lcoe__mutmut_21': x_lcoe__mutmut_21, 
    'x_lcoe__mutmut_22': x_lcoe__mutmut_22, 
    'x_lcoe__mutmut_23': x_lcoe__mutmut_23, 
    'x_lcoe__mutmut_24': x_lcoe__mutmut_24, 
    'x_lcoe__mutmut_25': x_lcoe__mutmut_25, 
    'x_lcoe__mutmut_26': x_lcoe__mutmut_26, 
    'x_lcoe__mutmut_27': x_lcoe__mutmut_27, 
    'x_lcoe__mutmut_28': x_lcoe__mutmut_28, 
    'x_lcoe__mutmut_29': x_lcoe__mutmut_29, 
    'x_lcoe__mutmut_30': x_lcoe__mutmut_30, 
    'x_lcoe__mutmut_31': x_lcoe__mutmut_31, 
    'x_lcoe__mutmut_32': x_lcoe__mutmut_32, 
    'x_lcoe__mutmut_33': x_lcoe__mutmut_33
}
x_lcoe__mutmut_orig.__name__ = 'x_lcoe'


def capacity_cost_to_capex(capex_per_kw: float, capacity_kw: float) -> float:
    args = [capex_per_kw, capacity_kw]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_capacity_cost_to_capex__mutmut_orig, x_capacity_cost_to_capex__mutmut_mutants, args, kwargs, None)


def x_capacity_cost_to_capex__mutmut_orig(capex_per_kw: float, capacity_kw: float) -> float:
    """Convert per-kW capex and a capacity into total capex USD."""
    return capex_per_kw * capacity_kw


def x_capacity_cost_to_capex__mutmut_1(capex_per_kw: float, capacity_kw: float) -> float:
    """Convert per-kW capex and a capacity into total capex USD."""
    return capex_per_kw / capacity_kw

x_capacity_cost_to_capex__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_capacity_cost_to_capex__mutmut_1': x_capacity_cost_to_capex__mutmut_1
}
x_capacity_cost_to_capex__mutmut_orig.__name__ = 'x_capacity_cost_to_capex'


def annual_energy_mwh(capacity_kw: float, capacity_factor: float) -> float:
    args = [capacity_kw, capacity_factor]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_annual_energy_mwh__mutmut_orig, x_annual_energy_mwh__mutmut_mutants, args, kwargs, None)


def x_annual_energy_mwh__mutmut_orig(capacity_kw: float, capacity_factor: float) -> float:
    """Return MWh/year produced by a unit at a given capacity factor."""
    return capacity_kw * capacity_factor * HOURS_PER_YEAR / 1000.0


def x_annual_energy_mwh__mutmut_1(capacity_kw: float, capacity_factor: float) -> float:
    """Return MWh/year produced by a unit at a given capacity factor."""
    return capacity_kw * capacity_factor * HOURS_PER_YEAR * 1000.0


def x_annual_energy_mwh__mutmut_2(capacity_kw: float, capacity_factor: float) -> float:
    """Return MWh/year produced by a unit at a given capacity factor."""
    return capacity_kw * capacity_factor / HOURS_PER_YEAR / 1000.0


def x_annual_energy_mwh__mutmut_3(capacity_kw: float, capacity_factor: float) -> float:
    """Return MWh/year produced by a unit at a given capacity factor."""
    return capacity_kw / capacity_factor * HOURS_PER_YEAR / 1000.0


def x_annual_energy_mwh__mutmut_4(capacity_kw: float, capacity_factor: float) -> float:
    """Return MWh/year produced by a unit at a given capacity factor."""
    return capacity_kw * capacity_factor * HOURS_PER_YEAR / 1001.0

x_annual_energy_mwh__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_annual_energy_mwh__mutmut_1': x_annual_energy_mwh__mutmut_1, 
    'x_annual_energy_mwh__mutmut_2': x_annual_energy_mwh__mutmut_2, 
    'x_annual_energy_mwh__mutmut_3': x_annual_energy_mwh__mutmut_3, 
    'x_annual_energy_mwh__mutmut_4': x_annual_energy_mwh__mutmut_4
}
x_annual_energy_mwh__mutmut_orig.__name__ = 'x_annual_energy_mwh'


def lcoh_pem(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    args = []# type: ignore
    kwargs = {'electrolyzer_capex_per_kw': electrolyzer_capex_per_kw, 'electrolyzer_kw': electrolyzer_kw, 'electrolyzer_opex_per_kw_yr': electrolyzer_opex_per_kw_yr, 'electricity_price_per_mwh': electricity_price_per_mwh, 'efficiency_lhv': efficiency_lhv, 'capacity_factor': capacity_factor, 'lifetime_years': lifetime_years, 'discount_rate': discount_rate, 'ira_45v_credit_per_kg': ira_45v_credit_per_kg}# type: ignore
    return _mutmut_trampoline(x_lcoh_pem__mutmut_orig, x_lcoh_pem__mutmut_mutants, args, kwargs, None)


def x_lcoh_pem__mutmut_orig(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_1(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 1.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_2(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = None
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_3(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor / HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_4(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw / capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_5(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = None
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_6(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv * H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_7(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in / efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_8(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = None
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_9(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 / electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_10(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in * 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_11(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1001.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_12(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = None
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_13(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw / electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_14(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = None

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_15(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr / electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_16(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = None
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_17(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = None
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_18(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = None
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_19(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 1.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_20(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(None, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_21(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, None):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_22(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_23(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, ):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_24(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(2, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_25(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years - 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_26(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 2):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_27(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = None
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_28(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 * (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_29(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 2.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_30(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) * t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_31(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 - r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_32(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (2.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_33(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv = (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_34(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv -= (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_35(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) / df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_36(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex - annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_37(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv = annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_38(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv -= annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_39(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 / df
    gross = cost_pv / h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_40(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = None
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_41(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv * h2_pv
    return gross - ira_45v_credit_per_kg


def x_lcoh_pem__mutmut_42(
    *,
    electrolyzer_capex_per_kw: float,
    electrolyzer_kw: float,
    electrolyzer_opex_per_kw_yr: float,
    electricity_price_per_mwh: float,
    efficiency_lhv: float,
    capacity_factor: float,
    lifetime_years: int,
    discount_rate: float,
    ira_45v_credit_per_kg: float = 0.0,
) -> float:
    """Levelised cost of hydrogen, USD/kg.

    Energy in: electricity. Energy out: hydrogen at 33.33 kWh/kg LHV.
    """
    annual_kwh_in = electrolyzer_kw * capacity_factor * HOURS_PER_YEAR
    annual_kg_h2 = annual_kwh_in * efficiency_lhv / H2_LHV_KWH_PER_KG
    annual_electricity_cost = annual_kwh_in / 1000.0 * electricity_price_per_mwh
    capex = electrolyzer_capex_per_kw * electrolyzer_kw
    opex = electrolyzer_opex_per_kw_yr * electrolyzer_kw

    r = discount_rate
    cost_pv = capex
    h2_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_electricity_cost) * df
        h2_pv += annual_kg_h2 * df
    gross = cost_pv / h2_pv
    return gross + ira_45v_credit_per_kg

x_lcoh_pem__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_lcoh_pem__mutmut_1': x_lcoh_pem__mutmut_1, 
    'x_lcoh_pem__mutmut_2': x_lcoh_pem__mutmut_2, 
    'x_lcoh_pem__mutmut_3': x_lcoh_pem__mutmut_3, 
    'x_lcoh_pem__mutmut_4': x_lcoh_pem__mutmut_4, 
    'x_lcoh_pem__mutmut_5': x_lcoh_pem__mutmut_5, 
    'x_lcoh_pem__mutmut_6': x_lcoh_pem__mutmut_6, 
    'x_lcoh_pem__mutmut_7': x_lcoh_pem__mutmut_7, 
    'x_lcoh_pem__mutmut_8': x_lcoh_pem__mutmut_8, 
    'x_lcoh_pem__mutmut_9': x_lcoh_pem__mutmut_9, 
    'x_lcoh_pem__mutmut_10': x_lcoh_pem__mutmut_10, 
    'x_lcoh_pem__mutmut_11': x_lcoh_pem__mutmut_11, 
    'x_lcoh_pem__mutmut_12': x_lcoh_pem__mutmut_12, 
    'x_lcoh_pem__mutmut_13': x_lcoh_pem__mutmut_13, 
    'x_lcoh_pem__mutmut_14': x_lcoh_pem__mutmut_14, 
    'x_lcoh_pem__mutmut_15': x_lcoh_pem__mutmut_15, 
    'x_lcoh_pem__mutmut_16': x_lcoh_pem__mutmut_16, 
    'x_lcoh_pem__mutmut_17': x_lcoh_pem__mutmut_17, 
    'x_lcoh_pem__mutmut_18': x_lcoh_pem__mutmut_18, 
    'x_lcoh_pem__mutmut_19': x_lcoh_pem__mutmut_19, 
    'x_lcoh_pem__mutmut_20': x_lcoh_pem__mutmut_20, 
    'x_lcoh_pem__mutmut_21': x_lcoh_pem__mutmut_21, 
    'x_lcoh_pem__mutmut_22': x_lcoh_pem__mutmut_22, 
    'x_lcoh_pem__mutmut_23': x_lcoh_pem__mutmut_23, 
    'x_lcoh_pem__mutmut_24': x_lcoh_pem__mutmut_24, 
    'x_lcoh_pem__mutmut_25': x_lcoh_pem__mutmut_25, 
    'x_lcoh_pem__mutmut_26': x_lcoh_pem__mutmut_26, 
    'x_lcoh_pem__mutmut_27': x_lcoh_pem__mutmut_27, 
    'x_lcoh_pem__mutmut_28': x_lcoh_pem__mutmut_28, 
    'x_lcoh_pem__mutmut_29': x_lcoh_pem__mutmut_29, 
    'x_lcoh_pem__mutmut_30': x_lcoh_pem__mutmut_30, 
    'x_lcoh_pem__mutmut_31': x_lcoh_pem__mutmut_31, 
    'x_lcoh_pem__mutmut_32': x_lcoh_pem__mutmut_32, 
    'x_lcoh_pem__mutmut_33': x_lcoh_pem__mutmut_33, 
    'x_lcoh_pem__mutmut_34': x_lcoh_pem__mutmut_34, 
    'x_lcoh_pem__mutmut_35': x_lcoh_pem__mutmut_35, 
    'x_lcoh_pem__mutmut_36': x_lcoh_pem__mutmut_36, 
    'x_lcoh_pem__mutmut_37': x_lcoh_pem__mutmut_37, 
    'x_lcoh_pem__mutmut_38': x_lcoh_pem__mutmut_38, 
    'x_lcoh_pem__mutmut_39': x_lcoh_pem__mutmut_39, 
    'x_lcoh_pem__mutmut_40': x_lcoh_pem__mutmut_40, 
    'x_lcoh_pem__mutmut_41': x_lcoh_pem__mutmut_41, 
    'x_lcoh_pem__mutmut_42': x_lcoh_pem__mutmut_42
}
x_lcoh_pem__mutmut_orig.__name__ = 'x_lcoh_pem'


def lcos(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    args = []# type: ignore
    kwargs = {'capex_per_kwh': capex_per_kwh, 'capacity_kwh': capacity_kwh, 'capex_per_kw': capex_per_kw, 'capacity_kw': capacity_kw, 'opex_per_kw_yr': opex_per_kw_yr, 'cycles_per_year': cycles_per_year, 'roundtrip_efficiency': roundtrip_efficiency, 'charge_electricity_price_per_mwh': charge_electricity_price_per_mwh, 'lifetime_years': lifetime_years, 'discount_rate': discount_rate}# type: ignore
    return _mutmut_trampoline(x_lcos__mutmut_orig, x_lcos__mutmut_mutants, args, kwargs, None)


def x_lcos__mutmut_orig(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_1(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = None
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_2(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh - capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_3(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh / capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_4(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw / capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_5(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = None
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_6(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr / capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_7(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = None
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_8(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh * 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_9(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year / capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_10(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1001.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_11(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = None
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_12(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in / roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_13(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = None

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_14(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in / charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_15(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = None
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_16(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = None
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_17(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = None
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_18(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 1.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_19(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(None, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_20(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, None):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_21(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_22(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, ):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_23(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(2, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_24(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years - 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_25(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 2):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_26(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = None
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_27(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 * (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_28(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 2.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_29(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) * t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_30(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 - r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_31(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (2.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_32(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv = (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_33(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv -= (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_34(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) / df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_35(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex - annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_36(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv = annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_37(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv -= annual_mwh_out * df
    return cost_pv / out_pv


def x_lcos__mutmut_38(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out / df
    return cost_pv / out_pv


def x_lcos__mutmut_39(
    *,
    capex_per_kwh: float,
    capacity_kwh: float,
    capex_per_kw: float,
    capacity_kw: float,
    opex_per_kw_yr: float,
    cycles_per_year: int,
    roundtrip_efficiency: float,
    charge_electricity_price_per_mwh: float,
    lifetime_years: int,
    discount_rate: float,
) -> float:
    """Levelised cost of storage, USD/MWh out."""
    capex = capex_per_kwh * capacity_kwh + capex_per_kw * capacity_kw
    opex = opex_per_kw_yr * capacity_kw
    annual_mwh_in = cycles_per_year * capacity_kwh / 1000.0
    annual_mwh_out = annual_mwh_in * roundtrip_efficiency
    annual_charge_cost = annual_mwh_in * charge_electricity_price_per_mwh

    r = discount_rate
    cost_pv = capex
    out_pv = 0.0
    for t in range(1, lifetime_years + 1):
        df = 1.0 / (1.0 + r) ** t
        cost_pv += (opex + annual_charge_cost) * df
        out_pv += annual_mwh_out * df
    return cost_pv * out_pv

x_lcos__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_lcos__mutmut_1': x_lcos__mutmut_1, 
    'x_lcos__mutmut_2': x_lcos__mutmut_2, 
    'x_lcos__mutmut_3': x_lcos__mutmut_3, 
    'x_lcos__mutmut_4': x_lcos__mutmut_4, 
    'x_lcos__mutmut_5': x_lcos__mutmut_5, 
    'x_lcos__mutmut_6': x_lcos__mutmut_6, 
    'x_lcos__mutmut_7': x_lcos__mutmut_7, 
    'x_lcos__mutmut_8': x_lcos__mutmut_8, 
    'x_lcos__mutmut_9': x_lcos__mutmut_9, 
    'x_lcos__mutmut_10': x_lcos__mutmut_10, 
    'x_lcos__mutmut_11': x_lcos__mutmut_11, 
    'x_lcos__mutmut_12': x_lcos__mutmut_12, 
    'x_lcos__mutmut_13': x_lcos__mutmut_13, 
    'x_lcos__mutmut_14': x_lcos__mutmut_14, 
    'x_lcos__mutmut_15': x_lcos__mutmut_15, 
    'x_lcos__mutmut_16': x_lcos__mutmut_16, 
    'x_lcos__mutmut_17': x_lcos__mutmut_17, 
    'x_lcos__mutmut_18': x_lcos__mutmut_18, 
    'x_lcos__mutmut_19': x_lcos__mutmut_19, 
    'x_lcos__mutmut_20': x_lcos__mutmut_20, 
    'x_lcos__mutmut_21': x_lcos__mutmut_21, 
    'x_lcos__mutmut_22': x_lcos__mutmut_22, 
    'x_lcos__mutmut_23': x_lcos__mutmut_23, 
    'x_lcos__mutmut_24': x_lcos__mutmut_24, 
    'x_lcos__mutmut_25': x_lcos__mutmut_25, 
    'x_lcos__mutmut_26': x_lcos__mutmut_26, 
    'x_lcos__mutmut_27': x_lcos__mutmut_27, 
    'x_lcos__mutmut_28': x_lcos__mutmut_28, 
    'x_lcos__mutmut_29': x_lcos__mutmut_29, 
    'x_lcos__mutmut_30': x_lcos__mutmut_30, 
    'x_lcos__mutmut_31': x_lcos__mutmut_31, 
    'x_lcos__mutmut_32': x_lcos__mutmut_32, 
    'x_lcos__mutmut_33': x_lcos__mutmut_33, 
    'x_lcos__mutmut_34': x_lcos__mutmut_34, 
    'x_lcos__mutmut_35': x_lcos__mutmut_35, 
    'x_lcos__mutmut_36': x_lcos__mutmut_36, 
    'x_lcos__mutmut_37': x_lcos__mutmut_37, 
    'x_lcos__mutmut_38': x_lcos__mutmut_38, 
    'x_lcos__mutmut_39': x_lcos__mutmut_39
}
x_lcos__mutmut_orig.__name__ = 'x_lcos'
