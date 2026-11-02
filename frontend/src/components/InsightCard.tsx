import React from 'react';
import { Sparkles, ArrowRight } from 'lucide-react';
import GlowCard from './GlowCard';

interface InsightCardProps {
  title: string;
  category?: string;
  description: string;
  metricHighlight?: string;
  actionText?: string;
  onAction?: () => void;
  className?: string;
}

export const InsightCard: React.FC<InsightCardProps> = ({
  title,
  category = 'AI INTELLIGENCE',
  description,
  metricHighlight,
  actionText = 'Investigate Signal',
  onAction,
  className = '',
}) => {
  return (
    <GlowCard className={`flex flex-col justify-between ${className}`}>
      <div>
        <div className="flex items-center gap-1.5 text-[#FF8A24] text-xs font-mono font-semibold">
          <Sparkles className="w-3.5 h-3.5 text-[#FF6A00]" />
          <span>{category}</span>
        </div>
        <h4 className="mt-2 text-base font-semibold text-[#F5F0EA]">{title}</h4>
        <p className="mt-1.5 text-xs text-[#A89D92] leading-relaxed">{description}</p>
        {metricHighlight && (
          <div className="mt-3 p-2.5 rounded-lg bg-[#080604]/50 border border-[#FF6A00]/15 text-xs font-mono text-[#FFB15A]">
            {metricHighlight}
          </div>
        )}
      </div>

      <div className="mt-4 pt-3 border-t border-[#FF6A00]/10 flex items-center justify-end">
        <button
          onClick={onAction}
          className="inline-flex items-center gap-1.5 text-xs font-mono text-[#FF8A24] hover:text-[#FFB15A] transition-colors"
        >
          <span>{actionText}</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </GlowCard>
  );
};

export default InsightCard;
