import React, { useState } from 'react';
import { ArrowLeft, CheckCircle2, Shield } from 'lucide-react';
import GlowButton from '@/components/GlowButton';
import GlowCard from '@/components/GlowCard';

export const RequestDemoPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const [submitted, setSubmitted] = useState(false);

  return (
    <div className="min-h-screen bg-[#080604] text-[#F5F0EA] p-6 sm:p-12 flex items-center justify-center">
      <div className="w-full max-w-lg space-y-6">
        <button
          onClick={() => onNavigate('/')}
          className="inline-flex items-center gap-2 text-xs font-mono text-[#A89D92] hover:text-[#FFB15A]"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Home
        </button>

        <GlowCard className="p-8">
          <div className="mb-6 space-y-2">
            <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold tracking-wider">
              ENTERPRISE PILOT
            </span>
            <h1 className="text-2xl font-bold text-[#F5F0EA]">Request Private AEGIS Demo</h1>
            <p className="text-xs text-[#A89D92]">
              Experience AEGIS tailored to your company's proprietary data and ERP ecosystem.
            </p>
          </div>

          {submitted ? (
            <div className="text-center py-8 space-y-3 font-mono">
              <CheckCircle2 className="w-12 h-12 text-[#FF6A00] mx-auto animate-pulse" />
              <h3 className="text-base font-bold text-[#F5F0EA]">Request Received</h3>
              <p className="text-xs text-[#A89D92]">
                Our enterprise architecture team will contact you within 24 hours.
              </p>
              <div className="pt-4">
                <GlowButton size="sm" onClick={() => onNavigate('/demo')}>
                  Explore Public Sandbox
                </GlowButton>
              </div>
            </div>
          ) : (
            <form
              onSubmit={(e) => {
                e.preventDefault();
                setSubmitted(true);
              }}
              className="space-y-4 text-xs font-mono"
            >
              <div>
                <label className="block text-[#A89D92] mb-1">Work Email</label>
                <input
                  type="email"
                  required
                  placeholder="executive@enterprise.com"
                  className="w-full px-4 py-2.5 rounded-xl bg-[#080604] border border-[#FF6A00]/25 text-[#F5F0EA] focus:outline-none focus:border-[#FF6A00]"
                />
              </div>

              <div>
                <label className="block text-[#A89D92] mb-1">Company / Organization</label>
                <input
                  type="text"
                  required
                  placeholder="Global Freight Solutions Inc."
                  className="w-full px-4 py-2.5 rounded-xl bg-[#080604] border border-[#FF6A00]/25 text-[#F5F0EA] focus:outline-none focus:border-[#FF6A00]"
                />
              </div>

              <div>
                <label className="block text-[#A89D92] mb-1">Primary Industry</label>
                <select className="w-full px-4 py-2.5 rounded-xl bg-[#080604] border border-[#FF6A00]/25 text-[#F5F0EA] focus:outline-none focus:border-[#FF6A00]">
                  <option>Logistics & Supply Chain</option>
                  <option>Omnichannel Retail</option>
                  <option>Enterprise SaaS</option>
                  <option>Healthcare & Life Sciences</option>
                  <option>Manufacturing & Automotive</option>
                  <option>Other Enterprise</option>
                </select>
              </div>

              <div className="pt-2">
                <GlowButton type="submit" size="md" className="w-full">
                  Submit Demonstration Request
                </GlowButton>
              </div>
            </form>
          )}
        </GlowCard>
      </div>
    </div>
  );
};

export default RequestDemoPage;
