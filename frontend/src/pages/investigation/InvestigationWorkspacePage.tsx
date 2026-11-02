import React, { useState } from 'react';
import {
  SearchCode,
  ArrowRight,
  GitCommit,
  Network,
  FileCheck2,
  Clock,
  AlertTriangle,
  Play,
} from 'lucide-react';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';
import SectionHeader from '@/components/SectionHeader';

interface InvestigationWorkspacePageProps {
  onNavigate: (path: string) => void;
}

export const InvestigationWorkspacePage: React.FC<InvestigationWorkspacePageProps> = ({
  onNavigate,
}) => {
  const [activeCase, setActiveCase] = useState({
    id: 'CASE-2026-0814',
    title: 'Fuel Benchmark Squeeze & Dwell Delay Cascade',
    status: 'ACTIVE INVESTIGATION',
    confidence: '94.2%',
    detectedAt: '2026-03-02 09:14 UTC',
    rootCause: 'Gulf Coast Wholesale Diesel Surge (+28%) + Long Beach Terminal 4 Chassis Deficit',
    contributingFactors: [
      'Uncontracted retail station pump purchases along Southwest I-10 corridor',
      'Port container gate dwell exceeding free-time allowance (+48h)',
      'Legacy master shipper contracts lacking automatic fuel index passthrough',
    ],
    affectedMetrics: [
      { name: 'Gross Margin Compression', impact: '-2.8% ($2.85M annualized)' },
      { name: 'OTIF SLA Performance', impact: '-4.1% late penalties' },
      { name: 'Fleet Fuel Burn Efficiency', impact: '+14.8% cost per mile' },
    ],
    evidence: [
      { id: 'EV-1', source: 'Fleet Telemetry IoT', detail: '342 vehicles registered engine idle time > 4.5h during Houston depot queue.' },
      { id: 'EV-2', source: 'EDI-214 Messages', detail: 'Terminal 4 demurrage charges accelerated from $4.2K to $18.6K per day.' },
      { id: 'EV-3', source: 'Commodity Regressor Feed', detail: 'NYMEX ULSD futures broke 90-day resistance line at $2.82/gal.' },
    ],
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#FF6A00]/14 pb-5">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-[#FF8A24] mb-1">
            <SearchCode className="w-4 h-4 text-[#FF6A00]" />
            <span>CAUSAL INVESTIGATION WORKSPACE</span>
          </div>
          <h1 className="text-2xl font-bold text-[#F5F0EA]">{activeCase.title}</h1>
          <p className="text-xs font-mono text-[#A89D92] mt-0.5">
            Incident ID: <strong className="text-[#FFB15A]">{activeCase.id}</strong> • Root Cause Confidence: {activeCase.confidence}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <GlowButton
            variant="secondary"
            size="sm"
            onClick={() => onNavigate('/simulation')}
          >
            <Play className="w-3.5 h-3.5 mr-1" />
            Simulate Response Levers
          </GlowButton>
        </div>
      </div>

      {/* Tri-Pane Console: Left Case Info, Center Causal Flow, Right Evidence Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left: Case Information & Root Cause */}
        <GlowCard className="lg:col-span-4 space-y-5">
          <div>
            <span className="text-[10px] font-mono uppercase text-[#FF8A24] font-bold tracking-wider">
              ROOT CAUSE ANALYSIS
            </span>
            <div className="mt-2 p-3.5 rounded-xl bg-[#FF4500]/10 border border-[#FF4500]/30 text-xs font-mono text-[#FFB15A] leading-relaxed">
              <strong className="text-[#FF6A00] block mb-1">PRIMARY HYPOTHESIS:</strong>
              {activeCase.rootCause}
            </div>
          </div>

          <div>
            <h4 className="text-xs font-mono text-[#A89D92] uppercase font-bold mb-2">Contributing Factors</h4>
            <div className="space-y-2 text-xs">
              {activeCase.contributingFactors.map((factor, i) => (
                <div key={i} className="p-2.5 rounded-lg bg-[#080604] border border-[#FF6A00]/14 flex items-start gap-2">
                  <span className="text-[#FF6A00] font-mono font-bold mt-0.5">•</span>
                  <span className="text-[#F5F0EA]">{factor}</span>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h4 className="text-xs font-mono text-[#A89D92] uppercase font-bold mb-2">Quantified Business Impact</h4>
            <div className="space-y-2 text-xs font-mono">
              {activeCase.affectedMetrics.map((met, i) => (
                <div key={i} className="p-2 rounded-lg bg-[#17100B] flex justify-between border border-[#FF6A00]/10">
                  <span className="text-[#A89D92]">{met.name}</span>
                  <span className="text-[#FFB15A] font-bold">{met.impact}</span>
                </div>
              ))}
            </div>
          </div>
        </GlowCard>

        {/* Center: Causal Graph Flow Visualization */}
        <GlowCard className="lg:col-span-5 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-bold text-[#F5F0EA] flex items-center gap-2">
              <Network className="w-4 h-4 text-[#FF6A00]" />
              <span>Causal Chain Network</span>
            </h4>
            <span className="text-[10px] font-mono text-[#6F665F]">TOPOLOGICAL SEQUENCE</span>
          </div>

          <div className="space-y-3 py-2">
            {[
              { step: '01', node: 'Diesel Wholesale Benchmark (+28%)', type: 'External Commodity Shock', color: 'border-[#FF4500]' },
              { step: '02', node: 'Terminal Queue & Idling Variance', type: 'Fleet Operational Inefficiency', color: 'border-[#FF6A00]' },
              { step: '03', node: 'Port Gate Dwell Exceedance', type: 'Intermodal Logistics Constraint', color: 'border-[#FF8A24]' },
              { step: '04', node: 'Contract Surcharge Clause Lags', type: 'Commercial SLA Exposure', color: 'border-[#FFB15A]' },
              { step: '05', node: 'Operating Margin Compression ($2.85M)', type: 'Consolidated Downside Threat', color: 'border-[#FF4500]' },
            ].map((chain, idx) => (
              <React.Fragment key={chain.step}>
                <div className={`p-3 rounded-xl bg-[#080604] border ${chain.color} flex items-center justify-between text-xs font-mono shadow-[0_0_15px_rgba(255,106,0,0.08)]`}>
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 rounded-md bg-[#FF6A00]/20 text-[#FF8A24] flex items-center justify-center font-bold text-[11px]">
                      {chain.step}
                    </span>
                    <div>
                      <p className="font-semibold text-[#F5F0EA]">{chain.node}</p>
                      <p className="text-[10px] text-[#6F665F]">{chain.type}</p>
                    </div>
                  </div>
                </div>
                {idx < 4 && (
                  <div className="w-0.5 h-3 bg-gradient-to-b from-[#FF6A00] to-[#FF8A24] mx-auto" />
                )}
              </React.Fragment>
            ))}
          </div>
        </GlowCard>

        {/* Right: Evidence Panel */}
        <GlowCard className="lg:col-span-3 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-bold text-[#F5F0EA] flex items-center gap-2">
              <FileCheck2 className="w-4 h-4 text-[#FF8A24]" />
              <span>Evidence Ledger</span>
            </h4>
            <span className="text-[10px] font-mono text-[#6F665F]">3 VERIFIED</span>
          </div>

          <div className="space-y-3">
            {activeCase.evidence.map((ev) => (
              <div key={ev.id} className="p-3 rounded-xl bg-[#080604] border border-[#FF6A00]/15 space-y-1 text-xs">
                <div className="flex justify-between text-[10px] font-mono text-[#FF8A24]">
                  <span>{ev.id}</span>
                  <span className="text-[#6F665F]">{ev.source}</span>
                </div>
                <p className="text-xs text-[#A89D92] leading-snug">{ev.detail}</p>
              </div>
            ))}
          </div>

          <div className="pt-3 border-t border-[#FF6A00]/12">
            <GlowButton
              size="sm"
              className="w-full"
              onClick={() => onNavigate('/decision-center')}
            >
              Review Prescribed Decisions
            </GlowButton>
          </div>
        </GlowCard>
      </div>
    </div>
  );
};

export default InvestigationWorkspacePage;
