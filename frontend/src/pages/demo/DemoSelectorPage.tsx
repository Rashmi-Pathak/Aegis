import React, { useState } from 'react';
import {
  Compass,
  ArrowRight,
  ShieldAlert,
  Database,
  Building2,
  FileArchive,
  Sparkles,
} from 'lucide-react';
import GlowButton from '@/components/GlowButton';
import GlowCard from '@/components/GlowCard';
import { DEMO_BUSINESSES } from '@/api/demoApi';
import { DemoBusiness } from '@/types';

interface DemoSelectorPageProps {
  onNavigate: (path: string) => void;
  onSelectBusiness: (businessId: string) => void;
}

export const DemoSelectorPage: React.FC<DemoSelectorPageProps> = ({
  onNavigate,
  onSelectBusiness,
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedBiz, setSelectedBiz] = useState<DemoBusiness>(DEMO_BUSINESSES[0]);

  const categories = [
    { id: 'all', label: 'All 15 Businesses' },
    { id: 'logistics', label: 'Logistics & Supply Chain' },
    { id: 'retail', label: 'Retail & Quick Commerce' },
    { id: 'tech', label: 'B2B Tech & FinTech' },
    { id: 'industrial', label: 'Manufacturing & Energy' },
    { id: 'services', label: 'Healthcare & Hospitality' },
  ];

  const handleLaunchDemo = (business: DemoBusiness) => {
    onSelectBusiness(business.id);
    onNavigate('/command-center');
  };

  return (
    <div className="min-h-screen bg-[#080604] text-[#F5F0EA] p-6 sm:p-12 max-w-7xl mx-auto space-y-10">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-[#FF6A00]/14 pb-8">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#120C08] border border-[#FF6A00]/25 text-xs font-mono text-[#FF8A24] mb-3">
            <Compass className="w-3.5 h-3.5 text-[#FF6A00]" />
            <span>15 SYNTHETIC BUSINESS SIMULATION ENVIRONMENTS</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-[#F5F0EA]">
            Select an Enterprise Twin
          </h1>
          <p className="text-sm text-[#A89D92] mt-2 max-w-2xl leading-relaxed">
            Each environment contains realistic enterprise transaction records with embedded supply shocks, cost anomalies, and strategic decision opportunities.
          </p>
        </div>

        <div className="shrink-0 flex items-center gap-3">
          <GlowButton
            variant="secondary"
            size="sm"
            onClick={() => onNavigate('/')}
          >
            Back to Home
          </GlowButton>
          <GlowButton
            size="sm"
            showArrow
            onClick={() => handleLaunchDemo(selectedBiz)}
          >
            Launch {selectedBiz.name} Twin
          </GlowButton>
        </div>
      </div>

      {/* Grid of 15 Businesses */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {DEMO_BUSINESSES.map((b) => {
          const isSelected = selectedBiz.id === b.id;
          return (
            <div
              key={b.id}
              onClick={() => setSelectedBiz(b)}
              className={`p-6 rounded-2xl bg-[#120C08] border transition-all duration-300 cursor-pointer flex flex-col justify-between group ${
                isSelected
                  ? 'border-[#FF6A00] shadow-[0_0_25px_rgba(255,106,0,0.3)] bg-[#17100B]'
                  : 'border-[#FF6A00]/16 hover:border-[#FF6A00]/50 hover:-translate-y-1'
              }`}
            >
              <div>
                {/* Header */}
                <div className="flex items-center justify-between font-mono text-xs mb-3">
                  <span className="text-[#FF8A24] font-semibold">{b.industry}</span>
                  <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-[#FF6A00]/10 text-[#FFB15A] text-[10px]">
                    <FileArchive className="w-3 h-3" />
                    <span>{b.zipFileName}</span>
                  </div>
                </div>

                <h3 className="text-xl font-bold text-[#F5F0EA] group-hover:text-[#FFB15A] transition-colors">
                  {b.name}
                </h3>
                <p className="text-xs text-[#FFB15A]/80 font-mono mt-1">{b.tagline}</p>
                <p className="text-xs text-[#A89D92] mt-2 leading-relaxed">{b.description}</p>

                {/* Primary Risk Story Callout */}
                <div className="mt-4 p-3 rounded-xl bg-[#080604]/70 border border-[#FF6A00]/15 space-y-1.5 text-xs">
                  <div className="flex items-center gap-1.5 text-[#FF6A00] font-mono text-[10px] font-bold">
                    <ShieldAlert className="w-3 h-3" />
                    <span>ACTIVE THREAT SCENARIO</span>
                  </div>
                  <p className="text-xs text-[#F5F0EA] font-medium leading-snug">
                    {b.primaryRiskStory.trigger}
                  </p>
                  <p className="text-[11px] font-mono text-[#FF8A24]">
                    Exposure: {b.primaryRiskStory.potentialImpact}
                  </p>
                </div>
              </div>

              {/* Metrics & Launch Action */}
              <div className="mt-6 pt-4 border-t border-[#FF6A00]/12 flex items-center justify-between text-xs font-mono">
                <div>
                  <span className="text-[10px] text-[#6F665F] uppercase block">Revenue</span>
                  <span className="font-bold text-[#F5F0EA]">{b.metrics.revenue}</span>
                </div>
                <div>
                  <span className="text-[10px] text-[#6F665F] uppercase block">Health</span>
                  <span className="font-bold text-[#FF8A24]">{b.healthScore} / 100</span>
                </div>
                <div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleLaunchDemo(b);
                    }}
                    className="px-3 py-1.5 rounded-lg bg-[#FF6A00] hover:bg-[#FF8A24] text-white font-sans text-xs font-semibold flex items-center gap-1 shadow-[0_0_12px_rgba(255,106,0,0.3)] transition-all"
                  >
                    <span>Launch</span>
                    <ArrowRight className="w-3 h-3" />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DemoSelectorPage;
