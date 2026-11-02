import React from 'react';
import { ArrowRight } from 'lucide-react';

interface GlowButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  showArrow?: boolean;
  glow?: boolean;
}

export const GlowButton: React.FC<GlowButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  showArrow = false,
  glow = true,
  className = '',
  ...props
}) => {
  // Normal square / crisp corners (rounded-md/rounded-lg) as requested
  const sizeStyles = {
    sm: 'px-3.5 py-1.5 text-xs rounded-md gap-1.5',
    md: 'px-5 py-2.5 text-sm rounded-lg gap-2',
    lg: 'px-7 py-3 text-sm rounded-lg gap-2.5 font-semibold tracking-wide',
  };

  const variantStyles = {
    primary:
      'bg-gradient-to-r from-[#FF6A00] to-[#FF8A24] text-white hover:from-[#FF8A24] hover:to-[#FFB15A] hover:text-black border border-[#FFB15A]/50 shadow-[0_0_20px_rgba(255,106,0,0.45)] hover:shadow-[0_0_35px_rgba(255,106,0,0.7)]',
    secondary:
      'bg-[#0C0805] text-[#F5F0EA] border border-[#FF6A00]/40 hover:border-[#FF6A00]/90 hover:bg-[#FF6A00]/20 hover:shadow-[0_0_25px_rgba(255,106,0,0.35)]',
    ghost:
      'bg-transparent text-[#A89D92] hover:text-[#F5F0EA] hover:bg-[#FF6A00]/10 border border-transparent',
  };

  return (
    <button
      className={`group relative inline-flex items-center justify-center font-medium transition-all duration-300 active:scale-[0.98] disabled:opacity-50 disabled:pointer-events-none ${
        sizeStyles[size]
      } ${variantStyles[variant]} ${className}`}
      {...props}
    >
      <span>{children}</span>
      {showArrow && (
        <ArrowRight className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" />
      )}
    </button>
  );
};

export const NeonButton = GlowButton;
export default GlowButton;
