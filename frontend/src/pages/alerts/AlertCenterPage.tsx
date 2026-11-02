import React, { useState, useEffect } from 'react';
import { Bell, AlertTriangle, ArrowRight, CheckCircle2, SearchCode } from 'lucide-react';
import SectionHeader from '@/components/SectionHeader';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';
import { alertApi } from '@/api/alertApi';
import { AlertItem } from '@/types';

export const AlertCenterPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const [alerts, setAlerts] = useState<AlertItem[]>([]);

  useEffect(() => {
    alertApi.getAlerts().then(setAlerts);
  }, []);

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#FF6A00]/14 pb-6">
        <div>
          <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold tracking-wider">
            REAL-TIME TELEMETRY ALERTS
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F0EA] tracking-tight mt-1">
            System Alert Center
          </h1>
          <p className="text-xs text-[#A89D92] mt-1 font-mono">
            Autonomous anomaly alerts triggered by isolation forest deviations and threshold breaches.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <GlowButton
            variant="secondary"
            size="sm"
            onClick={() => onNavigate('/anomalies')}
          >
            Anomaly Timeline Stream
          </GlowButton>
        </div>
      </div>

      {/* Alert Feed */}
      <div className="space-y-4">
        {alerts.map((alt) => (
          <div
            key={alt.id}
            onClick={() => onNavigate('/investigation')}
            className="p-5 rounded-2xl bg-[#120C08] border border-[#FF6A00]/18 hover:border-[#FF6A00]/50 cursor-pointer transition-all duration-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 group"
          >
            <div className="flex items-start gap-4">
              <div
                className={`p-2.5 rounded-xl mt-0.5 ${
                  alt.severity === 'critical'
                    ? 'bg-[#FF4500]/15 text-[#FF4500] border border-[#FF4500]/30 shadow-[0_0_12px_rgba(255,69,0,0.3)]'
                    : 'bg-[#FF6A00]/15 text-[#FF8A24] border border-[#FF6A00]/30'
                }`}
              >
                <AlertTriangle className="w-5 h-5" />
              </div>
              <div className="space-y-1">
                <div className="flex items-center gap-3 text-xs font-mono">
                  <span className="font-bold text-[#FF8A24] uppercase">{alt.severity} PRIORITY</span>
                  <span className="text-[#6F665F]">•</span>
                  <span className="text-[#6F665F]">{alt.source}</span>
                  <span className="text-[#6F665F]">•</span>
                  <span className="text-[#A89D92]">{alt.timestamp}</span>
                </div>
                <h4 className="text-base font-semibold text-[#F5F0EA] group-hover:text-[#FFB15A] transition-colors">
                  {alt.message}
                </h4>
                <p className="text-xs text-[#A89D92] font-mono">
                  Affected Target: <strong className="text-[#FFB15A]">{alt.affectedMetric}</strong>
                </p>
              </div>
            </div>

            <div className="shrink-0 flex items-center gap-2 self-end sm:self-center font-mono text-xs text-[#FF8A24]">
              <span>Investigate Signal</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AlertCenterPage;
