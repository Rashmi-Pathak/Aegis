import React from 'react';
import { ArrowLeft, Cpu, Database, Network, ShieldCheck, Zap } from 'lucide-react';
import GlowButton from '@/components/GlowButton';
import GlowCard from '@/components/GlowCard';

export const HowAegisWorksPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  return (
    <div className="min-h-screen bg-[#080604] text-[#F5F0EA] p-6 sm:p-12 max-w-6xl mx-auto">
      <button
        onClick={() => onNavigate('/')}
        className="inline-flex items-center gap-2 text-xs font-mono text-[#A89D92] hover:text-[#FFB15A] mb-8"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Overview
      </button>

      <div className="space-y-4 mb-12">
        <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold tracking-widest">
          SYSTEM ARCHITECTURE
        </span>
        <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight">How AEGIS Works</h1>
        <p className="text-[#A89D92] text-sm sm:text-base max-w-2xl leading-relaxed">
          A breakdown of the five core intelligence engines executing continuously across multi-tenant Python workers.
        </p>
      </div>

      <div className="space-y-8">
        {[
          {
            num: '01',
            title: 'Dynamic Data Ingestion & Canonical Schema Mapping',
            desc: 'AEGIS ingests heterogeneous data formats without requiring pre-defined schemas. It uses automatic column classification, null outlier handling, and converts proprietary records into the canonical business model.',
            icon: Database,
          },
          {
            num: '02',
            title: 'Statistical & Multi-Variate Anomaly Detection',
            desc: 'Isolation Forests, Local Outlier Factor (LOF), and DBSCAN engines execute concurrently on time-series telemetry to detect subtle multidimensional baseline shifts before thresholds trigger.',
            icon: Cpu,
          },
          {
            num: '03',
            title: 'Business Digital Twin & Causal Graph Propagation',
            desc: 'Using NetworkX graph topologies, AEGIS models every cross-domain business dependency. When an operational bottleneck occurs, the graph propagates the causal chain directly into gross profit and cash flow.',
            icon: Network,
          },
          {
            num: '04',
            title: 'Multi-Horizon Ensemble Forecasting',
            desc: 'Combines gradient boosted trees (LightGBM) with classical statistical time series (SARIMAX) to generate continuous 30, 60, and 90-day predictive envelopes with 95% confidence bands.',
            icon: Zap,
          },
          {
            num: '05',
            title: 'Prescriptive Decision Engine & What-If Simulation',
            desc: 'Generates ranked, actionable remediation strategies with estimated ROI and risk reduction. Executives can simulate multiple concurrent levers to stress-test outcomes.',
            icon: ShieldCheck,
          },
        ].map((item) => {
          const Icon = item.icon;
          return (
            <GlowCard key={item.num} className="flex flex-col sm:flex-row items-start gap-6">
              <div className="w-14 h-14 rounded-2xl bg-[#FF6A00]/15 border border-[#FF6A00]/30 flex items-center justify-center text-[#FF6A00] shrink-0 font-mono font-bold text-lg">
                {item.num}
              </div>
              <div className="space-y-2">
                <h3 className="text-lg font-bold text-[#F5F0EA] flex items-center gap-2">
                  <Icon className="w-5 h-5 text-[#FF8A24]" />
                  <span>{item.title}</span>
                </h3>
                <p className="text-xs sm:text-sm text-[#A89D92] leading-relaxed">{item.desc}</p>
              </div>
            </GlowCard>
          );
        })}
      </div>

      <div className="mt-12 text-center">
        <GlowButton size="lg" onClick={() => onNavigate('/demo')}>
          Explore Live Demonstrations
        </GlowButton>
      </div>
    </div>
  );
};

export default HowAegisWorksPage;
