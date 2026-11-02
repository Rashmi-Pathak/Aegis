import React from 'react';
import { TrendingUp, TrendingDown, Minus, AlertTriangle } from 'lucide-react';
import GlowCard from './GlowCard';

interface MetricCardProps {
  title: string;
  value: string | number;
  changePercent?: number;
  trend?: 'up' | 'down' | 'neutral';
  timeframe?: string;
  isAnomaly?: boolean;
  prefix?: string;
  suffix?: string;
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  changePercent,
  trend = 'neutral',
  timeframe = 'vs last period',
  isAnomaly = false,
  prefix = '',
  suffix = '',
  className = '',
}) => {
  return (
    <GlowCard className={`relative flex flex-col justify-between ${className}`}>
      {isAnomaly && (
        <div className="absolute top-4 right-4 flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-[#FF6A00]/15 border border-[#FF6A00]/40 text-[#FFB15A] text-[10px] font-mono font-medium">
          <AlertTriangle className="w-3 h-3 text-[#FF6A00]" />
          <span>DEVIATION</span>
        </div>
      )}

      <div>
        <p className="text-xs uppercase tracking-wider text-[#A89D92] font-medium">{title}</p>
        <div className="mt-2 flex items-baseline gap-1">
          {prefix && <span className="text-[#A89D92] text-xl font-mono">{prefix}</span>}
          <h3 className="text-3xl font-bold font-mono tracking-tight text-[#F5F0EA]">{value}</h3>
          {suffix && <span className="text-[#A89D92] text-sm font-mono">{suffix}</span>}
        </div>
      </div>

      {changePercent !== undefined && (
        <div className="mt-4 pt-3 border-t border-[#FF6A00]/10 flex items-center justify-between text-xs">
          <div
            className={`flex items-center gap-1 font-mono font-medium ${
              changePercent > 0
                ? 'text-[#FF8A24]'
                : changePercent < 0
                ? 'text-amber-500'
                : 'text-[#A89D92]'
            }`}
          >
            {trend === 'up' && <TrendingUp className="w-3.5 h-3.5" />}
            {trend === 'down' && <TrendingDown className="w-3.5 h-3.5" />}
            {trend === 'neutral' && <Minus className="w-3.5 h-3.5" />}
            <span>
              {changePercent > 0 ? '+' : ''}
              {changePercent}%
            </span>
          </div>
          <span className="text-[#6F665F] text-[11px]">{timeframe}</span>
        </div>
      )}
    </GlowCard>
  );
};

export default MetricCard;
