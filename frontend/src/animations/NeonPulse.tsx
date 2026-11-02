import React from 'react';
import { motion } from 'framer-motion';

interface NeonPulseProps {
  color?: string;
  size?: number;
  className?: string;
}

export const NeonPulse: React.FC<NeonPulseProps> = ({
  color = '#FF6A00',
  size = 10,
  className = '',
}) => {
  return (
    <span className={`relative inline-flex items-center justify-center ${className}`}>
      <motion.span
        animate={{
          scale: [1, 2.2, 1],
          opacity: [0.75, 0, 0.75],
        }}
        transition={{
          duration: 2.2,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
        className="absolute rounded-full"
        style={{
          width: size,
          height: size,
          backgroundColor: color,
        }}
      />
      <span
        className="relative rounded-full"
        style={{
          width: size,
          height: size,
          backgroundColor: color,
          boxShadow: `0 0 10px ${color}`,
        }}
      />
    </span>
  );
};

export default NeonPulse;
