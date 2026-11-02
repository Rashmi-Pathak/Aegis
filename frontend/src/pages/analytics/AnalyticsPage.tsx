import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, DollarSign, Users, Package, RefreshCw } from 'lucide-react';
import SectionHeader from '@/components/SectionHeader';
import MetricCard from '@/components/MetricCard';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';
import RevenueChart from '@/charts/RevenueChart';
import ContributionChart from '@/charts/ContributionChart';
import DataTable from '@/components/DataTable';
import { analyticsApi, AnalyticsOverview } from '@/api/analyticsApi';

export const AnalyticsPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const [data, setData] = useState<AnalyticsOverview | null>(null);

  useEffect(() => {
    analyticsApi.getOverview().then(setData);
  }, []);

  if (!data) return null;

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#FF6A00]/14 pb-6">
        <div>
          <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold tracking-wider">
            ENTERPRISE PERFORMANCE REPOSITORY
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F0EA] tracking-tight mt-1">
            Business Analytics & Performance
          </h1>
          <p className="text-xs text-[#A89D92] mt-1 font-mono">
            Canonical KPI metrics synchronized across all ingested transactional logs
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {['Revenue', 'Customers', 'Inventory', 'Finance', 'Marketing'].map((tab) => (
            <button
              key={tab}
              onClick={() => onNavigate(`/analytics/${tab.toLowerCase()}`)}
              className="px-3 py-1.5 rounded-xl bg-[#120C08] border border-[#FF6A00]/18 text-xs font-mono text-[#A89D92] hover:text-[#F5F0EA] hover:border-[#FF6A00]/40 transition-colors"
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Primary KPI Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard {...data.kpis.revenue} />
        <MetricCard {...data.kpis.operatingMargin} />
        <MetricCard {...data.kpis.cashFlow} />
        <MetricCard {...data.kpis.customerHealth} />
      </div>

      {/* Main Revenue Trajectory & Contribution Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <GlowCard className="lg:col-span-8">
          <h3 className="text-base font-bold text-[#F5F0EA] mb-4">Historical Revenue vs Plan Benchmark</h3>
          <RevenueChart data={data.revenueTrend} height={280} />
        </GlowCard>

        <GlowCard className="lg:col-span-4">
          <h3 className="text-base font-bold text-[#F5F0EA] mb-4">Business Unit Contribution</h3>
          <ContributionChart height={280} />
        </GlowCard>
      </div>

      {/* Performance by Business Division Table */}
      <div className="space-y-4">
        <SectionHeader
          badge="SEGMENT ANALYSIS"
          title="Division & Corridor Performance"
          description="Operating margins and real-time risk scores by business unit."
        />

        <DataTable
          columns={[
            { key: 'name', header: 'Operating Division' },
            {
              key: 'revenue',
              header: 'Revenue',
              render: (item: any) => <span className="font-mono font-bold text-[#FFB15A]">${item.revenue}M</span>,
            },
            {
              key: 'margin',
              header: 'Margin %',
              render: (item: any) => <span className="font-mono text-[#F5F0EA]">{item.margin}%</span>,
            },
            {
              key: 'riskScore',
              header: 'Risk Score',
              render: (item: any) => (
                <span
                  className={`font-mono font-bold ${
                    item.riskScore > 60 ? 'text-[#FF4500]' : 'text-emerald-400'
                  }`}
                >
                  {item.riskScore} / 100
                </span>
              ),
            },
          ]}
          data={data.categoryPerformance}
          keyExtractor={(item: any) => item.name}
        />
      </div>
    </div>
  );
};

export default AnalyticsPage;
