import React from 'react';
import { ArrowLeft, Megaphone, Target } from 'lucide-react';
import MetricCard from '@/components/MetricCard';
import GlowCard from '@/components/GlowCard';
import ContributionChart from '@/charts/ContributionChart';

export const MarketingPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      <button
        onClick={() => onNavigate('/analytics')}
        className="inline-flex items-center gap-2 text-xs font-mono text-[#A89D92] hover:text-[#FFB15A]"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Analytics Overview
      </button>

      <div className="border-b border-[#FF6A00]/14 pb-4">
        <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold">GROWTH & PIPELINE</span>
        <h1 className="text-2xl font-bold text-[#F5F0EA] mt-1">Marketing Acquisition & Spend Velocity</h1>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <MetricCard title="Discretionary Marketing Spend" value="$4.20M" changePercent={-8.0} trend="down" />
        <MetricCard title="Blended Customer CAC" value="$2,450" changePercent={-4.5} trend="down" />
        <MetricCard title="Pipeline Multiplier" value="4.8x" changePercent={1.2} trend="up" />
      </div>

      <GlowCard>
        <h3 className="text-base font-bold text-[#F5F0EA] mb-4">Pipeline Attribution Contribution</h3>
        <ContributionChart height={280} />
      </GlowCard>
    </div>
  );
};

export default MarketingPage;
