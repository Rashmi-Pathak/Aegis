import React from 'react';
import GlowCard from './GlowCard';

interface HealthScoreCardProps {
  score: number; // 0-100
  title?: string;
  subtitle?: string;
  className?: string;
}

export const HealthScoreCard: React.FC<HealthScoreCardProps> = ({
  score = 82,
  title = 'Enterprise Health Score',
  subtitle = 'Continuous composite assessment across revenue, operational risk, and liquidity',
  className = '',
}) => {
  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <GlowCard className={`flex items-center gap-6 ${className}`}>
      {/* Circular Progress Gauge */}
      <div className="relative w-28 h-28 shrink-0 flex items-center justify-center">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
          {/* Track */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="transparent"
            stroke="rgba(255, 106, 0, 0.12)"
            strokeWidth="8"
          />
          {/* Progress */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="transparent"
            stroke="#FF6A00"
            strokeWidth="8"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center font-mono">
          <span className="text-3xl font-extrabold text-[#F5F0EA] tracking-tighter">{score}</span>
          <span className="text-[10px] text-[#A89D92]">/ 100</span>
        </div>
      </div>

      <div>
        <span className="text-[11px] font-mono uppercase tracking-wider text-[#FF8A24] font-semibold">
          SYSTEM HEALTH
        </span>
        <h3 className="text-lg font-bold text-[#F5F0EA] mt-0.5">{title}</h3>
        <p className="text-xs text-[#A89D92] mt-1.5 leading-relaxed">{subtitle}</p>
        <div className="mt-3 flex items-center gap-4 text-xs font-mono">
          <span className="text-[#FFB15A]">Data Quality: 96%</span>
          <span className="text-[#A89D92]">•</span>
          <span className="text-[#F5F0EA]">Risk Stability: Optimal</span>
        </div>
      </div>
    </GlowCard>
  );
};

export default HealthScoreCard;
