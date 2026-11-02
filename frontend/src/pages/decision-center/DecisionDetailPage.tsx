import React from 'react';
import { ArrowLeft, CheckCircle2, UserCheck, ShieldCheck, Zap } from 'lucide-react';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';

export const DecisionDetailPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <button
        onClick={() => onNavigate('/decision-center')}
        className="inline-flex items-center gap-2 text-xs font-mono text-[#A89D92] hover:text-[#FFB15A]"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Decision Center
      </button>

      <GlowCard className="p-8 space-y-6">
        <div className="flex items-center justify-between">
          <span className="px-3 py-1 rounded-full text-xs font-mono uppercase bg-[#FF6A00]/15 text-[#FF8A24] font-bold border border-[#FF6A00]/30">
            OPERATIONAL STRATEGY DECISION
          </span>
          <span className="flex items-center gap-1.5 text-xs font-mono text-[#FFB15A]">
            <UserCheck className="w-4 h-4 text-[#FF6A00]" />
            HUMAN APPROVAL REQUIRED
          </span>
        </div>

        <h1 className="text-2xl font-bold text-[#F5F0EA]">
          Shift 24% Mid-Haul Corridors to Intermodal Rail
        </h1>
        <p className="text-sm text-[#A89D92] leading-relaxed">
          Transfer heavy freight volumes from Gulf Coast highway lanes to Kansas City Southern rail intermodal to bypass regional truckload diesel surcharges.
        </p>

        <div className="p-4 rounded-xl bg-[#080604] border border-[#FF6A00]/20 grid grid-cols-1 sm:grid-cols-3 gap-4 font-mono text-center">
          <div>
            <span className="text-[10px] text-[#6F665F] uppercase block">Expected Margin Impact</span>
            <span className="text-lg font-bold text-[#FFB15A]">+$1.15M</span>
          </div>
          <div>
            <span className="text-[10px] text-[#6F665F] uppercase block">Risk Reduction Score</span>
            <span className="text-lg font-bold text-[#FF8A24]">88 → 52</span>
          </div>
          <div>
            <span className="text-[10px] text-[#6F665F] uppercase block">Model Confidence</span>
            <span className="text-lg font-bold text-[#F5F0EA]">93%</span>
          </div>
        </div>

        <div className="pt-4 flex items-center justify-end gap-3 border-t border-[#FF6A00]/12">
          <GlowButton variant="secondary" size="md" onClick={() => onNavigate('/simulation')}>
            Simulate in Scenario Studio
          </GlowButton>
          <GlowButton size="md" onClick={() => onNavigate('/decision-center')}>
            Authorize & Execute Strategy
          </GlowButton>
        </div>
      </GlowCard>
    </div>
  );
};

export default DecisionDetailPage;
