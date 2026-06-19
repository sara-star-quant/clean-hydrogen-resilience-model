# Generated tables <!-- model v0.5.0 @ d26c030 | params 4dc4a3881481 -->

Do not edit by hand. Run `python -m electicity_model.cli render-all` to regenerate.

## District scenarios

<!-- model v0.5.0 @ d26c030 | params 4dc4a3881481 -->
<!-- caption: scenario output, not a forecast -->

| Scenario | CapEx | Fits $36M? | LCOE | LCOH |
|---|---|---|---|---|
| district_solar_h2_inland | $26.9M | yes | $214/MWh | $1.90/kg |
| district_microhydro_river | $20.3M | yes | $159/MWh | $4.30/kg |
| district_tidal_coastal | $24.2M | yes | $198/MWh | $5.22/kg |

## Heavy-duty truck scenarios

<!-- model v0.5.0 @ d26c030 | params 4dc4a3881481 -->
<!-- caption: scenario output, not a forecast -->

| Scenario | Powertrain | H2 price | TCO | Fuel cost |
|---|---|---|---|---|
| car_fcev_class8 | fcev | $4/kg | $0.907/km | $0.349/km |
| car_fcev_class8 | fcev | $6/kg | $1.082/km | $0.524/km |
| car_fcev_class8 | fcev | $9/kg | $1.343/km | $0.786/km |
| car_bev_class8_ref | bev | n/a | $0.712/km | $0.207/km |
| car_diesel_class8_ref | ice_diesel | n/a | $0.781/km | $0.422/km |
