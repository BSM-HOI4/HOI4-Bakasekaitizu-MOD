# BSM National Currency System

Last updated: 2026-06-08

## Overview

Each country/region has its own local currency with a dynamically fluctuating exchange rate against the Unified Currency (UC). The exchange rate affects UC gain and can be unified through the Economic Alliance Currency Union (Goal03).

## Currency List (30 currencies)

| ID | Key | Currency | Symbol | Anchor | Initial Rate (1 UC =) |
|----|-----|----------|--------|--------|----------------------|
| 0 | `nc_uc` | Unified Currency | UC | — | 1.0 |
| 1 | `nc_usd` | US Dollar | $ | USA | 1.0 |
| 2 | `nc_eur` | Euro | € | EUR/FRA/DEU | 0.92 |
| 3 | `nc_gbp` | Pound Sterling | £ | GBR | 0.79 |
| 4 | `nc_jpy` | Yen | ¥ | JPN | 149.0 |
| 5 | `nc_cny` | Yuan | ¥ | CHI | 7.2 |
| 6 | `nc_rub` | Ruble | ₽ | SOV | 92.0 |
| 7 | `nc_krw` | Won | ₩ | KOR | 1320.0 |
| 8 | `nc_inr` | Rupee | ₹ | IND | 83.0 |
| 9 | `nc_try` | Lira | ₺ | TUR | 27.0 |
| 10 | `nc_brl` | Real | R$ | BRA | 5.0 |
| 11 | `nc_mxn` | Mexican Peso | Mex$ | MEX | 17.0 |
| 12 | `nc_ars` | Argentine Peso | AR$ | ARG | 350.0 |
| 13 | `nc_sar` | Saudi Riyal | ﷼ | SAU | 3.75 |
| 14 | `nc_egp` | Egyptian Pound | E£ | EGY | 31.0 |
| 15 | `nc_chf` | Swiss Franc | Fr | SWI | 0.88 |
| 16 | `nc_sek` | Krona | kr | SWE | 10.5 |
| 17 | `nc_aud` | Australian Dollar | A$ | AST | 1.55 |
| 18 | `nc_idr` | Rupiah | Rp | IDN | 15500.0 |
| 19 | `nc_thb` | Baht | ฿ | SIA | 35.0 |
| 20 | `nc_ngn` | Naira | ₦ | NGA | 800.0 |
| 21 | `nc_zar` | Rand | R | ZAF | 19.0 |
| 22 | `nc_kes` | East African Shilling | KSh | KEN | 150.0 |
| 23 | `nc_cop` | Colombian Peso | Col$ | COL | 4000.0 |
| 24 | `nc_ils` | Shekel | ₪ | ISR | 3.7 |
| 25 | `nc_twd` | Taiwan Dollar | NT$ | TWN | 31.0 |
| 26 | `nc_php` | Philippine Peso | ₱ | PHI | 56.0 |
| 27 | `nc_myr` | Ringgit | RM | MAL | 4.7 |
| 28 | `nc_man` | Manchukuo Yuan | 滿 | MAN | 120.0 |
| 29 | `nc_generic` | Generic Currency | ¤ | — | 100.0 |

## Country Variables

| Variable | Type | Description |
|----------|------|-------------|
| `bsm_nc_id` | int | Currency ID (0-29) |
| `bsm_nc_rate` | float | Current exchange rate (1 UC = X NC) |
| `bsm_nc_base_rate` | float | Base exchange rate (initial value) |
| `bsm_nc_rate_prev` | float | Previous month's rate |
| `bsm_nc_rate_delta` | float | Month-over-month change |
| `bsm_nc_stability` | int | Currency stability (0-100) |
| `bsm_nc_inflation` | float | Inflation rate (%) |
| `bsm_nc_original_id` | int | Original currency ID (for Goal03 reversion) |
| `bsm_nc_filter_mode` | int | GUI filter (0=alliance, 1=world) |

## Monthly Exchange Rate Calculation

```
new_rate = base_rate / factor

factor composition:
  Base: 1.0
  + Stability: (stability - 0.5) × 0.1
  × War penalty: ×0.95 (prolonged: additional ×0.92, ×0.95)
  × UC surplus: ×1.02
  × UC debt: ×0.93
  × EA Goal03: ×1.05
  × High civilization: ×1.01 (>0.5), ×1.01 (>0.8)
  × Subject: ×0.96

Clamp: base_rate × 0.3 ~ base_rate × 3.0
```

## UC Gain Impact

The exchange modifier is added to `temp_factor` in the existing UC monthly calculation (`_bsm_Unified_Currency.txt`):

```
t_nc_uc_mod = (base_rate / current_rate - 1.0) × 0.3
temp_factor += t_nc_uc_mod
temp_factor = clamp(temp_factor, min=0.05)
```

- Strong currency (rate < base) → UC gain bonus
- Weak currency (rate > base) → UC gain penalty

## Strength Tier

| Tier | Condition | Display |
|------|-----------|---------|
| Strong | rate < base × 0.9 | §G▲ Strong§! |
| Normal | base×0.9 ≤ rate ≤ base×1.1 | §Y― Normal§! |
| Weak | rate > base × 1.1 | §R▼ Weak§! |

## EA Goal03 (Currency Union) Integration

On Goal03 activation:
- All members' `bsm_nc_id` unified to leader's currency
- `bsm_nc_rate` / `bsm_nc_base_rate` synced to leader
- Monthly calculation: ×1.05 bonus

On Goal03 deactivation:
- Revert to `bsm_nc_original_id`
- `bsm_nc_assign_currency` re-applies base_rate

## Crisis Events

| Event ID | Trigger | Effect | Cooldown |
|----------|---------|--------|----------|
| `nc.1` | Inflation > 20% | Rate +50, Stability -30 | 180 days |
| `nc.2` | UC < 0 | Rate ×1.5, Stability -40 | 360 days |
| `nc.3` | Stability > 90% | Rate ×0.95, Stability +10 | 365 days |
| `nc.4` | Goal03 achieved | News event | — |

## Dynamic Modifier

- `bsm_nc_crisis_modifier`: When stability < 30%
  - Stability -5%, War Support -3%, PP -10%

## File Structure

### New Files
| Path | Role |
|------|------|
| `common/scripted_effects/_bsm_national_currency.txt` | Init, monthly calc, data prep, event triggers |
| `common/scripted_triggers/_bsm_national_currency_triggers.txt` | Currency check triggers |
| `common/scripted_localisation/_bsm_national_currency_sloc.txt` | Dynamic localisation |
| `common/dynamic_modifiers/_bsm_national_currency_modifiers.txt` | Crisis modifier |
| `events/_bsm_national_currency_events.txt` | Currency events |
| `interface/_bsm_national_currency.gfx` | Sprite definitions (30×3 = 90) |
| `localisation/japanese/_bsm_national_currency_l_japanese.yml` | Localisation |
| `gfx/currency/` | Currency icon images (75×40px PNG) |

### Modified Files
| Path | Changes |
|------|---------|
| `common/on_actions/_bsm_system.txt` | Startup: `bsm_nc_init_currency`, Monthly: `bsm_nc_monthly_update` |
| `common/scripted_effects/_bsm_Unified_Currency.txt` | Exchange rate modifier integrated into UC calc |
| `common/modifier_definitions/_bsm_core.txt` | Added `NC_exchange_factor` |
| `common/scripted_effects/bsm_ea_goals_effects.txt` | Goal03 currency union/reversion |
| `interface/bsm_economic_alliance.gui` | 5-tab layout + Tab5 currency rate panel |
| `common/scripted_guis/bsm_economic_alliance_sgui.txt` | Tab5 visibility, filter, dynamic list |
| `interface/BSM_topbar.gui` | Added 75×40 currency icon display area |

## GUI: EA Tab 5 Currency Rates

A 5th tab "Currency Rates" is added to the EA window.

### Layout
- Tab buttons: `GFX_sort_button_140x29` ×5 (all tabs changed to 140px width)
- List: `nc_rate_list` (`global.bsm_nc_rate_display_list` array)
- Entry: `nc_rate_entry` (780×40, row height = icon height)

### Entry Columns
| Column | Position | Content |
|--------|----------|---------|
| Flag | x=4 | `[THIS.GetFlag]` |
| Symbol | x=38 | `[THIS.GetNCSymbol]` |
| Tier | x=38 y=24 | `[THIS.GetNCTier]` |
| Name | x=120 | `[THIS.GetName]` |
| Rate | x=440 | `[?bsm_nc_rate\|2]` |
| Delta | x=555 | `[?bsm_nc_rate_delta\|2+]` |
| Stability | x=670 | `[?bsm_nc_stability\|0]%` |

### Filter
- Alliance only (`bsm_nc_filter_mode = 0`): Current EA members + player
- World (`bsm_nc_filter_mode = 1`): All countries with non-UC currency

## Scripted Localisation

| Name | Purpose |
|------|---------|
| `GetNCName` | Full currency name (e.g. "US Dollar ($)") |
| `GetNCSymbol` | Symbol only (e.g. "$") |
| `GetNCTier` | Tier text (Strong/Normal/Weak) |
| `GetNCIcon` | Text icon (symbol + tier color) |
| `GetNCExchangeRate` | Exchange rate display |
| `GetNCInflation` | Inflation status |
| `GetNCStability` | Currency stability |

## Image Assets

### Location
`bakasekai/gfx/currency/`

### Naming Convention
```
{CURRENCY}.png          # Normal
{CURRENCY}_strong.png   # Strong
{CURRENCY}_weak.png     # Weak
```

### Specs
- Size: 75×40 px
- Format: PNG
- Currency code in uppercase (e.g. `USD.png`, `EUR.png`, `JPY.png`)

### Completed
- USD (normal/strong/weak)
- EUR (normal/strong/weak)

### Pending
UC, GBP, JPY, CNY, RUB, KRW, INR, TRY, BRL, MXN, ARS, SAR, EGP, CHF, SEK, AUD, IDR, THB, NGN, ZAR, KES, COP, ILS, TWD, PHP, MYR, MAN, GENERIC (3 each = 84 images)

## Adding a New Currency

1. Add tag block to `bsm_nc_assign_currency` in `_bsm_national_currency.txt`
2. Add entry to `GetNCName`/`GetNCSymbol` in `_bsm_national_currency_sloc.txt`
3. Add localisation to `_bsm_national_currency_l_japanese.yml`
4. Add sprite definitions to `_bsm_national_currency.gfx`
5. Place 3 images in `gfx/currency/`
