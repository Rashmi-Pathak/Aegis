import React from 'react';

export const CommandCenterBackground: React.FC = () => {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden bg-[#080604]">
      {/* Subtle top horizontal glowing hairline */}
      <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-[#FF6A00]/40 to-transparent" />

      {/* Top right ambient telemetry glow */}
      <div
        className="absolute top-[-100px] right-[-100px] w-[500px] h-[500px] rounded-full blur-[140px] opacity-15"
        style={{
          background: 'radial-gradient(circle, rgba(255,106,0,0.4) 0%, transparent 70%)',
        }}
      />

      {/* Bottom left subtle warm fill */}
      <div
        className="absolute bottom-[-150px] left-[200px] w-[600px] h-[600px] rounded-full blur-[160px] opacity-10"
        style={{
          background: 'radial-gradient(circle, rgba(255,177,90,0.3) 0%, transparent 70%)',
        }}
      />

      {/* Fine grid */}
      <div className="absolute inset-0 grid-pattern opacity-25" />
    </div>
  );
};

export default CommandCenterBackground;
