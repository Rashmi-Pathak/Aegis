import React from 'react';
import { ArrowLeft, DollarSign, Wallet } from 'lucide-react';
import MetricCard from '@/components/MetricCard';
import GlowCard from '@/components/GlowCard';
import CashFlowChart from '@/charts/CashFlowChart';

export const FinancePage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      <button
        onClick={() => onNavigate('/analytics')}
        className="inline-flex items-center gap-2 text-xs font-mono text-[#A89D92] hover:text-[#FFB15A]"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Analytics Overview
      </button>

      <div className="border-b border-[#FF6A00]/14 pb-4">
        <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold">FINANCIAL INTELLIGENCE</span>
        <h1 className="text-2xl font-bold text-[#F5F0EA] mt-1">Cash Flow & Capital Liquidity</h1>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <MetricCard title="Free Cash Flow" value="$18.65M" changePercent={-4.1} trend="down" />
        <MetricCard title="Operating Cash Flow" value="$24.10M" changePercent={2.4} trend="up" />
        <MetricCard title="Cash Runway" value="18 Months" changePercent={0} trend="neutral" />
      </div>

      <GlowCard>
        <h3 className="text-base font-bold text-[#F5F0EA] mb-4">Monthly Inflow vs Outflow Cash Liquidity</h3>
        <CashFlowChart height={280} />
      </GlowCard>
    </div>
  );
};

export default FinancePage;
