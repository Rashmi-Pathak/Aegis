import React from 'react';
import { ArrowLeft, Package, Clock } from 'lucide-react';
import MetricCard from '@/components/MetricCard';
import GlowCard from '@/components/GlowCard';
import InventoryTrendChart from '@/charts/InventoryTrendChart';

export const InventoryPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      <button
        onClick={() => onNavigate('/analytics')}
        className="inline-flex items-center gap-2 text-xs font-mono text-[#A89D92] hover:text-[#FFB15A]"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Analytics Overview
      </button>

      <div className="border-b border-[#FF6A00]/14 pb-4">
        <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold">SUPPLY & ASSET INTELLIGENCE</span>
        <h1 className="text-2xl font-bold text-[#F5F0EA] mt-1">Fleet & Inventory Asset Utilization</h1>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <MetricCard title="Active Fleet Utilization" value="84.6%" changePercent={-3.4} trend="down" />
        <MetricCard title="Average Port Dwell Time" value="38.4h" changePercent={14.2} trend="up" isAnomaly={true} />
        <MetricCard title="Turnover Rate" value="12.4x" changePercent={1.1} trend="up" />
      </div>

      <GlowCard>
        <h3 className="text-base font-bold text-[#F5F0EA] mb-4">Fleet Asset Utilization vs Idle Dwell</h3>
        <InventoryTrendChart height={280} />
      </GlowCard>
    </div>
  );
};

export default InventoryPage;
