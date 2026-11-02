import React from 'react';
import Lightning from '@/animations/Lightning';

interface HeroGlowBackgroundProps {
  showLightning?: boolean;
}

export const HeroGlowBackground: React.FC<HeroGlowBackgroundProps> = ({ showLightning = true }) => {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none select-none z-0">
      {/* Massive hot orange center bloom from above */}
      <div
        className="absolute top-[-100px] left-1/2 -translate-x-1/2 w-[1100px] h-[650px] rounded-full blur-[160px] opacity-60"
        style={{
          background: 'radial-gradient(ellipse at center, rgba(255,106,0,0.7) 0%, rgba(255,138,36,0.4) 40%, rgba(184,66,0,0.15) 65%, transparent 80%)',
        }}
      />

      {/* Atmospheric Lightning */}
      {showLightning && (
        <div className="absolute inset-0 opacity-45 mix-blend-screen pointer-events-auto">
          <Lightning
            color="#FF6A00"
            bolts={1}
            spread={0.55}
            branches={0.45}
            xOffset={0}
            angle={0}
            size={1}
            thickness={1}
            glow={1.15}
            intensity={0.72}
            speed={0.65}
            flicker={0.48}
            mouseInteraction={true}
            mouseStrength={0.8}
            clickStrike={true}
            intro={true}
            fade={0.15}
            opacity={0.5}
            lightMode={false}
          />
        </div>
      )}

      {/* Fine grid overlay */}
      <div className="absolute inset-0 grid-pattern opacity-35" />
    </div>
  );
};

export default HeroGlowBackground;
