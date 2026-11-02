import React from 'react';
import { CheckCircle2, ShieldCheck, Zap, UserCheck, Play } from 'lucide-react';
import GlowCard from './GlowCard';
import GlowButton from './GlowButton';
import { DecisionItem } from '@/types';

interface DecisionCardProps {
  decision: DecisionItem;
  onSimulate?: (decision: DecisionItem) => void;
  onApprove?: (decision: DecisionItem) => void;
  className?: string;
}

export const DecisionCard: React.FC<DecisionCardProps> = ({
  decision,
  onSimulate,
  onApprove,
  className = '',
}) => {
  return (
    <GlowCard className={`flex flex-col justify-between ${className}`}>
      <div>
        {/* Header badges */}
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono uppercase tracking-wider font-semibold bg-[#FF6A00]/15 text-[#FF8A24] border border-[#FF6A00]/30">
              {decision.type}
            </span>
            {decision.requiresHumanApproval && (
              <span className="flex items-center gap-1 text-[10px] font-mono text-[#FFB15A] bg-[#FFB15A]/10 border border-[#FFB15A]/30 px-2 py-0.5 rounded-full">
                <UserCheck className="w-3 h-3 text-[#FF6A00]" />
                HUMAN APPROVAL REQUIRED
              </span>
            )}
          </div>
          <span className="text-xs font-mono text-[#A89D92]">
            Confidence: <strong className="text-[#F5F0EA]">{Math.round(decision.confidence * 100)}%</strong>
          </span>
        </div>

        {/* Title & recommendation */}
        <h4 className="mt-3 text-base font-semibold text-[#F5F0EA]">{decision.title}</h4>
        <p className="mt-2 text-xs text-[#A89D92] leading-relaxed">{decision.recommendation}</p>

        {/* Impact specs */}
        <div className="mt-4 p-3 rounded-xl bg-[#080604]/60 border border-[#FF6A00]/12 space-y-2 text-xs">
          <div className="flex items-center gap-2 text-[#FFB15A]">
            <Zap className="w-3.5 h-3.5 text-[#FF6A00] shrink-0" />
            <span>
              <strong>Impact:</strong> {decision.expectedImpact}
            </span>
          </div>
          <div className="flex items-center gap-2 text-[#A89D92]">
            <ShieldCheck className="w-3.5 h-3.5 text-[#FF8A24] shrink-0" />
            <span>
              <strong>Risk Reduction:</strong> {decision.riskReduction}
            </span>
          </div>
        </div>
      </div>

      {/* Action Footer */}
      <div className="mt-5 pt-3 border-t border-[#FF6A00]/12 flex items-center justify-between gap-3">
        <button
          onClick={() => onSimulate?.(decision)}
          className="inline-flex items-center gap-1.5 text-xs font-mono text-[#FF8A24] hover:text-[#FFB15A] transition-colors"
        >
          <Play className="w-3.5 h-3.5 fill-[#FF6A00]" />
          <span>SIMULATE DECISION</span>
        </button>

        <GlowButton
          size="sm"
          variant={decision.status === 'approved' ? 'secondary' : 'primary'}
          onClick={() => onApprove?.(decision)}
          disabled={decision.status === 'approved'}
        >
          {decision.status === 'approved' ? (
            <span className="flex items-center gap-1 text-[#FFB15A]">
              <CheckCircle2 className="w-3.5 h-3.5" /> Approved
            </span>
          ) : (
            'Authorize Decision'
          )}
        </GlowButton>
      </div>
    </GlowCard>
  );
};

export default DecisionCard;
