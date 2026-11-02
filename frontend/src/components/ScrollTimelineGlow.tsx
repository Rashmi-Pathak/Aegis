import React from 'react';
import { motion, useScroll, useSpring, useTransform } from 'framer-motion';

interface ScrollTimelineGlowProps {
  className?: string;
  containerRef?: React.RefObject<HTMLElement>;
}

export const ScrollTimelineGlow: React.FC<ScrollTimelineGlowProps> = ({
  className = '',
  containerRef,
}) => {
  // Track scroll through the sections container
  const { scrollYProgress } = useScroll(
    containerRef
      ? {
          target: containerRef,
          offset: ['start 45%', 'end 85%'],
        }
      : {
          offset: ['start start', 'end end'],
        }
  );

  const smoothProgress = useSpring(scrollYProgress, {
    stiffness: 90,
    damping: 24,
    restDelta: 0.001,
  });

  // Scale of the glowing line height (0% to 100%)
  const lineHeight = useTransform(smoothProgress, [0, 1], ['0%', '100%']);
  const tipOpacity = useTransform(smoothProgress, [0, 0.015, 0.98, 1], [0, 1, 1, 0.6]);

  return (
    <div
      className={`absolute top-12 bottom-12 left-1/2 -translate-x-1/2 pointer-events-none z-0 ${className}`}
      style={{ width: '48px' }}
    >
      {/* 1. Inactive background track */}
      <div className="absolute top-0 bottom-0 left-1/2 -translate-x-1/2 w-[2px] bg-gradient-to-b from-[#FF6A00]/25 via-[#FF6A00]/10 to-[#FF6A00]/5" />

      {/* 2. Active Glowing Neon Line extending downward as user scrolls */}
      <motion.div
        className="absolute top-0 left-1/2 -translate-x-1/2 w-[3px] origin-top"
        style={{
          height: lineHeight,
          background: 'linear-gradient(to bottom, #FF6A00 0%, #FF8A24 40%, #FFB15A 80%, #FFF4E5 100%)',
          boxShadow: '0 0 16px #FF6A00, 0 0 35px #FF8A24, 0 0 60px rgba(255,106,0,0.7)',
        }}
      />

      {/* 3. Radiant ambient glow pool traveling with the line tip */}
      <motion.div
        className="absolute left-1/2 -translate-x-1/2 w-[220px] h-[220px] rounded-full pointer-events-none blur-[60px]"
        style={{
          top: lineHeight,
          opacity: tipOpacity,
          transform: 'translate(-50%, -50%)',
          background:
            'radial-gradient(circle, rgba(255,106,0,0.95) 0%, rgba(255,177,90,0.5) 45%, transparent 75%)',
        }}
      />

      {/* 4. Active Leading Beacon Orb at the tip of the line */}
      <motion.div
        className="absolute left-1/2 -translate-x-1/2 w-5 h-5 rounded-full flex items-center justify-center z-10"
        style={{
          top: lineHeight,
          opacity: tipOpacity,
          transform: 'translate(-50%, -50%)',
        }}
      >
        {/* Pulsing ring wave */}
        <div className="absolute inset-[-4px] rounded-full bg-[#FF6A00] animate-ping opacity-75" />
        {/* Outer neon halo */}
        <div className="absolute inset-0 rounded-full bg-gradient-to-tr from-[#FF6A00] to-[#FFB15A] opacity-90 shadow-[0_0_20px_#FF6A00]" />
        {/* Glowing white core */}
        <div className="relative w-2.5 h-2.5 rounded-full bg-white shadow-[0_0_12px_#FFF]" />
      </motion.div>
    </div>
  );
};

export default ScrollTimelineGlow;
