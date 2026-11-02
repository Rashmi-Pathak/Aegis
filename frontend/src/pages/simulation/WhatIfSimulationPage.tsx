import React, { useState, useEffect } from 'react';
import { Sliders, RefreshCw, Play, ShieldAlert, TrendingUp, Sparkles, ArrowRight } from 'lucide-react';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';
import ScenarioComparisonChart from '@/charts/ScenarioComparisonChart';
import { simulationApi } from '@/api/simulationApi';
import { SimulationParams, SimulationResult } from '@/types';

export const WhatIfSimulationPage: React.FC<{ onNavigate: (path: string) => void }> = ({
  onNavigate,
}) => {
  const [params, setParams] = useState<SimulationParams>({
    marketingSpendDelta: -8,
    priceDelta: 5,
    discountDelta: -4,
    hiringDelta: -15,
    procurementDelta: 6,
    inventoryBufferDelta: 12,
  });

  const [result, setResult] = useState<SimulationResult | null>(null);
  const [isSimulating, setIsSimulating] = useState(false);

  const runSim = async (currentParams: SimulationParams) => {
    setIsSimulating(true);
    try {
      const res = await simulationApi.runSimulation(currentParams);
      setResult(res);
    } finally {
      setIsSimulating(false);
    }
  };

  useEffect(() => {
    runSim(params);
  }, []);

  const handleSliderChange = (key: keyof SimulationParams, value: number) => {
    const updated = { ...params, [key]: value };
    setParams(updated);
    runSim(updated);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#FF6A00]/14 pb-5">
        <div>
          <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold tracking-wider">
            STRESS-TESTING & DIGITAL TWIN
          </span>
          <h1 className="text-2xl font-bold text-[#F5F0EA]">What-If Simulation Studio</h1>
          <p className="text-xs font-mono text-[#A89D92] mt-0.5">
            Real-time causal scenario modeling across revenue, operating margins, working capital, and risk exposure.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <GlowButton
            variant="secondary"
            size="sm"
            onClick={() => {
              const resetParams = {
                marketingSpendDelta: 0,
                priceDelta: 0,
                discountDelta: 0,
                hiringDelta: 0,
                procurementDelta: 0,
                inventoryBufferDelta: 0,
              };
              setParams(resetParams);
              runSim(resetParams);
            }}
          >
            Reset to Baseline
          </GlowButton>
          <GlowButton
            size="sm"
            onClick={() => onNavigate('/decision-center')}
          >
            Commit as Recommended Decision
          </GlowButton>
        </div>
      </div>

      {/* Tri-Pane Full Studio Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left: Interactive Scenario Levers */}
        <GlowCard className="lg:col-span-4 space-y-5">
          <div className="flex items-center justify-between border-b border-[#FF6A00]/12 pb-3">
            <h3 className="text-sm font-bold text-[#F5F0EA] flex items-center gap-2">
              <Sliders className="w-4 h-4 text-[#FF6A00]" />
              <span>Control Parameters</span>
            </h3>
            <span className="text-[10px] font-mono text-[#6F665F]">6 ACTIVE LEVERS</span>
          </div>

          <div className="space-y-4 text-xs font-mono">
            {/* Price Lever */}
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-[#A89D92]">Price Delta</span>
                <span className="text-[#FFB15A] font-bold">
                  {params.priceDelta > 0 ? '+' : ''}{params.priceDelta}%
                </span>
              </div>
              <input
                type="range"
                min="-15"
                max="25"
                value={params.priceDelta}
                onChange={(e) => handleSliderChange('priceDelta', Number(e.target.value))}
                className="w-full accent-[#FF6A00] cursor-pointer"
              />
            </div>

            {/* Marketing Budget Lever */}
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-[#A89D92]">Discretionary Marketing Spend</span>
                <span className="text-[#FF8A24] font-bold">
                  {params.marketingSpendDelta > 0 ? '+' : ''}{params.marketingSpendDelta}%
                </span>
              </div>
              <input
                type="range"
                min="-30"
                max="30"
                value={params.marketingSpendDelta}
                onChange={(e) => handleSliderChange('marketingSpendDelta', Number(e.target.value))}
                className="w-full accent-[#FF6A00] cursor-pointer"
              />
            </div>

            {/* Discount Lever */}
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-[#A89D92]">Promotional Discounting Delta</span>
                <span className="text-[#FFB15A] font-bold">
                  {params.discountDelta > 0 ? '+' : ''}{params.discountDelta}%
                </span>
              </div>
              <input
                type="range"
                min="-20"
                max="20"
                value={params.discountDelta}
                onChange={(e) => handleSliderChange('discountDelta', Number(e.target.value))}
                className="w-full accent-[#FF6A00] cursor-pointer"
              />
            </div>

            {/* Procurement / Fuel Hedging Lever */}
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-[#A89D92]">Procurement / Hedging Coverage</span>
                <span className="text-[#FF8A24] font-bold">
                  {params.procurementDelta > 0 ? '+' : ''}{params.procurementDelta}%
                </span>
              </div>
              <input
                type="range"
                min="-10"
                max="30"
                value={params.procurementDelta}
                onChange={(e) => handleSliderChange('procurementDelta', Number(e.target.value))}
                className="w-full accent-[#FF6A00] cursor-pointer"
              />
            </div>

            {/* Inventory Safety Buffer */}
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-[#A89D92]">Inventory Safety Buffer Buffer</span>
                <span className="text-[#FFB15A] font-bold">
                  {params.inventoryBufferDelta > 0 ? '+' : ''}{params.inventoryBufferDelta}%
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="50"
                value={params.inventoryBufferDelta}
                onChange={(e) => handleSliderChange('inventoryBufferDelta', Number(e.target.value))}
                className="w-full accent-[#FF6A00] cursor-pointer"
              />
            </div>

            {/* Headcount Adjustments */}
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-[#A89D92]">Driver / Operations Headcount</span>
                <span className="text-[#A89D92] font-bold">
                  {params.hiringDelta > 0 ? '+' : ''}{params.hiringDelta} staff
                </span>
              </div>
              <input
                type="range"
                min="-50"
                max="50"
                value={params.hiringDelta}
                onChange={(e) => handleSliderChange('hiringDelta', Number(e.target.value))}
                className="w-full accent-[#FF6A00] cursor-pointer"
              />
            </div>
          </div>
        </GlowCard>

        {/* Center: Baseline vs Scenario Visualization */}
        <GlowCard className="lg:col-span-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-[#F5F0EA]">Baseline vs Scenario Comparison</h3>
            <span className="text-xs font-mono text-[#FF8A24]">
              {isSimulating ? 'Simulating...' : 'Computed in 6ms'}
            </span>
          </div>

          <ScenarioComparisonChart
            baselineRevenue={result?.baselineRevenue}
            simulatedRevenue={result?.simulatedRevenue}
            baselineProfit={result?.baselineProfit}
            simulatedProfit={result?.simulatedProfit}
            baselineCash={result?.baselineCashFlow}
            simulatedCash={result?.simulatedCashFlow}
            height={280}
          />

          <div className="p-3 rounded-xl bg-[#080604] border border-[#FF6A00]/14 space-y-2 text-xs">
            <span className="text-[10px] font-mono uppercase text-[#FF8A24] font-bold block">
              IDENTIFIED TRADEOFFS & SIDE EFFECTS:
            </span>
            {result?.tradeoffs.map((t, i) => (
              <p key={i} className="text-[#A89D92] flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-[#FFB15A] shrink-0" />
                <span>{t}</span>
              </p>
            ))}
          </div>
        </GlowCard>

        {/* Right: Predicted Metric Scorecard */}
        <GlowCard className="lg:col-span-3 space-y-4">
          <h3 className="text-sm font-bold text-[#F5F0EA] border-b border-[#FF6A00]/12 pb-2">
            Simulated Impact
          </h3>

          <div className="space-y-3 font-mono text-xs">
            <div className="p-3 rounded-xl bg-[#080604] border border-[#FF6A00]/15">
              <span className="text-[10px] text-[#6F665F] uppercase block">Revenue Outcome</span>
              <p className="text-xl font-bold text-[#FFB15A] mt-1">${result?.simulatedRevenue}M</p>
              <p className="text-[10px] text-[#FF8A24]">
                Baseline: ${result?.baselineRevenue}M
              </p>
            </div>

            <div className="p-3 rounded-xl bg-[#080604] border border-[#FF6A00]/15">
              <span className="text-[10px] text-[#6F665F] uppercase block">Operating Margin Profit</span>
              <p className="text-xl font-bold text-[#F5F0EA] mt-1">${result?.simulatedProfit}M</p>
              <p className="text-[10px] text-[#FF8A24]">
                Baseline: ${result?.baselineProfit}M
              </p>
            </div>

            <div className="p-3 rounded-xl bg-[#080604] border border-[#FF6A00]/15">
              <span className="text-[10px] text-[#6F665F] uppercase block">Risk Threat Score</span>
              <p className="text-xl font-bold text-[#FF6A00] mt-1">{result?.simulatedRiskScore} / 100</p>
              <p className="text-[10px] text-[#A89D92]">
                Baseline: {result?.baselineRiskScore} / 100
              </p>
            </div>
          </div>
        </GlowCard>
      </div>
    </div>
  );
};

export default WhatIfSimulationPage;
