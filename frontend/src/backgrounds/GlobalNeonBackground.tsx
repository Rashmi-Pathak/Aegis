import React from 'react';

interface GlobalNeonBackgroundProps {
  children?: React.ReactNode;
  className?: string;
}

export const GlobalNeonBackground: React.FC<GlobalNeonBackgroundProps> = ({
  children,
  className = '',
}) => {
  return (
    <div className={`relative min-h-screen w-full bg-[#050302] overflow-hidden flex flex-col ${className}`}>
      {/* 1. Top Radiant Orange Light Pool */}
      <div
        className="fixed top-[-10%] left-1/2 -translate-x-1/2 w-[1200px] h-[750px] rounded-full pointer-events-none blur-[160px] opacity-45"
        style={{
          background: 'radial-gradient(circle, rgba(255,106,0,0.6) 0%, rgba(217,91,0,0.3) 45%, rgba(148,56,0,0.1) 70%, transparent 85%)',
        }}
      />

      {/* 2. Middle Section Radiant Orange Glow */}
      <div
        className="fixed top-[45%] left-[-15%] w-[850px] h-[850px] rounded-full pointer-events-none blur-[180px] opacity-35"
        style={{
          background: 'radial-gradient(circle, rgba(255,138,36,0.5) 0%, rgba(255,106,0,0.2) 50%, transparent 75%)',
        }}
      />

      {/* 3. Right Mid-Page Warm Atmosphere */}
      <div
        className="fixed top-[65%] right-[-15%] w-[900px] h-[900px] rounded-full pointer-events-none blur-[190px] opacity-40"
        style={{
          background: 'radial-gradient(circle, rgba(255,106,0,0.55) 0%, rgba(184,66,0,0.2) 55%, transparent 80%)',
        }}
      />

      {/* 4. Bottom Giant Orange Light Reservoir */}
      <div
        className="fixed bottom-[-10%] left-1/2 -translate-x-1/2 w-[1400px] h-[600px] rounded-full pointer-events-none blur-[160px] opacity-50"
        style={{
          background: 'radial-gradient(circle, rgba(255,106,0,0.7) 0%, rgba(255,138,36,0.35) 45%, transparent 75%)',
        }}
      />

      {/* 5. Subtle micro-star/grid texture */}
      <div className="fixed inset-0 grid-pattern pointer-events-none opacity-30" />

      {/* Content wrapper */}
      <div className="relative z-10 w-full flex-1 flex flex-col items-center justify-center">
        {children}
      </div>
    </div>
  );
};

export default GlobalNeonBackground;
