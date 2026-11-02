import React from 'react';
import { motion } from 'framer-motion';

interface FloatingIsometricCoreProps {
  size?: number;
  className?: string;
  glowOpacity?: number;
}

export const FloatingIsometricCore: React.FC<FloatingIsometricCoreProps> = ({
  size = 380,
  className = '',
  glowOpacity = 0.6,
}) => {
  return (
    <div
      className={`relative flex items-center justify-center select-none ${className}`}
      style={{ width: size, height: size }}
    >
      {/* Soft orange radial glow underneath */}
      <div
        className="absolute w-3/4 h-3/4 rounded-full pointer-events-none blur-3xl transition-opacity duration-1000"
        style={{
          background: 'radial-gradient(circle, rgba(255,106,0,0.35) 0%, rgba(255,177,90,0.15) 40%, transparent 70%)',
          opacity: glowOpacity,
        }}
      />

      {/* Floating animated core container */}
      <motion.div
        animate={{
          y: [-8, 8, -8],
          rotateZ: [0, 1.5, 0, -1.5, 0],
        }}
        transition={{
          duration: 7,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
        className="relative z-10 w-full h-full flex items-center justify-center"
      >
        <svg
          viewBox="0 0 400 400"
          className="w-full h-full filter drop-shadow-[0_10px_25px_rgba(255,106,0,0.25)]"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <linearGradient id="facetTop" x1="200" y1="60" x2="200" y2="180" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stopColor="#FFB15A" stopOpacity="0.85" />
              <stop offset="100%" stopColor="#FF6A00" stopOpacity="0.45" />
            </linearGradient>

            <linearGradient id="facetLeft" x1="80" y1="180" x2="200" y2="300" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stopColor="#FF8A24" stopOpacity="0.7" />
              <stop offset="100%" stopColor="#17100B" stopOpacity="0.95" />
            </linearGradient>

            <linearGradient id="facetRight" x1="320" y1="180" x2="200" y2="300" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stopColor="#FF6A00" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#0D0906" stopOpacity="0.95" />
            </linearGradient>

            <linearGradient id="innerCore" x1="150" y1="150" x2="250" y2="250" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stopColor="#FFF2E2" />
              <stop offset="50%" stopColor="#FFB15A" />
              <stop offset="100%" stopColor="#FF6A00" />
            </linearGradient>

            <filter id="coreGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="6" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>

          {/* Isometric outer frame */}
          {/* Top Face */}
          <polygon
            points="200,60 320,130 200,200 80,130"
            fill="url(#facetTop)"
            stroke="#FFB15A"
            strokeWidth="1.5"
            strokeOpacity="0.6"
          />

          {/* Left Face */}
          <polygon
            points="80,130 200,200 200,340 80,270"
            fill="url(#facetLeft)"
            stroke="#FF6A00"
            strokeWidth="1.5"
            strokeOpacity="0.4"
          />

          {/* Right Face */}
          <polygon
            points="200,200 320,130 320,270 200,340"
            fill="url(#facetRight)"
            stroke="#FF8A24"
            strokeWidth="1.5"
            strokeOpacity="0.5"
          />

          {/* Internal floating crystalline octahedron */}
          <g filter="url(#coreGlow)">
            {/* Inner diamond top */}
            <polygon
              points="200,140 240,180 200,220 160,180"
              fill="url(#innerCore)"
              opacity="0.9"
            />
            {/* Inner diamond lower */}
            <polygon
              points="200,220 240,180 200,260 160,180"
              fill="#FF6A00"
              opacity="0.75"
            />
          </g>

          {/* Orbiting geometric rings */}
          <ellipse
            cx="200"
            cy="200"
            rx="140"
            ry="60"
            stroke="#FF6A00"
            strokeWidth="1"
            strokeDasharray="4 8"
            opacity="0.4"
            transform="rotate(-15 200 200)"
          />
          <ellipse
            cx="200"
            cy="200"
            rx="160"
            ry="70"
            stroke="#FFB15A"
            strokeWidth="0.75"
            strokeDasharray="6 12"
            opacity="0.3"
            transform="rotate(25 200 200)"
          />

          {/* Orbiting data nodes */}
          <circle cx="90" cy="180" r="3.5" fill="#FFB15A" filter="url(#coreGlow)" />
          <circle cx="310" cy="220" r="4" fill="#FF8A24" filter="url(#coreGlow)" />
          <circle cx="200" cy="90" r="3" fill="#FFF2E2" filter="url(#coreGlow)" />
          <circle cx="200" cy="310" r="3.5" fill="#FF6A00" filter="url(#coreGlow)" />
        </svg>
      </motion.div>

      {/* Floating lower shadow */}
      <motion.div
        animate={{
          scale: [0.85, 1.1, 0.85],
          opacity: [0.35, 0.6, 0.35],
        }}
        transition={{
          duration: 7,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
        className="absolute bottom-4 w-48 h-8 rounded-full bg-black/70 blur-md pointer-events-none"
      />
    </div>
  );
};

export default FloatingIsometricCore;
