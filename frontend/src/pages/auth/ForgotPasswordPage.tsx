import React, { useState } from 'react';
import { ArrowLeft, Mail, CheckCircle2 } from 'lucide-react';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';

export const ForgotPasswordPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);

  return (
    <div className="w-full max-w-md mx-auto space-y-6">
      <div className="text-center space-y-2">
        <h1 className="text-2xl font-bold text-[#F5F0EA]">Reset Terminal Access</h1>
        <p className="text-xs text-[#A89D92]">
          Enter your registered enterprise email to receive secure recovery credentials.
        </p>
      </div>

      <GlowCard className="p-8">
        {sent ? (
          <div className="text-center py-6 space-y-3 font-mono text-xs">
            <CheckCircle2 className="w-12 h-12 text-[#FF6A00] mx-auto animate-pulse" />
            <h3 className="text-sm font-bold text-[#F5F0EA]">Reset Link Dispatched</h3>
            <p className="text-[#A89D92]">Check your enterprise inbox for authentication token instructions.</p>
            <div className="pt-4">
              <GlowButton size="sm" onClick={() => onNavigate('/login')}>
                Back to Sign In
              </GlowButton>
            </div>
          </div>
        ) : (
          <form
            onSubmit={(e) => {
              e.preventDefault();
              setSent(true);
            }}
            className="space-y-4 text-xs font-mono"
          >
            <div>
              <label className="block text-[#A89D92] mb-1.5 font-medium">Enterprise Email</label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#6F665F]" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="executive@company.com"
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-[#080604] border border-[#FF6A00]/25 text-[#F5F0EA] focus:outline-none focus:border-[#FF6A00]"
                />
              </div>
            </div>

            <div className="pt-2">
              <GlowButton type="submit" size="md" className="w-full">
                Dispatch Password Recovery
              </GlowButton>
            </div>

            <div className="text-center pt-3">
              <button
                type="button"
                onClick={() => onNavigate('/login')}
                className="text-xs font-mono text-[#A89D92] hover:text-[#FFB15A]"
              >
                ← Return to Login
              </button>
            </div>
          </form>
        )}
      </GlowCard>
    </div>
  );
};

export default ForgotPasswordPage;
