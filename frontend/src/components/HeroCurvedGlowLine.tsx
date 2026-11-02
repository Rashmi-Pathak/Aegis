import React from 'react';

interface HeroCurvedGlowLineProps {
  className?: string;
  glowOpacity?: number;
  height?: number;
}

export const HeroCurvedGlowLine: React.FC<HeroCurvedGlowLineProps> = ({
  className = '',
  glowOpacity = 1,
  height = 320,
}) => {
  return (
    <div className={`relative w-full overflow-hidden select-none pointer-events-none ${className}`}>
      {/* 1. Gigantic diffuse ambient orange glow pool behind the arc */}
      <div
        className="absolute left-1/2 -translate-x-1/2 top-0 w-[1500px] h-[650px] blur-[150px] pointer-events-none"
        style={{
          opacity: 0.85 * glowOpacity,
          background:
            'radial-gradient(ellipse at center, rgba(255,106,0,0.85) 0%, rgba(255,138,36,0.5) 30%, rgba(184,66,0,0.2) 65%, transparent 85%)',
        }}
      />

      {/* 2. Secondary hot orange center bloom */}
      <div
        className="absolute left-1/2 -translate-x-1/2 top-6 w-[1000px] h-[340px] blur-[80px] pointer-events-none"
        style={{
          opacity: 0.95 * glowOpacity,
          background:
            'radial-gradient(ellipse at center, #FF8A24 0%, rgba(255,106,0,0.75) 45%, transparent 85%)',
        }}
      />

      {/* 3. Curved Semicircular Glowing Razor Horizon Arc (SVG) */}
      <div className="relative w-full flex items-start justify-center" style={{ height: `${height}px` }}>
        <svg
          viewBox="0 0 1440 320"
          className="w-full h-full preserve-3d"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            {/* Horizontal gradient along the arc: hot center, fading to transparent edges */}
            <linearGradient id="horizonGlowLine" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#FF6A00" stopOpacity="0" />
              <stop offset="12%" stopColor="#FF6A00" stopOpacity="0.45" />
              <stop offset="35%" stopColor="#FF8A24" stopOpacity="0.95" />
              <stop offset="50%" stopColor="#FFF4E5" stopOpacity="1" />
              <stop offset="65%" stopColor="#FF8A24" stopOpacity="0.95" />
              <stop offset="88%" stopColor="#FF6A00" stopOpacity="0.45" />
              <stop offset="100%" stopColor="#FF6A00" stopOpacity="0" />
            </linearGradient>

            {/* Radiant glowing underfill that spills light downward into the section */}
            <linearGradient id="horizonAreaFill" x1="50%" y1="0%" x2="50%" y2="100%">
              <stop offset="0%" stopColor="#FF6A00" stopOpacity="0.8" />
              <stop offset="25%" stopColor="#FF8A24" stopOpacity="0.45" />
              <stop offset="60%" stopColor="#B84200" stopOpacity="0.18" />
              <stop offset="100%" stopColor="#080604" stopOpacity="0" />
            </linearGradient>

            <filter id="arcBloom" x="-25%" y="-50%" width="150%" height="220%">
              <feGaussianBlur stdDeviation="10" result="blur1" />
              <feGaussianBlur stdDeviation="28" result="blur2" />
              <feMerge>
                <feMergeNode in="blur2" />
                <feMergeNode in="blur1" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {/* Glowing underfill gradient shaping the horizon down into the cards */}
          <path
            d="M -100 320 C 350 45, 1090 45, 1540 320 L 1540 320 L -100 320 Z"
            fill="url(#horizonAreaFill)"
          />

          {/* Wide diffuse glow bloom */}
          <path
            d="M -50 300 C 400 45, 1040 45, 1490 300"
            stroke="#FF6A00"
            strokeWidth="18"
            opacity="0.85"
            filter="url(#arcBloom)"
          />

          {/* Medium bright core neon arc */}
          <path
            d="M -50 300 C 400 45, 1040 45, 1490 300"
            stroke="#FF8A24"
            strokeWidth="6"
            opacity="0.95"
            filter="url(#arcBloom)"
          />

          {/* Crisp, intense razor white/amber horizon edge */}
          <path
            d="M -50 300 C 400 45, 1040 45, 1490 300"
            stroke="url(#horizonGlowLine)"
            strokeWidth="2.8"
          />
        </svg>
      </div>
    </div>
  );
};

export default HeroCurvedGlowLine;
