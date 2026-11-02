import React from 'react';
import { Database, RefreshCw, AlertCircle } from 'lucide-react';
import GlowButton from '@/components/GlowButton';

interface EmptyStateProps {
  title?: string;
  description?: string;
  actionText?: string;
  onAction?: () => void;
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'No Data Available',
  description = 'No signals or intelligence records matching the selected parameters were detected.',
  actionText,
  onAction,
  className = '',
}) => {
  return (
    <div className={`p-12 text-center rounded-2xl bg-[#120C08]/50 border border-[#FF6A00]/14 backdrop-blur-md flex flex-col items-center justify-center ${className}`}>
      <div className="w-14 h-14 rounded-2xl bg-[#FF6A00]/10 border border-[#FF6A00]/25 flex items-center justify-center text-[#FF6A00] mb-4">
        <Database className="w-7 h-7" />
      </div>
      <h3 className="text-base font-bold text-[#F5F0EA]">{title}</h3>
      <p className="text-xs text-[#A89D92] mt-1 max-w-md">{description}</p>
      {actionText && onAction && (
        <div className="mt-5">
          <GlowButton size="sm" onClick={onAction}>
            {actionText}
          </GlowButton>
        </div>
      )}
    </div>
  );
};

export const LoadingState: React.FC<{ message?: string; className?: string }> = ({
  message = 'Synthesizing business telemetry...',
  className = '',
}) => {
  return (
    <div className={`p-12 text-center rounded-2xl bg-[#120C08]/40 border border-[#FF6A00]/10 flex flex-col items-center justify-center ${className}`}>
      <RefreshCw className="w-8 h-8 text-[#FF6A00] animate-spin mb-3" />
      <p className="text-xs font-mono text-[#A89D92]">{message}</p>
    </div>
  );
};

export const ErrorState: React.FC<{ error?: string; onRetry?: () => void; className?: string }> = ({
  error = 'Intelligence service unavailable',
  onRetry,
  className = '',
}) => {
  return (
    <div className={`p-8 text-center rounded-2xl bg-[#FF4500]/10 border border-[#FF4500]/30 flex flex-col items-center justify-center ${className}`}>
      <AlertCircle className="w-8 h-8 text-[#FF6A00] mb-2" />
      <h4 className="text-sm font-bold text-[#F5F0EA]">{error}</h4>
      {onRetry && (
        <div className="mt-4">
          <GlowButton size="sm" variant="secondary" onClick={onRetry}>
            Retry Request
          </GlowButton>
        </div>
      )}
    </div>
  );
};

export default EmptyState;
