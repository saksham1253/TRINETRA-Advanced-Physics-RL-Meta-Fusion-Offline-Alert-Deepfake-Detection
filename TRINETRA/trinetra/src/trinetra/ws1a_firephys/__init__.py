"""ws1a_firephys — fire & thermal physics (Class A established + Class C novel, flag-gated). M1."""
from .established_ef import (
    flame_height_heskestad, strouhal_puffing_frequency, plume_centerline_dT,
    byram_convection_number, graybody_radiance, graybody_temperature, beer_lambert_transmittance,
)
from .novel_nd import (
    aliased_frequency, nd1_dealiased_flicker, nd2_transmittance_temperature, nd3_ignition_index,
    ND1Result, ND2Result,
)
from .gate import fire_gate, FireInputs, FireResult

__all__ = [
    "flame_height_heskestad", "strouhal_puffing_frequency", "plume_centerline_dT",
    "byram_convection_number", "graybody_radiance", "graybody_temperature", "beer_lambert_transmittance",
    "aliased_frequency", "nd1_dealiased_flicker", "nd2_transmittance_temperature", "nd3_ignition_index",
    "ND1Result", "ND2Result",
    "fire_gate", "FireInputs", "FireResult",
]
