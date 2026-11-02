import React from 'react';
import { Activity, Clock } from 'lucide-react';
import GlowCard from './GlowCard';
import { AnomalyItem } from '@/types';

interface AnomalyCardProps {
  anomaly: AnomalyItem;
  className?: string;
}

export const AnomalyCard: React.FC<AnomalyCardProps> = ({ anomaly, className = '' }) => {
  return (
    <GlowCard className={`flex flex-col justify-between ${className}`}>
      <div>
        <div className="flex items-center justify-between text-xs font-mono">
          <div className="flex items-center gap-1.5 text-[#FF6A00]">
            <Activity className="w-3.5 h-3.5 animate-pulse" />
            <span className="font-semibold uppercase tracking-wider">{anomaly.severity} OUTLIER</span>
          </div>
          <div className="flex items-center gap-1 text-[#6F665F]">
            <Clock className="w-3 h-3" />
            <span>{anomaly.detectedAt}</span>
          </div>
        </div>

        <h4 className="mt-2.5 text-sm font-semibold text-[#F5F0EA]">{anomaly.metric}</h4>
        <p className="mt-1.5 text-xs text-[#A89D92] leading-relaxed">{anomaly.explanation}</p>
      </div>

      <div className="mt-4 pt-3 border-t border-[#FF6A00]/10 grid grid-cols-2 gap-2 text-xs font-mono">
        <div className="p-2 rounded-lg bg-[#080604]/50 border border-[#FF6A00]/10">
          <span className="text-[10px] text-[#6F665F] uppercase block">Expected Baseline</span>
          <span className="text-[#A89D92] font-medium">{anomaly.expectedValue}</span>
        </div>
        <div className="p-2 rounded-lg bg-[#FF6A00]/10 border border-[#FF6A00]/25">
          <span className="text-[10px] text-[#FFB15A] uppercase block">Observed Anomaly</span>
          <span className="text-[#FF8A24] font-bold">{anomaly.actualValue}</span>
        </div>
      </div>
    </GlowCard>
  );
};

export default AnomalyCard;
