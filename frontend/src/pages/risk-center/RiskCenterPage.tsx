import React, { useState, useEffect } from 'react';
import { ShieldAlert, AlertTriangle, ArrowRight, Filter, Zap } from 'lucide-react';
import SectionHeader from '@/components/SectionHeader';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';
import RiskCard from '@/components/RiskCard';
import HeatmapChart from '@/charts/HeatmapChart';
import RiskTrendChart from '@/charts/RiskTrendChart';
import { riskApi } from '@/api/riskApi';
import { RiskItem } from '@/types';

interface RiskCenterPageProps {
  onNavigate: (path: string) => void;
  onSelectRisk?: (risk: RiskItem) => void;
}

export const RiskCenterPage: React.FC<RiskCenterPageProps> = ({
  onNavigate,
  onSelectRisk,
}) => {
  const [risks, setRisks] = useState<RiskItem[]>([]);
  const [selectedRisk, setSelectedRisk] = useState<RiskItem | null>(null);
  const [activeCategory, setActiveCategory] = useState<string>('all');

  useEffect(() => {
    riskApi.getRisks().then((res) => {
      setRisks(res);
      setSelectedRisk(res[0]);
    });
  }, []);

  const filteredRisks = activeCategory === 'all'
    ? risks
    : risks.filter((r) => r.category === activeCategory);

  const totalExposure = risks.reduce((acc, curr) => {
    const num = parseFloat(curr.exposureAmount.replace(/[^0-9.]/g, '')) || 0;
    return acc + num;
  }, 0);

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#FF6A00]/14 pb-6">
        <div>
          <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold tracking-wider">
            ENTERPRISE THREAT RADAR
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F0EA] tracking-tight mt-1">
            Risk & Threat Intelligence Center
          </h1>
          <p className="text-xs text-[#A89D92] mt-1 font-mono">
            Quantified multi-variate risk modeling • Exposure formula: Probability × Impact × Exposure
          </p>
        </div>

        <div className="flex items-center gap-3">
          <GlowButton
            variant="secondary"
            size="sm"
            onClick={() => onNavigate('/simulation')}
          >
            Simulate Response Levers
          </GlowButton>
        </div>
      </div>

      {/* Top Threat Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono">
        <GlowCard className="p-4">
          <span className="text-[10px] text-[#6F665F] uppercase block">Total Net Exposure</span>
          <span className="text-2xl font-bold text-[#FFB15A] mt-1">${totalExposure.toFixed(2)}M</span>
          <span className="text-[11px] text-[#FF4500] block mt-0.5">Active Capital at Risk</span>
        </GlowCard>

        <GlowCard className="p-4">
          <span className="text-[10px] text-[#6F665F] uppercase block">Critical Threats</span>
          <span className="text-2xl font-bold text-[#FF4500] mt-1">
            {risks.filter((r) => r.severity === 'critical').length}
          </span>
          <span className="text-[11px] text-[#A89D92] block mt-0.5">Immediate SLA Impact</span>
        </GlowCard>

        <GlowCard className="p-4">
          <span className="text-[10px] text-[#6F665F] uppercase block">Avg Threat Probability</span>
          <span className="text-2xl font-bold text-[#FF8A24] mt-1">68.4%</span>
          <span className="text-[11px] text-[#A89D92] block mt-0.5">Bayesian Prior Model</span>
        </GlowCard>

        <GlowCard className="p-4">
          <span className="text-[10px] text-[#6F665F] uppercase block">Mitigation Pipeline</span>
          <span className="text-2xl font-bold text-[#F5F0EA] mt-1">3 Queued</span>
          <span className="text-[11px] text-[#FFB15A] block mt-0.5">Decisions Ready for Exec</span>
        </GlowCard>
      </div>

      {/* Probability vs Impact Scatter Matrix */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <GlowCard className="lg:col-span-8 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-[#F5F0EA]">Risk Matrix (Probability × Impact)</h3>
                <p className="text-xs text-[#A89D92] font-mono">
                  Bubble size represents capital exposure • Click bubble to inspect
                </p>
              </div>
            </div>
            <HeatmapChart
              risks={risks}
              onSelectRisk={(r) => setSelectedRisk(r)}
              height={320}
            />
          </div>
        </GlowCard>

        {/* Selected Risk Quick Inspector */}
        <GlowCard className="lg:col-span-4 flex flex-col justify-between border-[#FF6A00]/40">
          {selectedRisk ? (
            <div>
              <div className="flex items-center justify-between">
                <span className="px-2 py-0.5 rounded-full text-[10px] font-mono uppercase bg-[#FF4500]/15 text-[#FF6A00] font-bold border border-[#FF6A00]/30">
                  {selectedRisk.severity} Priority
                </span>
                <span className="text-xs font-mono text-[#A89D92]">{selectedRisk.detectedAt}</span>
              </div>

              <h4 className="text-lg font-bold text-[#F5F0EA] mt-3">{selectedRisk.title}</h4>
              <p className="text-xs text-[#A89D92] mt-2">
                Identified through continuous variance telemetry in operational logs.
              </p>

              <div className="mt-4 p-3 rounded-xl bg-[#080604] border border-[#FF6A00]/15 space-y-2 text-xs font-mono">
                <div className="flex justify-between">
                  <span className="text-[#6F665F]">Capital Exposure:</span>
                  <span className="text-[#FFB15A] font-bold">{selectedRisk.exposureAmount}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-[#6F665F]">Composite Score:</span>
                  <span className="text-[#FF8A24] font-bold">{selectedRisk.score} / 100</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-[#6F665F]">Probability:</span>
                  <span className="text-[#F5F0EA]">{Math.round(selectedRisk.probability * 100)}%</span>
                </div>
              </div>

              <div className="mt-4 space-y-1 text-xs">
                <span className="text-[11px] font-mono text-[#6F665F] uppercase block">Primary Triggers</span>
                {selectedRisk.primaryDrivers.map((d, i) => (
                  <p key={i} className="text-[#A89D92] flex items-center gap-1.5">
                    <span className="w-1 h-1 rounded-full bg-[#FF6A00]" />
                    <span>{d}</span>
                  </p>
                ))}
              </div>
            </div>
          ) : (
            <p className="text-xs font-mono text-[#6F665F]">Select a risk to inspect details</p>
          )}

          <div className="pt-4 border-t border-[#FF6A00]/10 mt-6 flex gap-2">
            <GlowButton
              size="sm"
              className="w-full"
              onClick={() => onNavigate('/investigation')}
            >
              Investigate Causal Chain
            </GlowButton>
            <GlowButton
              variant="secondary"
              size="sm"
              className="w-full"
              onClick={() => onNavigate('/simulation')}
            >
              Simulate Response
            </GlowButton>
          </div>
        </GlowCard>
      </div>

      {/* Category Filter Pills & List of all Risks */}
      <div className="space-y-4">
        <div className="flex flex-wrap items-center gap-2">
          {['all', 'financial', 'operational', 'supply_chain'].map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`px-3 py-1 rounded-lg text-xs font-mono uppercase transition-colors ${
                activeCategory === cat
                  ? 'bg-[#FF6A00] text-white font-semibold'
                  : 'bg-[#120C08] text-[#A89D92] border border-[#FF6A00]/15 hover:border-[#FF6A00]/40'
              }`}
            >
              {cat === 'all' ? 'All Threats' : cat.replace('_', ' ')}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {filteredRisks.map((r) => (
            <RiskCard
              key={r.id}
              risk={r}
              onClick={() => setSelectedRisk(r)}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default RiskCenterPage;
