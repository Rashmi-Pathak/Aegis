import React, { useState, useEffect } from 'react';
import { Sliders, UserCheck, CheckCircle2, XCircle, ArrowRight, Play } from 'lucide-react';
import SectionHeader from '@/components/SectionHeader';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';
import DecisionCard from '@/components/DecisionCard';
import { decisionApi } from '@/api/decisionApi';
import { DecisionItem } from '@/types';

export const DecisionCenterPage: React.FC<{ onNavigate: (path: string) => void }> = ({
  onNavigate,
}) => {
  const [decisions, setDecisions] = useState<DecisionItem[]>([]);
  const [activeTab, setActiveTab] = useState<'all' | 'pending' | 'approved' | 'simulated'>('all');

  useEffect(() => {
    decisionApi.getDecisions().then(setDecisions);
  }, []);

  const handleApprove = async (d: DecisionItem) => {
    await decisionApi.approveDecision(d.id);
    setDecisions((prev) =>
      prev.map((item) => (item.id === d.id ? { ...item, status: 'approved' } : item))
    );
  };

  const filtered = activeTab === 'all'
    ? decisions
    : decisions.filter((d) => d.status === activeTab);

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#FF6A00]/14 pb-6">
        <div>
          <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold tracking-wider">
            PRESCRIPTIVE GOVERNANCE & ACTION
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F0EA] tracking-tight mt-1">
            Autonomous Decision Center
          </h1>
          <p className="text-xs text-[#A89D92] mt-1 font-mono">
            Ranked prescriptive remediations • Human-in-the-loop executive authorization required
          </p>
        </div>

        <div className="flex items-center gap-3">
          <GlowButton
            variant="secondary"
            size="sm"
            onClick={() => onNavigate('/simulation')}
          >
            <Play className="w-3.5 h-3.5 mr-1" />
            Simulate Custom Scenario
          </GlowButton>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap items-center gap-2 border-b border-[#FF6A00]/12 pb-3 font-mono text-xs">
        {[
          { id: 'all', label: `All Remediations (${decisions.length})` },
          { id: 'pending', label: `Pending Executive Approval (${decisions.filter((d) => d.status === 'pending').length})` },
          { id: 'approved', label: `Authorized & Queued (${decisions.filter((d) => d.status === 'approved').length})` },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-3.5 py-1.5 rounded-xl transition-colors ${
              activeTab === tab.id
                ? 'bg-[#FF6A00] text-white font-bold'
                : 'text-[#A89D92] hover:text-[#F5F0EA] bg-[#120C08]'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Decision Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map((d) => (
          <DecisionCard
            key={d.id}
            decision={d}
            onSimulate={() => onNavigate('/simulation')}
            onApprove={handleApprove}
          />
        ))}
      </div>
    </div>
  );
};

export default DecisionCenterPage;
