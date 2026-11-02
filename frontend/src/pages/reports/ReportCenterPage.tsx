import React, { useState, useEffect } from 'react';
import { FileText, Download, Calendar, Eye, FileSpreadsheet } from 'lucide-react';
import SectionHeader from '@/components/SectionHeader';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';
import { reportApi } from '@/api/reportApi';
import { ReportItem } from '@/types';

export const ReportCenterPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const [reports, setReports] = useState<ReportItem[]>([]);

  useEffect(() => {
    reportApi.getReports().then(setReports);
  }, []);

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#FF6A00]/14 pb-6">
        <div>
          <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold tracking-wider">
            EXECUTIVE AUDIT & BRIEFINGS
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F0EA] tracking-tight mt-1">
            Executive Report Center
          </h1>
          <p className="text-xs text-[#A89D92] mt-1 font-mono">
            Automated intelligence briefs synthesized for Board of Directors and C-Suite review.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <GlowButton size="sm" onClick={() => {}}>
            Generate Instant Audit Brief
          </GlowButton>
        </div>
      </div>

      {/* Report Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {reports.map((rep) => (
          <GlowCard key={rep.id} className="flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between text-xs font-mono mb-2">
                <span className="text-[#FF8A24] uppercase font-bold">{rep.category} BRIEF</span>
                <span className="text-[#6F665F]">{rep.generatedAt}</span>
              </div>
              <h3 className="text-base font-bold text-[#F5F0EA]">{rep.title}</h3>
              <p className="text-xs text-[#A89D92] mt-2 leading-relaxed">{rep.summary}</p>
            </div>

            <div className="mt-6 pt-4 border-t border-[#FF6A00]/12 flex items-center justify-between">
              <span className="text-[11px] font-mono text-[#FFB15A] flex items-center gap-1.5">
                <Calendar className="w-3.5 h-3.5 text-[#FF6A00]" />
                {rep.frequency.toUpperCase()} CADENCE
              </span>

              <div className="flex items-center gap-2">
                <GlowButton size="sm" variant="secondary" onClick={() => {}}>
                  <Download className="w-3.5 h-3.5 mr-1" /> Export
                </GlowButton>
                <GlowButton size="sm" onClick={() => onNavigate(`/reports/${rep.id}`)}>
                  <Eye className="w-3.5 h-3.5 mr-1" /> View Brief
                </GlowButton>
              </div>
            </div>
          </GlowCard>
        ))}
      </div>
    </div>
  );
};

export default ReportCenterPage;
