import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  AlertTriangle,
  ShieldAlert,
  Sliders,
  Network,
  RefreshCw,
  ArrowRight,
  Zap,
} from 'lucide-react';
import MetricCard from '@/components/MetricCard';
import RiskCard from '@/components/RiskCard';
import ForecastCard from '@/components/ForecastCard';
import DecisionCard from '@/components/DecisionCard';
import AnomalyCard from '@/components/AnomalyCard';
import HealthScoreCard from '@/components/HealthScoreCard';
import SectionHeader from '@/components/SectionHeader';
import GlowButton from '@/components/GlowButton';
import GlowCard from '@/components/GlowCard';
import RevenueChart from '@/charts/RevenueChart';
import HeatmapChart from '@/charts/HeatmapChart';
import AnomalyTimeline from '@/charts/AnomalyTimeline';
import { analyticsApi, AnalyticsOverview } from '@/api/analyticsApi';
import { riskApi } from '@/api/riskApi';
import { forecastApi } from '@/api/forecastApi';
import { decisionApi } from '@/api/decisionApi';
import { anomalyApi } from '@/api/anomalyApi';
import { DEMO_BUSINESSES } from '@/api/demoApi';
import { RiskItem, ForecastItem, DecisionItem, AnomalyItem } from '@/types';

interface ExecutiveCommandCenterPageProps {
  onNavigate: (path: string) => void;
  activeBusinessId?: string;
}

export const ExecutiveCommandCenterPage: React.FC<ExecutiveCommandCenterPageProps> = ({
  onNavigate,
  activeBusinessId = 'primelogix',
}) => {
  const [loading, setLoading] = useState(true);
  const [overview, setOverview] = useState<AnalyticsOverview | null>(null);
  const [risks, setRisks] = useState<RiskItem[]>([]);
  const [forecasts, setForecasts] = useState<ForecastItem[]>([]);
  const [decisions, setDecisions] = useState<DecisionItem[]>([]);
  const [anomalies, setAnomalies] = useState<AnomalyItem[]>([]);

  const activeBusiness =
    DEMO_BUSINESSES.find((b) => b.id.toLowerCase() === activeBusinessId.toLowerCase()) ||
    DEMO_BUSINESSES[0];

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const [ov, r, f, d, a] = await Promise.all([
          analyticsApi.getOverview(),
          riskApi.getRisks(),
          forecastApi.getForecasts(),
          decisionApi.getDecisions(),
          anomalyApi.getAnomalies(),
        ]);
        setOverview(ov);
        setRisks(r);
        setForecasts(f);
        setDecisions(d);
        setAnomalies(a);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [activeBusinessId]);

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      {/* 1. TOP HEADER & HEALTH OVERVIEW */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#FF6A00]/14 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-[#FF8A24] mb-1">
            <span className="w-2 h-2 rounded-full bg-[#FF6A00] animate-ping" />
            <span>AUTONOMOUS BUSINESS INTELLIGENCE RUNTIME</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F0EA] tracking-tight">
            {activeBusiness.name} Executive Command Center
          </h1>
          <p className="text-xs text-[#A89D92] mt-1 font-mono">
            Industry: {activeBusiness.industry} • Live Digital Twin Active • 90-Day Outlook
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <GlowButton
            variant="secondary"
            size="sm"
            onClick={() => onNavigate('/simulation')}
          >
            Open Simulator
          </GlowButton>
          <GlowButton
            size="sm"
            showArrow
            onClick={() => onNavigate('/risk-center')}
          >
            Mitigate Threats ({risks.length})
          </GlowButton>
        </div>
      </div>

      {/* 2. HEALTH SCORE & PRIMARY KPIS */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Health Score Card */}
        <div className="lg:col-span-5">
          <HealthScoreCard
            score={activeBusiness.healthScore}
            title={`${activeBusiness.name} Composite Health`}
            subtitle="Calculated in real-time by weighting revenue growth, margin compression risks, and fleet idle time."
          />
        </div>

        {/* Top 3 Primary Metrics */}
        <div className="lg:col-span-7 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <MetricCard
            title="Operating Revenue"
            value={activeBusiness.metrics.revenue}
            changePercent={8.4}
            trend="up"
            timeframe="vs target forecast"
          />
          <MetricCard
            title="Gross Margin"
            value={activeBusiness.metrics.margin}
            changePercent={-2.8}
            trend="down"
            isAnomaly={true}
            timeframe="compression warning"
          />
          <MetricCard
            title="Free Cash Flow"
            value="$18.65M"
            changePercent={-4.1}
            trend="down"
            timeframe="trailing 30 days"
          />
        </div>
      </div>

      {/* 3. CORE INTELLIGENCE TELEMETRY: FORECAST VS ANOMALY FEED */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Revenue Performance & AI Forecast */}
        <GlowCard className="lg:col-span-8 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-[#F5F0EA]">Revenue Trajectory & Target Plan</h3>
                <p className="text-xs text-[#A89D92] font-mono">Monthly actuals vs budgeted plan benchmark</p>
              </div>
              <button
                onClick={() => onNavigate('/analytics')}
                className="text-xs font-mono text-[#FF8A24] hover:text-[#FFB15A] flex items-center gap-1"
              >
                <span>Analytics Detail</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
            <RevenueChart height={260} />
          </div>
        </GlowCard>

        {/* Live Anomaly Feed */}
        <GlowCard className="lg:col-span-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-base font-bold text-[#F5F0EA] flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-[#FF6A00]" />
                <span>Detected Anomalies</span>
              </h3>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-[#FF6A00]/20 text-[#FFB15A]">
                {anomalies.length} ACTIVE
              </span>
            </div>
            <div className="space-y-3">
              {anomalies.slice(0, 2).map((a) => (
                <div key={a.id} className="p-3 rounded-xl bg-[#080604] border border-[#FF6A00]/15 space-y-1">
                  <div className="flex justify-between text-[10px] font-mono">
                    <span className="text-[#FF4500] uppercase font-bold">{a.severity}</span>
                    <span className="text-[#6F665F]">{a.detectedAt}</span>
                  </div>
                  <h4 className="text-xs font-semibold text-[#F5F0EA]">{a.metric}</h4>
                  <p className="text-[11px] text-[#A89D92] leading-tight">{a.explanation}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-3 border-t border-[#FF6A00]/10 mt-4">
            <button
              onClick={() => onNavigate('/anomalies')}
              className="w-full text-center text-xs font-mono text-[#FF8A24] hover:text-[#FFB15A] block"
            >
              View All Anomaly Streams →
            </button>
          </div>
        </GlowCard>
      </div>

      {/* 4. ACTIVE THREATS & RISK OVERVIEW */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <SectionHeader
            badge="EXPOSURE RADAR"
            title="High-Priority Threat Signals"
            description="Autonomous risk detection ranked by total capital exposure."
            className="mb-0"
          />
          <button
            onClick={() => onNavigate('/risk-center')}
            className="text-xs font-mono text-[#FF8A24] hover:text-[#FFB15A] flex items-center gap-1"
          >
            <span>Full Risk Matrix</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {risks.slice(0, 4).map((r) => (
            <RiskCard
              key={r.id}
              risk={r}
              onClick={() => onNavigate(`/risk-center`)}
            />
          ))}
        </div>
      </div>

      {/* 5. DECISION QUEUE & WHAT-IF ACTIONS */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <SectionHeader
            badge="PRESCRIPTIVE ACTIONS"
            title="Autonomous Decision Queue"
            description="Recommended operational remediations with pre-computed ROI."
            className="mb-0"
          />
          <button
            onClick={() => onNavigate('/decision-center')}
            className="text-xs font-mono text-[#FF8A24] hover:text-[#FFB15A] flex items-center gap-1"
          >
            <span>Decision Center</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {decisions.slice(0, 3).map((d) => (
            <DecisionCard
              key={d.id}
              decision={d}
              onSimulate={() => onNavigate('/simulation')}
              onApprove={() => {
                decisionApi.approveDecision(d.id);
                setDecisions((prev) =>
                  prev.map((item) =>
                    item.id === d.id ? { ...item, status: 'approved' } : item
                  )
                );
              }}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default ExecutiveCommandCenterPage;
