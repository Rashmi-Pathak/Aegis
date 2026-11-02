import React from 'react';
import { ArrowLeft, DollarSign, TrendingUp } from 'lucide-react';
import SectionHeader from '@/components/SectionHeader';
import MetricCard from '@/components/MetricCard';
import GlowCard from '@/components/GlowCard';
import RevenueChart from '@/charts/RevenueChart';
import WaterfallChart from '@/charts/WaterfallChart';

export const RevenuePage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      <button
        onClick={() => onNavigate('/analytics')}
        className="inline-flex items-center gap-2 text-xs font-mono text-[#A89D92] hover:text-[#FFB15A]"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Analytics Overview
      </button>

      <div className="border-b border-[#FF6A00]/14 pb-4">
        <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold">REVENUE INTELLIGENCE</span>
        <h1 className="text-2xl font-bold text-[#F5F0EA] mt-1">Gross & Net Revenue Analytics</h1>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <MetricCard title="Gross Billable Revenue" value="$148.24M" changePercent={8.4} trend="up" />
        <MetricCard title="Average Revenue Per Shipper" value="$42,800" changePercent={3.2} trend="up" />
        <MetricCard title="Net Price Realization" value="98.1%" changePercent={-0.8} trend="down" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <GlowCard className="lg:col-span-8">
          <h3 className="text-base font-bold text-[#F5F0EA] mb-4">Historical Revenue vs Plan Benchmark</h3>
          <RevenueChart height={280} />
        </GlowCard>

        <GlowCard className="lg:col-span-4">
          <h3 className="text-base font-bold text-[#F5F0EA] mb-4">Quarterly Bridge Waterfall</h3>
          <WaterfallChart height={280} />
        </GlowCard>
      </div>
    </div>
  );
};

export default RevenuePage;
