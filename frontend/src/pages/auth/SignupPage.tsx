import React, { useState } from 'react';
import { ArrowRight, Lock, Mail, Building2, User } from 'lucide-react';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';
import { authApi } from '@/api/authApi';

export const SignupPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    organizationName: '',
    password: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await authApi.signup(formData);
    onNavigate('/onboarding/organization');
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
        <h1 className="text-2xl font-bold text-[#F5F0EA]">Provision Enterprise Tenant</h1>
        <p className="text-xs text-[#A89D92]">
          Deploy a dedicated multi-tenant AEGIS instance with isolated telemetry.
        </p>
      </div>

      <GlowCard className="p-8 space-y-5">
        <form onSubmit={handleSubmit} className="space-y-4 text-xs font-mono">
          <div>
            <label className="block text-[#A89D92] mb-1.5 font-medium">Full Name</label>
            <div className="relative">
              <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#6F665F]" />
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="Marcus Vance"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-[#080604] border border-[#FF6A00]/25 text-[#F5F0EA] placeholder-[#6F665F] focus:outline-none focus:border-[#FF6A00]"
              />
            </div>
          </div>

          <div>
            <label className="block text-[#A89D92] mb-1.5 font-medium">Enterprise Email</label>
            <div className="relative">
              <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#6F665F]" />
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                placeholder="m.vance@company.com"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-[#080604] border border-[#FF6A00]/25 text-[#F5F0EA] placeholder-[#6F665F] focus:outline-none focus:border-[#FF6A00]"
              />
            </div>
          </div>

          <div>
            <label className="block text-[#A89D92] mb-1.5 font-medium">Organization / Legal Entity</label>
            <div className="relative">
              <Building2 className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#6F665F]" />
              <input
                type="text"
                required
                value={formData.organizationName}
                onChange={(e) => setFormData({ ...formData, organizationName: e.target.value })}
                placeholder="Apex Freight Logistics Group"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-[#080604] border border-[#FF6A00]/25 text-[#F5F0EA] placeholder-[#6F665F] focus:outline-none focus:border-[#FF6A00]"
              />
            </div>
          </div>

          <div>
            <label className="block text-[#A89D92] mb-1.5 font-medium">Password</label>
            <div className="relative">
              <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#6F665F]" />
              <input
                type="password"
                required
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                placeholder="••••••••••••"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-[#080604] border border-[#FF6A00]/25 text-[#F5F0EA] placeholder-[#6F665F] focus:outline-none focus:border-[#FF6A00]"
              />
            </div>
          </div>

          <div className="pt-2">
            <GlowButton type="submit" size="md" className="w-full" showArrow>
              Create Account & Configure Tenant
            </GlowButton>
          </div>
        </form>

        <div className="pt-4 border-t border-[#FF6A00]/12 text-center text-xs font-mono">
          <p className="text-[#A89D92]">
            Already have access?{' '}
            <button
              onClick={() => onNavigate('/login')}
              className="text-[#FF8A24] hover:text-[#FFB15A] font-semibold"
            >
              Sign In
            </button>
          </p>
        </div>
      </GlowCard>
    </div>
  );
};

export default SignupPage;
