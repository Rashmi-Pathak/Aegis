import React, { useState } from 'react';
import { Building2, ArrowRight, Layers, Globe } from 'lucide-react';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';

export const OrganizationSetupPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const [industry, setIndustry] = useState('Logistics & Freight');
  const [scale, setScale] = useState('$50M - $250M');

  return (
    <div className="min-h-screen bg-[#080604] text-[#F5F0EA] p-6 sm:p-12 flex items-center justify-center">
      <div className="w-full max-w-2xl space-y-6">
        <div className="text-center space-y-2">
          <span className="text-xs font-mono uppercase text-[#FF8A24] font-bold tracking-widest">
            STEP 1 OF 4 • ORGANIZATION SETUP
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F0EA]">Define Business Architecture</h1>
          <p className="text-xs text-[#A89D92]">
            Configure the industry ontology and scale tier for your multi-tenant intelligence twin.
          </p>
        </div>

        <GlowCard className="p-8 space-y-6">
          <div className="space-y-4 text-xs font-mono">
            <div>
              <label className="block text-[#A89D92] mb-2 font-medium">Primary Industry Ontology</label>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
                {[
                  'Logistics & Freight',
                  'Omnichannel Retail',
                  'Enterprise B2B SaaS',
                  'Healthcare & Clinics',
                  'Industrial & Automotive',
                  'AgriTech & Food Supply',
                ].map((ind) => (
                  <button
                    key={ind}
                    type="button"
                    onClick={() => setIndustry(ind)}
                    className={`p-3 rounded-xl border text-left transition-all ${
                      industry === ind
                        ? 'border-[#FF6A00] bg-[#FF6A00]/15 text-[#FFB15A] font-bold'
                        : 'border-[#FF6A00]/15 bg-[#080604] text-[#A89D92] hover:border-[#FF6A00]/40'
                    }`}
                  >
                    {ind}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-[#A89D92] mb-2 font-medium">Annualized Operating Revenue Scale</label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                {['<$10M', '$10M - $50M', '$50M - $250M', '$250M+'].map((sc) => (
                  <button
                    key={sc}
                    type="button"
                    onClick={() => setScale(sc)}
                    className={`p-3 rounded-xl border text-center transition-all ${
                      scale === sc
                        ? 'border-[#FF6A00] bg-[#FF6A00]/15 text-[#FFB15A] font-bold'
                        : 'border-[#FF6A00]/15 bg-[#080604] text-[#A89D92] hover:border-[#FF6A00]/40'
                    }`}
                  >
                    {sc}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-[#FF6A00]/12 flex justify-between items-center">
            <button
              onClick={() => onNavigate('/')}
              className="text-xs font-mono text-[#6F665F] hover:text-[#A89D92]"
            >
              Cancel
            </button>
            <GlowButton
              size="md"
              showArrow
              onClick={() => onNavigate('/onboarding/upload')}
            >
              Continue to Data Ingestion
            </GlowButton>
          </div>
        </GlowCard>
      </div>
    </div>
  );
};

export default OrganizationSetupPage;
