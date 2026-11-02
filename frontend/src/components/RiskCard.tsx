import React from 'react';
import { ShieldAlert, ArrowUpRight } from 'lucide-react';
import GlowCard from './GlowCard';
import { RiskItem } from '@/types';

interface RiskCardProps {
  risk: RiskItem;
  onClick?: () => void;
  className?: string;
}

export const RiskCard: React.FC<RiskCardProps> = ({ risk, onClick, className = '' }) => {
  const getSeverityStyle = (severity: RiskItem['severity']) => {
    switch (severity) {
      case 'critical':
        return {
          badge: 'bg-[#FF4500]/20 text-[#FF6A00] border-[#FF6A00]/50 shadow-[0_0_12px_rgba(255,106,0,0.3)]',
          dot: 'bg-[#FF4500] shadow-[0_0_8px_#FF4500]',
          border: 'border-[#FF6A00]/40',
        };
      case 'high':
        return {
          badge: 'bg-[#FF6A00]/15 text-[#FF8A24] border-[#FF8A24]/40',
          dot: 'bg-[#FF8A24]',
          border: 'border-[#FF8A24]/30',
        };
      case 'medium':
        return {
          badge: 'bg-[#FFB15A]/10 text-[#FFB15A] border-[#FFB15A]/30',
          dot: 'bg-[#FFB15A]',
          border: 'border-[#FFB15A]/20',
        };
      case 'low':
      default:
        return {
          badge: 'bg-[#6F665F]/15 text-[#A89D92] border-[#6F665F]/30',
          dot: 'bg-[#A89D92]',
          border: 'border-[#FF6A00]/10',
        };
    }
  };

  const style = getSeverityStyle(risk.severity);

  return (
    <GlowCard
      onClick={onClick}
      className={`group flex flex-col justify-between hover:border-[#FF6A00]/60 ${style.border} ${className}`}
    >
      <div>
        {/* Header */}
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${style.dot}`} />
            <span
              className={`px-2.5 py-0.5 rounded-full text-[10px] uppercase font-mono tracking-wider font-semibold border ${style.badge}`}
            >
              {risk.severity} RISK
            </span>
          </div>
          <span className="text-xs font-mono text-[#A89D92]">{risk.detectedAt}</span>
        </div>

        {/* Title */}
        <h4 className="mt-3 text-base font-semibold text-[#F5F0EA] group-hover:text-[#FFB15A] transition-colors flex items-center justify-between">
          <span>{risk.title}</span>
          <ArrowUpRight className="w-4 h-4 text-[#A89D92] group-hover:text-[#FF6A00] group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-all" />
        </h4>

        {/* Primary drivers */}
        {risk.primaryDrivers && risk.primaryDrivers.length > 0 && (
          <p className="mt-2 text-xs text-[#A89D92] line-clamp-2">
            <span className="text-[#6F665F]">Trigger:</span> {risk.primaryDrivers.join(' • ')}
          </p>
        )}
      </div>

      {/* Exposure & Score Footer */}
      <div className="mt-5 pt-3.5 border-t border-[#FF6A00]/12 grid grid-cols-3 gap-2 text-center">
        <div className="text-left">
          <p className="text-[10px] text-[#6F665F] uppercase tracking-wider font-medium">Risk Score</p>
          <p className="text-sm font-mono font-bold text-[#FF8A24]">{risk.score} / 100</p>
        </div>
        <div>
          <p className="text-[10px] text-[#6F665F] uppercase tracking-wider font-medium">Probability</p>
          <p className="text-sm font-mono text-[#F5F0EA]">{Math.round(risk.probability * 100)}%</p>
        </div>
        <div className="text-right">
          <p className="text-[10px] text-[#6F665F] uppercase tracking-wider font-medium">Exposure</p>
          <p className="text-sm font-mono font-bold text-[#FFB15A]">{risk.exposureAmount}</p>
        </div>
      </div>
    </GlowCard>
  );
};

export default RiskCard;
