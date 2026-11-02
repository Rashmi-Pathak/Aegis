import React from 'react';

export const AuthLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="min-h-screen w-full bg-[#050302] flex items-center justify-center p-4 sm:p-6 relative overflow-hidden select-none">
      {/* 1. Top Radiant Orange Light Pool */}
      <div
        className="fixed top-[-10%] left-1/2 -translate-x-1/2 w-[1100px] h-[650px] rounded-full pointer-events-none blur-[160px] opacity-50"
        style={{
          background:
            'radial-gradient(circle, rgba(255,106,0,0.65) 0%, rgba(217,91,0,0.3) 45%, transparent 75%)',
        }}
      />

      {/* 2. Bottom Giant Orange Light Reservoir */}
      <div
        className="fixed bottom-[-10%] left-1/2 -translate-x-1/2 w-[1200px] h-[600px] rounded-full pointer-events-none blur-[160px] opacity-45"
        style={{
          background:
            'radial-gradient(circle, rgba(255,106,0,0.65) 0%, rgba(255,138,36,0.3) 45%, transparent 75%)',
        }}
      />

      {/* 3. Subtle micro-star/grid texture */}
      <div className="fixed inset-0 grid-pattern pointer-events-none opacity-30" />

      {/* Centered Auth Box in exact middle of viewport */}
      <div className="relative z-10 w-full max-w-md mx-auto my-auto flex flex-col items-center justify-center">
        <div className="w-full">{children}</div>
      </div>
    </div>
  );
};

export default AuthLayout;
