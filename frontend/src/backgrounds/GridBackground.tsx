import React from 'react';

interface GridBackgroundProps {
  className?: string;
  intensity?: 'subtle' | 'medium' | 'high';
}

export const GridBackground: React.FC<GridBackgroundProps> = ({
  className = '',
  intensity = 'subtle',
}) => {
  const opacity = intensity === 'subtle' ? 'opacity-25' : intensity === 'medium' ? 'opacity-40' : 'opacity-60';

  return (
    <div className={`absolute inset-0 grid-pattern pointer-events-none select-none ${opacity} ${className}`} />
  );
};

export default GridBackground;
