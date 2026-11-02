import React, { useState } from 'react';
import { Shield, ArrowRight, Lock, Mail } from 'lucide-react';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';
import { authApi } from '@/api/authApi';

export const LoginPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await authApi.login({ email, password });
    onNavigate('/command-center');
  };

  return (
    <div className="w-full max-w-md mx-auto space-y-6">
      <div className="text-center space-y-2">
        <div
          onClick={() => onNavigate('/')}
          className="inline-flex items-center gap-2.5 cursor-pointer mb-2"
        >
          <div className="w-9 h-9 rounded-xl bg-[#FF6A00] flex items-center justify-center shadow-[0_0_20px_rgba(255,106,0,0.4)]">
            <svg viewBox="0 0 100 100" className="w-5 h-5 fill-white">
              <polygon points="50,10 90,85 10,85" />
            </svg>
          </div>
          <span className="font-extrabold tracking-widest text-[#F5F0EA] text-xl font-mono">
            AEGIS
          </span>
        </div>
        <h1 className="text-2xl font-bold text-[#F5F0EA]">Access Intelligence Terminal</h1>
        <p className="text-xs text-[#A89D92]">
          Enter your executive or analyst credentials to access your tenant.
        </p>
      </div>

      <GlowCard className="p-8 space-y-5">
        <form onSubmit={handleSubmit} className="space-y-4 text-xs font-mono">
          <div>
            <label className="block text-[#A89D92] mb-1.5 font-medium">Enterprise Email</label>
            <div className="relative">
              <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#6F665F]" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="executive@primelogix.com"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-[#080604] border border-[#FF6A00]/25 text-[#F5F0EA] placeholder-[#6F665F] focus:outline-none focus:border-[#FF6A00] focus:ring-1 focus:ring-[#FF6A00]/40"
              />
            </div>
          </div>

          <div>
            <div className="flex justify-between items-center mb-1.5">
              <label className="text-[#A89D92] font-medium">Master Password</label>
              <button
                type="button"
                onClick={() => onNavigate('/forgot-password')}
                className="text-[11px] text-[#FF8A24] hover:text-[#FFB15A]"
              >
                Forgot Password?
              </button>
            </div>
            <div className="relative">
              <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#6F665F]" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-[#080604] border border-[#FF6A00]/25 text-[#F5F0EA] placeholder-[#6F665F] focus:outline-none focus:border-[#FF6A00] focus:ring-1 focus:ring-[#FF6A00]/40"
              />
            </div>
          </div>

          <div className="pt-2">
            <GlowButton type="submit" size="md" className="w-full" showArrow>
              Authenticate & Open Terminal
            </GlowButton>
          </div>
        </form>

        <div className="pt-4 border-t border-[#FF6A00]/12 text-center text-xs font-mono">
          <p className="text-[#A89D92]">
            Don't have an organization tenant?{' '}
            <button
              onClick={() => onNavigate('/signup')}
              className="text-[#FF8A24] hover:text-[#FFB15A] font-semibold"
            >
              Initialize Tenant
            </button>
          </p>
        </div>
      </GlowCard>
    </div>
  );
};

export default LoginPage;
