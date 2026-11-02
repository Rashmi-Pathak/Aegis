import React, { useState, useEffect } from 'react';
import { ArrowLeft, ShieldAlert, Zap, Sliders, SearchCode, CheckCircle2 } from 'lucide-react';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';
import { riskApi } from '@/api/riskApi';
import { RiskItem } from '@/types';

export const RiskDetailPage: React.FC<{
  onNavigate: (path: string) => void;
  riskId?: string;
}> = ({ onNavigate, riskId = 'rsk_fuel_surge' }) => {
  const [risk, setRisk] = useState<RiskItem | null>(null);

  useEffect(() => {
    riskApi.getRiskDetail(riskId).then(setRisk);
  }, [riskId]);

  if (!risk) return null;

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <button
        onClick={() => onNavigate('/risk-center')}
        className="inline-flex items-center gap-2 text-xs font-mono text-[#A89D92] hover:text-[#FFB15A]"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Risk Matrix
      </button>

      {/* Main Threat Header */}
      <div className="p-8 rounded-3xl bg-[#120C08] border border-[#FF6A00]/30 shadow-[0_0_30px_rgba(255,106,0,0.15)] flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-3 font-mono text-xs mb-2">
            <span className="px-3 py-1 rounded-full uppercase bg-[#FF4500]/20 text-[#FF6A00] font-bold border border-[#FF6A00]/40">
              {risk.severity} Threat Signal
            </span>
            <span className="text-[#A89D92]">{risk.detectedAt}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F0EA]">{risk.title}</h1>
          <p className="text-xs text-[#FFB15A] font-mono mt-1">Status: {risk.status.toUpperCase()}</p>
        </div>

        <div className="flex items-center gap-3">
          <GlowButton
            variant="secondary"
            size="md"
            onClick={() => onNavigate('/simulation')}
          >
            <Sliders className="w-4 h-4 mr-1.5" />
            SIMULATE RESPONSE
          </GlowButton>
          <GlowButton
            size="md"
            onClick={() => onNavigate('/investigation')}
          >
            <SearchCode className="w-4 h-4 mr-1.5" />
            INVESTIGATE
          </GlowButton>
        </div>
      </div>

      {/* Quantitative Drivers & Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 font-mono text-center">
        <GlowCard className="p-4">
          <span className="text-[10px] text-[#6F665F] uppercase">Net Exposure</span>
          <p className="text-2xl font-bold text-[#FFB15A] mt-1">{risk.exposureAmount}</p>
        </GlowCard>
        <GlowCard className="p-4">
          <span className="text-[10px] text-[#6F665F] uppercase">Composite Risk Score</span>
          <p className="text-2xl font-bold text-[#FF6A00] mt-1">{risk.score} / 100</p>
        </GlowCard>
        <GlowCard className="p-4">
          <span className="text-[10px] text-[#6F665F] uppercase">Likelihood Probability</span>
          <p className="text-2xl font-bold text-[#F5F0EA] mt-1">{Math.round(risk.probability * 100)}%</p>
        </GlowCard>
        <GlowCard className="p-4">
          <span className="text-[10px] text-[#6F665F] uppercase">Financial Impact Severity</span>
          <p className="text-2xl font-bold text-[#FF8A24] mt-1">{risk.impact} / 100</p>
        </GlowCard>
      </div>

      {/* Drivers & Propagation */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <GlowCard>
          <h4 className="text-base font-bold text-[#F5F0EA] mb-4">Primary & Secondary Drivers</h4>
          <div className="space-y-3 text-xs">
            {risk.primaryDrivers.map((driver, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-[#080604] border border-[#FF6A00]/15 flex items-center gap-3">
                <span className="w-2 h-2 rounded-full bg-[#FF6A00]" />
                <span className="text-[#F5F0EA] font-medium">{driver}</span>
              </div>
            ))}
            {risk.secondaryDrivers.map((driver, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-[#080604] border border-[#FF6A00]/10 flex items-center gap-3 opacity-75">
                <span className="w-1.5 h-1.5 rounded-full bg-[#A89D92]" />
                <span className="text-[#A89D92]">{driver}</span>
              </div>
            ))}
          </div>
        </GlowCard>

        <GlowCard>
          <h4 className="text-base font-bold text-[#F5F0EA] mb-4">Prescriptive Remediations</h4>
          <div className="space-y-3 text-xs">
            {risk.recommendedActions.map((action, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-[#FF6A00]/10 border border-[#FF6A00]/25 flex items-start gap-3">
                <CheckCircle2 className="w-4 h-4 text-[#FF8A24] shrink-0 mt-0.5" />
                <span className="text-[#F5F0EA] leading-relaxed">{action}</span>
              </div>
            ))}
          </div>
        </GlowCard>
      </div>
    </div>
  );
};

export default RiskDetailPage;
