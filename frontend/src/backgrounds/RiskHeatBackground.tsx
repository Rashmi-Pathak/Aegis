import React from 'react';

interface RiskHeatBackgroundProps {
  intensity?: 'low' | 'medium' | 'high' | 'critical';
  className?: string;
}

export const RiskHeatBackground: React.FC<RiskHeatBackgroundProps> = ({
  intensity = 'medium',
  className = '',
}) => {
  const getGlow = () => {
    switch (intensity) {
      case 'critical':
        return 'radial-gradient(circle at 75% 25%, rgba(255,50,0,0.3) 0%, rgba(255,106,0,0.15) 50%, transparent 80%)';
      case 'high':
        return 'radial-gradient(circle at 75% 25%, rgba(255,106,0,0.25) 0%, rgba(255,138,36,0.1) 50%, transparent 80%)';
      case 'medium':
        return 'radial-gradient(circle at 75% 25%, rgba(255,177,90,0.18) 0%, rgba(255,106,0,0.08) 50%, transparent 80%)';
      case 'low':
      default:
        return 'radial-gradient(circle at 75% 25%, rgba(255,177,90,0.08) 0%, transparent 70%)';
    }
  };

  return (
    <div className={`absolute inset-0 pointer-events-none select-none overflow-hidden ${className}`}>
      <div
        className="absolute inset-0 transition-all duration-1000 blur-3xl opacity-70"
        style={{ background: getGlow() }}
      />
      <div className="absolute inset-0 grid-pattern opacity-20" />
    </div>
  );
};

export default RiskHeatBackground;
