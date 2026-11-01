import { C, Card, Chip, N, Slide, Src, Stat } from './ui'

function FundBar() {
  const rows = [
    ['Response + relief', 40, '₹414.2 cr/yr', C.red],
    ['Recovery + reconstruction', 30, '₹310.7 cr/yr', C.ember],
    ['Preparedness + capacity', 10, '₹103.6 cr/yr', C.blue],
    ['Mitigation', 20, '₹207.1 cr/yr', C.teal],
  ] as const
  return (
    <div className="flex flex-col gap-[8px]">
      {rows.map(([label, pct, value, col]) => (
        <div key={label} className="grid grid-cols-[190px_1fr_120px] items-center gap-[10px]">
          <span style={{ fontSize: 15 }}>{label}</span>
          <div className="h-[16px] rounded-full" style={{ background: '#F6DCC4' }}>
            <div className="h-full rounded-full" style={{ width: `${pct * 2.2}%`, background: col }} />
          </div>
          <span className="font-mono text-right" style={{ fontSize: 14 }}>{value}</span>
        </div>
      ))}
    </div>
  )
}

function Formula() {
  return (
    <div className="rounded-[12px] p-[12px]" style={{ background: C.well }}>
      <div className="font-mono" style={{ fontSize: 16, lineHeight: 1.5 }}>
        ₹724.9 cr × addressable share × warning effect × operational realisation
      </div>
      <div className="mt-[8px] grid grid-cols-[1fr_auto] gap-x-[12px] gap-y-[6px]" style={{ fontSize: 16 }}>
        <span>Low: 10% × 10% × 50%</span><b style={{ color: C.teal }}>{N('uk_avoidable_low').v}</b>
        <span>Base: 20% × 20% × 65%</span><b style={{ color: C.teal }}>{N('uk_avoidable_base').v}</b>
      </div>
    </div>
  )
}

export function Slide1() {
  return (
    <Slide
      n={1}
      title="A ₹1.5–3 crore warning network against Uttarakhand's ₹724.9 crore annual relief-and-recovery envelope."
      sub="Official fiscal baselines + live Indian component quotes + transparent scenarios. Potential avoided burden, not guaranteed cash savings."
    >
      <div className="grid h-full grid-cols-12 grid-rows-[1fr_auto] gap-[18px]">
        <Card title="Official Uttarakhand fiscal baseline" className="col-span-4" accent={C.blue} right={<Chip k="SOURCE">OFFICIAL</Chip>}>
          <div className="flex h-full flex-col justify-between gap-[12px]">
            <Stat v={N('uk_dm_5yr').v} label="disaster-management allocation, 2021–26" size={52} color={C.blue} />
            <FundBar />
            <div className="rounded-[12px] p-[10px]" style={{ background: C.well }}>
              <b style={{ fontSize: 22 }}>{N('uk_rr_annual').v}</b>
              <div style={{ fontSize: 16, color: C.dim }}>response/relief + recovery/reconstruction comparison envelope</div>
            </div>
            <Src>FC-XV Volume I · para 8.54 · Table 10.13</Src>
          </div>
        </Card>

        <Card title="Priority-corridor network" className="col-span-4" accent={C.ember} right={<Chip k="VERIFY">PLANNING RANGE</Chip>}>
          <div className="flex h-full flex-col justify-between gap-[10px]">
            <Stat v={N('uk_network_cost').v} label="first-year planning range" size={52} color={C.ember} />
            <div className="grid grid-cols-3 gap-[9px] text-center">
              {[
                ['500', 'slope nodes'],
                ['50', 'shared rain stations'],
                ['95', 'edge gateways'],
              ].map(([v, l]) => (
                <div key={l} className="rounded-[10px] p-[10px]" style={{ background: C.well }}>
                  <div className="font-bold" style={{ fontSize: 30 }}>{v}</div>
                  <div style={{ fontSize: 14, color: C.dim }}>{l}</div>
                </div>
              ))}
            </div>
            <ul className="flex flex-col gap-[5px]" style={{ fontSize: 16 }}>
              <li>● slope node ≈ ₹8,000 installed</li>
              <li>● industrial rain station ≈ ₹40,000</li>
              <li>● gateway ≈ ₹35,000</li>
              <li>● redundant servers, audit, security, training, spares included as allowances</li>
            </ul>
            <div className="rounded-[10px] px-[12px] py-[8px] font-semibold" style={{ background: '#EFE7FF', color: C.violet }}>
              Only 0.15–0.29% of annual disaster-management allocation
            </div>
            <Src>ElectronicsComp quotes, 31 Oct 2026 · docs/27</Src>
          </div>
        </Card>

        <Card title="Potential gross avoided burden" className="col-span-4" accent={C.teal} right={<Chip k="VERIFY">SCENARIO · NOT GUARANTEED</Chip>}>
          <div className="flex h-full flex-col justify-between gap-[10px]">
            <div className="grid grid-cols-2 gap-[12px]">
              <Stat v={N('uk_avoidable_low').v} label="low scenario" size={38} color={C.teal} />
              <Stat v={N('uk_avoidable_base').v} label="base scenario" size={38} color={C.teal} />
            </div>
            <Formula />
            <div className="rounded-[12px] p-[12px]" style={{ background: '#FDE3D3' }}>
              <b style={{ color: C.red }}>Do not say “TRINETRA will save ₹18.8 cr”.</b>
              <div style={{ fontSize: 15, color: C.dim, marginTop: 4 }}>A shadow pilot must measure lead time, uptime, operator action, false alarms and covered-vs-comparison losses.</div>
            </div>
            <Src>results/uttarakhand_cost_benefit.json · formula in docs/27</Src>
          </div>
        </Card>

        <Card title="Reality check: one severe Uttarakhand event" className="col-span-7" accent={C.red} right={<Chip k="SOURCE">OFFICIAL JRDNA</Chip>}>
          <div className="grid grid-cols-[1fr_1fr_1.4fr] items-center gap-[18px]">
            <Stat v={N('uk_2013_cost').v} label="2013 damage and recovery needs" src="GoU–World Bank–ADB JRDNA, Table 1" size={39} color={C.red} />
            <Stat v={N('uk_2013_roads').v} label="roads and bridges alone" src="same assessment" size={39} color={C.red} />
            <p style={{ fontSize: 17, color: C.dim }}>
              The event cross-check gives ₹19.8 cr (low) to ₹103.1 cr (base) in potential avoided burden—but this is a sensitivity test, not a retrospective claim.
            </p>
          </div>
        </Card>

        <Card title="Why invest before the disaster" className="col-span-5" accent={C.gold} right={<Chip k="SOURCE">SURVEYS + REPORTS</Chip>}>
          <div className="grid grid-cols-2 gap-[18px]">
            <Stat v="8×" label="higher mortality where early-warning coverage is limited" src="WMO + UNDRR MHEWS 2023 country survey" size={40} color={C.teal} />
            <Stat v="−30%" label="damage with just 24 h storm / heatwave warning" src="Global Commission on Adaptation, 2019" size={40} color={C.teal} />
          </div>
        </Card>
      </div>
    </Slide>
  )
}
