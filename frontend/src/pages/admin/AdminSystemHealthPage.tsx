import React from 'react';
import { Cpu, Server, Activity, Users, Database, Shield, Terminal, RefreshCw } from 'lucide-react';
import SectionHeader from '@/components/SectionHeader';
import GlowCard from '@/components/GlowCard';
import GlowButton from '@/components/GlowButton';
import DataTable from '@/components/DataTable';

export const AdminSystemHealthPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#FF6A00]/14 pb-6">
        <div>
          <span className="text-xs font-mono uppercase text-[#FF8A24] font-semibold tracking-wider">
            SUPER ADMIN TELEMETRY
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F0EA] tracking-tight mt-1">
            System Infrastructure & Cluster Health
          </h1>
          <p className="text-xs text-[#A89D92] mt-1 font-mono">
            FastAPI Workers • Redis Queue • MLflow Tracking • Multi-Tenant Isolation
          </p>
        </div>

        <div className="flex items-center gap-2">
          {['Tenants', 'Users', 'Subscriptions', 'API Usage', 'Cluster Health', 'Jobs', 'Audit'].map((tab) => (
            <button
              key={tab}
              onClick={() => {}}
              className="px-3 py-1.5 rounded-xl bg-[#120C08] border border-[#FF6A00]/18 text-xs font-mono text-[#A89D92] hover:text-[#F5F0EA] hover:border-[#FF6A00]/40 transition-colors"
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Cluster Hardware Telemetry Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 font-mono">
        <GlowCard className="p-4">
          <div className="flex items-center justify-between text-xs text-[#6F665F]">
            <span>CPU UTILIZATION</span>
            <Cpu className="w-4 h-4 text-[#FF6A00]" />
          </div>
          <p className="text-2xl font-bold text-[#F5F0EA] mt-2">24.8%</p>
          <p className="text-[10px] text-emerald-400 mt-0.5">16 vCPUs (Optimal Load)</p>
        </GlowCard>

        <GlowCard className="p-4">
          <div className="flex items-center justify-between text-xs text-[#6F665F]">
            <span>MEMORY (RAM)</span>
            <Server className="w-4 h-4 text-[#FF8A24]" />
          </div>
          <p className="text-2xl font-bold text-[#FFB15A] mt-2">18.4 GB</p>
          <p className="text-[10px] text-[#A89D92] mt-0.5">of 64 GB Allocated</p>
        </GlowCard>

        <GlowCard className="p-4">
          <div className="flex items-center justify-between text-xs text-[#6F665F]">
            <span>REDIS JOB QUEUE</span>
            <Activity className="w-4 h-4 text-[#FF6A00]" />
          </div>
          <p className="text-2xl font-bold text-[#FF6A00] mt-2">4 Pending</p>
          <p className="text-[10px] text-[#FF8A24] mt-0.5">Ingestion & Drift Batches</p>
        </GlowCard>

        <GlowCard className="p-4">
          <div className="flex items-center justify-between text-xs text-[#6F665F]">
            <span>API ERROR RATE</span>
            <Shield className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-emerald-400 mt-2">0.002%</p>
          <p className="text-[10px] text-[#A89D92] mt-0.5">2.4M Calls / 24h</p>
        </GlowCard>
      </div>

      {/* Multi-Tenant Organizations Table */}
      <div className="space-y-4">
        <SectionHeader
          badge="MULTI-TENANT DIRECTORY"
          title="Active Enterprise Organizations"
          description="Isolated organization_id environments running on AEGIS infrastructure."
        />

        <DataTable
          columns={[
            { key: 'name', header: 'Organization' },
            { key: 'industry', header: 'Industry' },
            {
              key: 'tier',
              header: 'Subscription Tier',
              render: (org: any) => (
                <span className="font-mono text-xs text-[#FF8A24] uppercase font-bold">
                  {org.tier}
                </span>
              ),
            },
            {
              key: 'health',
              header: 'Health Score',
              render: (org: any) => <span className="font-mono font-bold text-[#FFB15A]">{org.health} / 100</span>,
            },
            {
              key: 'status',
              header: 'Cluster Status',
              render: () => <span className="font-mono text-xs text-emerald-400">ACTIVE</span>,
            },
          ]}
          data={[
            { name: 'PrimeLogix Global', industry: 'Logistics & Freight', tier: 'enterprise', health: 78 },
            { name: 'NovaMart Superstores', industry: 'Omnichannel Retail', tier: 'enterprise', health: 74 },
            { name: 'CloudNest Systems', industry: 'Enterprise SaaS', tier: 'growth', health: 82 },
            { name: 'AutoCore EV Assembly', industry: 'Automotive Manufacturing', tier: 'enterprise', health: 71 },
            { name: 'MediPlus Health Network', industry: 'Healthcare & Diagnostic', tier: 'enterprise', health: 79 },
          ]}
          keyExtractor={(org: any) => org.name}
        />
      </div>
    </div>
  );
};

export const AdminOrganizationsPage = AdminSystemHealthPage;
export const AdminUsersPage = AdminSystemHealthPage;
export const AdminSubscriptionsPage = AdminSystemHealthPage;
export const AdminUsagePage = AdminSystemHealthPage;
export const AdminModelsPage = AdminSystemHealthPage;
export const AdminJobsPage = AdminSystemHealthPage;
export const AdminAuditLogsPage = AdminSystemHealthPage;

export default AdminSystemHealthPage;
