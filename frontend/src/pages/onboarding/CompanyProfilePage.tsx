import React from 'react';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';

export const CompanyProfilePage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  return (
    <div className="min-h-screen bg-[#080604] text-[#F5F0EA] p-6 sm:p-12 flex items-center justify-center">
      <GlowCard className="w-full max-w-xl p-8 space-y-4">
        <h2 className="text-xl font-bold">Company Profile Configuration</h2>
        <p className="text-xs text-[#A89D92]">Set up your organizational profile parameters.</p>
        <GlowButton size="sm" onClick={() => onNavigate('/onboarding/upload')}>
          Proceed to Ingestion
        </GlowButton>
      </GlowCard>
    </div>
  );
};

export const BusinessOperationsPage = CompanyProfilePage;
export const BusinessScalePage = CompanyProfilePage;
export const DataConnectionPage = CompanyProfilePage;
export const OnboardingCompletePage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  return (
    <div className="min-h-screen bg-[#080604] text-[#F5F0EA] p-6 sm:p-12 flex items-center justify-center">
      <GlowCard className="w-full max-w-xl p-8 text-center space-y-4">
        <h2 className="text-xl font-bold">Onboarding Complete</h2>
        <p className="text-xs text-[#A89D92]">Your AEGIS intelligence twin is live.</p>
        <GlowButton size="md" onClick={() => onNavigate('/command-center')}>
          Enter Command Center
        </GlowButton>
      </GlowCard>
    </div>
  );
};

export default CompanyProfilePage;
