import React from 'react';
import { motion } from 'framer-motion';

interface GlowHoverProps {
  children: React.ReactNode;
  className?: string;
  glowColor?: string;
}

export const GlowHover: React.FC<GlowHoverProps> = ({
  children,
  className = '',
  glowColor = 'rgba(255, 106, 0, 0.3)',
}) => {
  return (
    <motion.div
      whileHover={{
        y: -3,
        boxShadow: `0 0 25px ${glowColor}`,
      }}
      transition={{ duration: 0.25, ease: 'easeOut' }}
      className={`transition-all duration-300 ${className}`}
    >
      {children}
    </motion.div>
  );
};

export default GlowHover;
