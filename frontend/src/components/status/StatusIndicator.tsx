import React from 'react';
import NeonPulse from '@/animations/NeonPulse';

interface StatusIndicatorProps {
  status?: 'operational' | 'degraded' | 'critical' | 'processing';
  label?: string;
  className?: string;
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({
  status = 'operational',
  label,
  className = '',
}) => {
  const getColor = () => {
    switch (status) {
      case 'operational':
        return '#FF6A00';
      case 'degraded':
        return '#FFB15A';
      case 'critical':
        return '#FF4500';
      case 'processing':
        return '#FF8A24';
    }
  };

  const getLabel = () => {
    if (label) return label;
    switch (status) {
      case 'operational':
        return 'SYSTEM OPERATIONAL';
      case 'degraded':
        return 'ELEVATED RISK MONITORING';
      case 'critical':
        return 'ACTIVE INCIDENT IN PROGRESS';
      case 'processing':
        return 'DATA ENGINE PROCESSING';
    }
  };

  return (
    <div className={`inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-[#120C08] border border-[#FF6A00]/25 text-[11px] font-mono text-[#F5F0EA] ${className}`}>
      <NeonPulse color={getColor()} size={7} />
      <span className="tracking-wider">{getLabel()}</span>
    </div>
  );
};

export default StatusIndicator;
