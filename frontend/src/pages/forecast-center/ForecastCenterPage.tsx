import React, { useState, useEffect } from 'react';
import { TrendingUp, RefreshCw, Layers, ShieldCheck, Zap } from 'lucide-react';
import SectionHeader from '@/components/SectionHeader';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';
import ForecastCard from '@/components/ForecastCard';
import RevenueForecastChart from '@/charts/RevenueForecastChart';
import ForecastConfidenceChart from '@/charts/ForecastConfidenceChart';
import { forecastApi } from '@/api/forecastApi';
import { ForecastItem } from '@/types';

export const ForecastCenterPage: React.FC<{ onNavigate: (path: string) => void }> = ({
  onNavigate,
}) => {
  const [forecasts, setForecasts] = useState<ForecastItem[]>([]);
  const [selectedHorizon, setSelectedHorizon] = useState('90');

  useEffect(() => {
    forecastApi.getForecasts().then(setForecasts);
  }, []);

  const sections = ['Revenue', 'Demand & Freight', 'Energy / Fuel Cost', 'Inventory Capacity', 'Cash Flow', 'Customer Retention'];

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#FF6A00]/14 pb-6">
        <div>
          <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold tracking-wider">
            MULTI-HORIZON PREDICTIVE ENGINES
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F0EA] tracking-tight mt-1">
            Enterprise Forecast Center
          </h1>
          <p className="text-xs text-[#A89D92] mt-1 font-mono">
            Ensemble modeling: LightGBM + Statsmodels SARIMAX • 95% Confidence Bounds
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center bg-[#120C08] border border-[#FF6A00]/20 rounded-xl p-1 text-xs font-mono">
            {['30', '60', '90', '180'].map((h) => (
              <button
                key={h}
                onClick={() => setSelectedHorizon(h)}
                className={`px-3 py-1 rounded-lg transition-colors ${
                  selectedHorizon === h
                    ? 'bg-[#FF6A00] text-white font-bold'
                    : 'text-[#A89D92] hover:text-[#F5F0EA]'
                }`}
              >
                {h}D
              </button>
            ))}
          </div>

          <GlowButton
            variant="secondary"
            size="sm"
            onClick={() => onNavigate('/simulation')}
          >
            Run Scenario Stress Test
          </GlowButton>
        </div>
      </div>

      {/* Primary Forecast Showcase Banner */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <GlowCard className="lg:col-span-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-[#F5F0EA]">Gross Operating Revenue Projection</h3>
              <p className="text-xs text-[#A89D92] font-mono">
                {selectedHorizon}-Day Horizon • Historical Baseline vs Machine Ensemble
              </p>
            </div>
            <span className="text-xs font-mono font-bold text-[#FF8A24] bg-[#FF6A00]/15 px-3 py-1 rounded-full border border-[#FF6A00]/30">
              94.2% Predictive Accuracy
            </span>
          </div>
          <RevenueForecastChart height={300} />
        </GlowCard>

        {/* Model Accuracy & Confidence Degradation */}
        <GlowCard className="lg:col-span-4 flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-[#F5F0EA] mb-1">Horizon Confidence Envelope</h3>
            <p className="text-xs text-[#A89D92] font-mono mb-4">
              Degradation across extended multi-week horizon
            </p>
            <ForecastConfidenceChart height={200} />
          </div>

          <div className="pt-4 border-t border-[#FF6A00]/10 mt-4 space-y-2 text-xs font-mono">
            <div className="flex justify-between">
              <span className="text-[#6F665F]">Mean Absolute Error (MAE):</span>
              <span className="text-[#FFB15A] font-bold">0.28</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#6F665F]">Root Mean Squared Error (RMSE):</span>
              <span className="text-[#FF8A24] font-bold">0.41</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#6F665F]">Model Drift Status:</span>
              <span className="text-emerald-400 font-bold">STABLE (0.02σ)</span>
            </div>
          </div>
        </GlowCard>
      </div>

      {/* Modular Forecast Cards Across Domains */}
      <div className="space-y-4">
        <SectionHeader
          badge="DOMAIN OUTLOOKS"
          title="Predictive Streams by Business Unit"
          description="Independent forecast ensembles trained on domain telemetry."
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {forecasts.map((fc) => (
            <ForecastCard key={fc.id} forecast={fc} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default ForecastCenterPage;
