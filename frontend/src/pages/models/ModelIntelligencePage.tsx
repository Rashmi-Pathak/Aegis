import React, { useState, useEffect } from 'react';
import { Cpu, CheckCircle2, RefreshCw, Activity, ShieldCheck } from 'lucide-react';
import SectionHeader from '@/components/SectionHeader';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';
import DataTable from '@/components/DataTable';
import { modelApi } from '@/api/modelApi';
import { ModelIntelligenceItem } from '@/types';

export const ModelIntelligencePage: React.FC<{ onNavigate: (path: string) => void }> = ({
  onNavigate,
}) => {
  const [models, setModels] = useState<ModelIntelligenceItem[]>([]);

  useEffect(() => {
    modelApi.getModels().then(setModels);
  }, []);

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#FF6A00]/14 pb-6">
        <div>
          <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold tracking-wider">
            PYTHON ML REGISTRY & GOVERNANCE
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F0EA] tracking-tight mt-1">
            Model Intelligence & Drift Monitor
          </h1>
          <p className="text-xs text-[#A89D92] mt-1 font-mono">
            Active Python inference workers • LightGBM, Statsmodels, Scikit-learn, NetworkX
          </p>
        </div>

        <div className="flex items-center gap-3">
          <GlowButton
            variant="secondary"
            size="sm"
            onClick={() => {}}
          >
            <RefreshCw className="w-3.5 h-3.5 mr-1" />
            Check Model Drift
          </GlowButton>
        </div>
      </div>

      {/* Model Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {models.map((m) => (
          <GlowCard key={m.id} className="flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between font-mono text-xs mb-3">
                <span className="text-[#FF8A24] font-semibold">{m.version}</span>
                <span className="px-2 py-0.5 rounded-full text-[10px] bg-emerald-500/15 text-emerald-400 font-bold">
                  {m.driftStatus.toUpperCase()}
                </span>
              </div>
              <h4 className="text-sm font-bold text-[#F5F0EA]">{m.name}</h4>
              <p className="text-[11px] text-[#A89D92] font-mono mt-1">
                Type: {m.type.toUpperCase().replace('_', ' ')}
              </p>
            </div>

            <div className="mt-5 pt-3 border-t border-[#FF6A00]/12 space-y-1 font-mono text-xs">
              <div className="flex justify-between">
                <span className="text-[#6F665F]">Accuracy / Score:</span>
                <span className="text-[#FFB15A] font-bold">{m.accuracy}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#6F665F]">Last Trained:</span>
                <span className="text-[#A89D92]">{m.lastTrained}</span>
              </div>
            </div>
          </GlowCard>
        ))}
      </div>

      {/* Detailed ML Performance Table */}
      <div className="space-y-4">
        <SectionHeader
          badge="METRICS BREAKDOWN"
          title="Trained Ensemble Validation Performance"
          description="Evaluation metrics captured across backtest validation folds."
        />

        <DataTable
          columns={[
            { key: 'name', header: 'Model Architecture' },
            {
              key: 'type',
              header: 'ML Task',
              render: (m) => <span className="font-mono text-xs text-[#FF8A24]">{m.type}</span>,
            },
            {
              key: 'accuracy',
              header: 'Validation Accuracy',
              render: (m) => <span className="font-mono text-xs font-bold text-[#F5F0EA]">{m.accuracy}</span>,
            },
            {
              key: 'mae',
              header: 'MAE / F1',
              render: (m) => <span className="font-mono text-xs text-[#FFB15A]">{m.mae || m.f1Score || 'N/A'}</span>,
            },
            {
              key: 'driftStatus',
              header: 'Concept Drift Status',
              render: (m) => (
                <span className="inline-flex items-center gap-1.5 font-mono text-xs text-emerald-400">
                  <CheckCircle2 className="w-3.5 h-3.5" /> Stable
                </span>
              ),
            },
          ]}
          data={models}
          keyExtractor={(m) => m.id}
        />
      </div>
    </div>
  );
};

export default ModelIntelligencePage;
