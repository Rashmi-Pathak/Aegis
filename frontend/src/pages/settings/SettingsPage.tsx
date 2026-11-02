import React, { useState } from 'react';
import { Settings, Building2, Users, Shield, Sliders, Bell } from 'lucide-react';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';

export const SettingsPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const [activeTab, setActiveTab] = useState<'org' | 'users' | 'security' | 'integrations'>('org');

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      <div className="border-b border-[#FF6A00]/14 pb-5">
        <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold tracking-wider">
          PLATFORM CONFIGURATION
        </span>
        <h1 className="text-2xl font-bold text-[#F5F0EA] mt-1">Tenant & System Settings</h1>
        <p className="text-xs font-mono text-[#A89D92]">
          Manage organization profiles, user RBAC privileges, API tokens, and cloud ingestion endpoints.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {/* Navigation Sidebar */}
        <div className="space-y-1 text-xs font-mono">
          {[
            { id: 'org', label: 'Organization & Profile', icon: Building2 },
            { id: 'users', label: 'Team Members & Roles', icon: Users },
            { id: 'security', label: 'Authentication & Security', icon: Shield },
            { id: 'integrations', label: 'Cloud Connectors & APIs', icon: Sliders },
          ].map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id as any)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-left transition-colors ${
                  activeTab === item.id
                    ? 'bg-[#FF6A00] text-white font-semibold'
                    : 'text-[#A89D92] hover:text-[#F5F0EA] bg-[#120C08]'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>

        {/* Settings Body */}
        <GlowCard className="md:col-span-3 space-y-6">
          {activeTab === 'org' && (
            <div className="space-y-4 text-xs font-mono">
              <h3 className="text-base font-bold text-[#F5F0EA] font-sans">Organization Profile</h3>
              <div>
                <label className="block text-[#A89D92] mb-1">Company Legal Name</label>
                <input
                  type="text"
                  defaultValue="PrimeLogix Global Intermodal Inc."
                  className="w-full px-3.5 py-2 rounded-xl bg-[#080604] border border-[#FF6A00]/25 text-[#F5F0EA] focus:outline-none focus:border-[#FF6A00]"
                />
              </div>
              <div>
                <label className="block text-[#A89D92] mb-1">Primary Operating Industry</label>
                <input
                  type="text"
                  defaultValue="Freight & Global Logistics"
                  className="w-full px-3.5 py-2 rounded-xl bg-[#080604] border border-[#FF6A00]/25 text-[#F5F0EA] focus:outline-none focus:border-[#FF6A00]"
                />
              </div>
              <div className="pt-2">
                <GlowButton size="sm">Save Changes</GlowButton>
              </div>
            </div>
          )}

          {activeTab === 'users' && (
            <div className="space-y-4 text-xs font-mono">
              <h3 className="text-base font-bold text-[#F5F0EA] font-sans">Active Team Members</h3>
              <div className="space-y-2">
                {[
                  { name: 'Marcus Vance', role: 'Chief Risk Officer (Super Admin)', email: 'm.vance@primelogix.com' },
                  { name: 'Sarah Lin', role: 'Lead Supply Chain Analyst', email: 's.lin@primelogix.com' },
                  { name: 'Devon Hayes', role: 'Operations Controller', email: 'd.hayes@primelogix.com' },
                ].map((u) => (
                  <div key={u.email} className="p-3 rounded-xl bg-[#080604] border border-[#FF6A00]/15 flex items-center justify-between">
                    <div>
                      <span className="font-bold text-[#F5F0EA] block">{u.name}</span>
                      <span className="text-[10px] text-[#6F665F]">{u.email}</span>
                    </div>
                    <span className="text-[11px] text-[#FF8A24] font-semibold">{u.role}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div className="space-y-4 text-xs font-mono">
              <h3 className="text-base font-bold text-[#F5F0EA] font-sans">Security & Tenant Isolation</h3>
              <p className="text-[#A89D92]">
                Row-level database security enforced via organization_id isolation tokens.
              </p>
              <div className="p-4 rounded-xl bg-[#080604] border border-[#FF6A00]/20 space-y-2">
                <div className="flex justify-between">
                  <span className="text-[#6F665F]">Encryption Standard:</span>
                  <span className="text-[#FFB15A]">AES-256-GCM at rest, TLS 1.3 in transit</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-[#6F665F]">Audit Log Retention:</span>
                  <span className="text-[#F5F0EA]">365 Days</span>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'integrations' && (
            <div className="space-y-4 text-xs font-mono">
              <h3 className="text-base font-bold text-[#F5F0EA] font-sans">Cloud Connectors</h3>
              <div className="space-y-2">
                <div className="p-3 rounded-xl bg-[#080604] border border-emerald-500/30 flex justify-between items-center">
                  <span>PostgreSQL Primary Telemetry Replica</span>
                  <span className="text-emerald-400 font-bold">CONNECTED</span>
                </div>
                <div className="p-3 rounded-xl bg-[#080604] border border-[#FF6A00]/25 flex justify-between items-center">
                  <span>SAP ERP OData Gateway</span>
                  <span className="text-[#FF8A24]">SYNCHRONIZING</span>
                </div>
              </div>
            </div>
          )}
        </GlowCard>
      </div>
    </div>
  );
};

export default SettingsPage;
