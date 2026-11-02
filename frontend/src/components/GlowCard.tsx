import React, { useRef, useState, useCallback } from 'react';

interface GlowCardProps {
  children: React.ReactNode;
  className?: string;
  glowIntensity?: 'subtle' | 'medium' | 'high';
  internalGlow?: boolean; // Enables glowing orange inside the card matching reference
  enableTilt?: boolean; // 3D physics-based interactive hover tilt
  maxTilt?: number; // Max tilt degrees (default 12)
  onClick?: () => void;
}

export const GlowCard: React.FC<GlowCardProps> = ({
  children,
  className = '',
  glowIntensity = 'subtle',
  internalGlow = true,
  enableTilt = true,
  maxTilt = 12,
  onClick,
}) => {
  const cardRef = useRef<HTMLDivElement>(null);
  const [isHovered, setIsHovered] = useState(false);
  const [tilt, setTilt] = useState({ rotateX: 0, rotateY: 0, mouseX: 0, mouseY: 0 });

  const handleMouseMove = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      if (!enableTilt || !cardRef.current) return;
      const rect = cardRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      // Tilts toward cursor: when mouse is top-right, right tilts forward/up, top dips or rises
      const rotateY = ((x - centerX) / centerX) * maxTilt;
      const rotateX = -((y - centerY) / centerY) * maxTilt;

      setTilt({
        rotateX,
        rotateY,
        mouseX: x,
        mouseY: y,
      });
    },
    [enableTilt, maxTilt]
  );

  const handleMouseEnter = useCallback(() => {
    if (enableTilt) setIsHovered(true);
  }, [enableTilt]);

  const handleMouseLeave = useCallback(() => {
    if (!enableTilt) return;
    setIsHovered(false);
    setTilt({ rotateX: 0, rotateY: 0, mouseX: 0, mouseY: 0 });
  }, [enableTilt]);

  const borderClass =
    glowIntensity === 'high'
      ? 'border-[#FF6A00]/60 shadow-[0_0_35px_rgba(255,106,0,0.3)]'
      : glowIntensity === 'medium'
      ? 'border-[#FF6A00]/35 shadow-[0_0_22px_rgba(255,106,0,0.18)]'
      : 'border-[#FF6A00]/22 hover:border-[#FF6A00]/60 hover:shadow-[0_0_35px_rgba(255,106,0,0.3)]';

  return (
    <div
      ref={cardRef}
      onClick={onClick}
      onMouseMove={handleMouseMove}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      style={{
        transform:
          enableTilt && isHovered
            ? `perspective(1000px) rotateX(${tilt.rotateX}deg) rotateY(${tilt.rotateY}deg) scale3d(1.02, 1.02, 1.02)`
            : 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)',
        transition:
          enableTilt && isHovered
            ? 'transform 0.08s ease-out'
            : 'transform 0.5s cubic-bezier(0.23, 1, 0.32, 1), border-color 0.3s, box-shadow 0.3s',
        transformStyle: 'preserve-3d',
      }}
      className={`relative rounded-xl bg-[#0C0805] p-6 border overflow-hidden ${borderClass} ${
        onClick ? 'cursor-pointer' : ''
      } ${className}`}
    >
      {/* 1. Dynamic Cursor Spotlight (follows mouse on hover for authentic glass shine) */}
      {enableTilt && isHovered && (
        <div
          className="absolute inset-0 pointer-events-none transition-opacity duration-300"
          style={{
            background: `radial-gradient(circle 320px at ${tilt.mouseX}px ${tilt.mouseY}px, rgba(255, 138, 36, 0.28) 0%, rgba(255, 106, 0, 0.08) 50%, transparent 80%)`,
          }}
        />
      )}

      {/* 2. Internal rich orange glow pool from the bottom (matching reference image) */}
      {internalGlow && (
        <div
          className="absolute inset-0 pointer-events-none transition-opacity duration-500"
          style={{
            background:
              'radial-gradient(ellipse at 50% 115%, rgba(255, 106, 0, 0.45) 0%, rgba(255, 138, 36, 0.16) 45%, transparent 75%)',
          }}
        />
      )}

      {/* 3. Razor-sharp subtle orange reflection line at the top rim */}
      <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-[#FFB15A]/40 to-transparent pointer-events-none" />

      {/* 4. Razor-sharp bottom warm rim */}
      <div className="absolute bottom-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-[#FF6A00]/60 to-transparent pointer-events-none" />

      {/* Card Content floating with 3D depth */}
      <div
        className="relative z-10"
        style={{
          transform: enableTilt && isHovered ? 'translateZ(18px)' : 'translateZ(0px)',
          transition: 'transform 0.2s ease-out',
        }}
      >
        {children}
      </div>
    </div>
  );
};

export const GlassCard = GlowCard;
export default GlowCard;
