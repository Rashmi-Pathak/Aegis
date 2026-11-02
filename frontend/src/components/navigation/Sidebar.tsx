import React from 'react';
import {
  LayoutDashboard,
  Brain,
  TrendingUp,
  BarChart3,
  AlertTriangle,
  ShieldAlert,
  SearchCode,
  Sliders,
  Workflow,
  Network,
  FileText,
  Bell,
  Database,
  Cpu,
  Settings,
  Building2,
  Users,
  Compass,
  PanelLeftClose,
  PanelLeftOpen,
  ChevronLeft,
  ChevronRight,
  X,
} from 'lucide-react';

interface SidebarProps {
  currentPath: string;
  onNavigate: (path: string) => void;
  className?: string;
  collapsed?: boolean;
  onToggleCollapse?: () => void;
  isMobileOpen?: boolean;
  onCloseMobile?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentPath,
  onNavigate,
  className = '',
  collapsed = false,
  onToggleCollapse,
  isMobileOpen = false,
  onCloseMobile,
}) => {
  const navSections = [
    {
      title: 'COMMAND',
      items: [
        { label: 'Command Center', path: '/command-center', icon: LayoutDashboard },
        { label: 'Demo Environments', path: '/demo', icon: Compass },
      ],
    },
    {
      title: 'INTELLIGENCE',
      items: [
        { label: 'Analytics & KPIs', path: '/analytics', icon: BarChart3 },
        { label: 'Forecast Center', path: '/forecast-center', icon: TrendingUp },
        { label: 'Anomaly Engine', path: '/anomalies', icon: AlertTriangle },
        { label: 'Risk Intelligence', path: '/risk-center', icon: ShieldAlert },
        { label: 'Investigation Workspace', path: '/investigation', icon: SearchCode },
        { label: 'Decision Engine', path: '/decision-center', icon: Sliders },
        { label: 'What-If Simulation', path: '/simulation', icon: Workflow },
        { label: 'Business Digital Twin', path: '/business-graph', icon: Network },
      ],
    },
    {
      title: 'DATA & INFRASTRUCTURE',
      items: [
        { label: 'Data Center & Schemas', path: '/data-center', icon: Database },
        { label: 'Model Intelligence', path: '/models', icon: Cpu },
        { label: 'Executive Reports', path: '/reports', icon: FileText },
        { label: 'System Alerts', path: '/alerts', icon: Bell },
      ],
    },
    {
      title: 'GOVERNANCE',
      items: [
        { label: 'Organization & Team', path: '/settings/organization', icon: Building2 },
        { label: 'Settings', path: '/settings', icon: Settings },
        { label: 'Super Admin', path: '/admin', icon: Users },
      ],
    },
  ];

  const handleNavClick = (path: string) => {
    onNavigate(path);
    if (onCloseMobile) {
      onCloseMobile();
    }
  };

  return (
    <>
      {/* ============================================================== */}
      {/* 1. MOBILE BACKDROP & DRAWER (< lg screens)                      */}
      {/* ============================================================== */}
      <div
        className={`fixed inset-0 bg-black/80 backdrop-blur-sm z-40 transition-opacity duration-300 lg:hidden ${
          isMobileOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
        }`}
        onClick={onCloseMobile}
        aria-hidden={!isMobileOpen}
      />

      <div
        className={`fixed inset-y-0 left-0 z-50 w-72 max-w-[85vw] bg-[#0A0705] border-r border-[#FF6A00]/25 shadow-[0_0_50px_rgba(0,0,0,0.9)] flex flex-col justify-between transition-transform duration-300 ease-in-out lg:hidden ${
          isMobileOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
        role="dialog"
        aria-modal="true"
      >
        {/* Mobile Header */}
        <div>
          <div className="h-16 px-5 border-b border-[#FF6A00]/14 flex items-center justify-between">
            <div
              onClick={() => handleNavClick('/')}
              className="flex items-center gap-2.5 cursor-pointer group"
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#FF6A00] to-[#FF8A24] p-1.5 flex items-center justify-center shadow-[0_0_15px_rgba(255,106,0,0.4)]">
                <svg viewBox="0 0 100 100" className="w-full h-full fill-white">
                  <polygon points="50,10 90,85 10,85" />
                </svg>
              </div>
              <div className="flex flex-col">
                <span className="font-extrabold tracking-widest text-[#F5F0EA] text-base leading-none">
                  AEGIS
                </span>
                <span className="text-[9px] font-mono tracking-wider text-[#FF8A24] mt-0.5">
                  DECISION INTEL
                </span>
              </div>
            </div>

            <button
              onClick={onCloseMobile}
              className="p-2 rounded-xl text-[#A89D92] hover:text-[#F5F0EA] hover:bg-[#FF6A00]/10 border border-[#FF6A00]/15"
              aria-label="Close navigation"
            >
              <X className="w-5 h-5 text-[#FF8A24]" />
            </button>
          </div>

          {/* Mobile Navigation Links */}
          <div className="py-4 px-3 space-y-5 overflow-y-auto max-h-[calc(100vh-140px)]">
            {navSections.map((sec) => (
              <div key={sec.title}>
                <p className="px-3 text-[10px] font-mono uppercase tracking-widest text-[#6F665F] font-semibold mb-2">
                  {sec.title}
                </p>
                <div className="space-y-1">
                  {sec.items.map((item) => {
                    const Icon = item.icon;
                    const isActive = currentPath.startsWith(item.path);
                    return (
                      <button
                        key={item.path}
                        onClick={() => handleNavClick(item.path)}
                        className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 group ${
                          isActive
                            ? 'bg-[#FF6A00]/15 text-[#FFB15A] border border-[#FF6A00]/30 shadow-[0_0_12px_rgba(255,106,0,0.15)] font-semibold'
                            : 'text-[#A89D92] hover:text-[#F5F0EA] hover:bg-[#FF6A00]/06'
                        }`}
                      >
                        <Icon
                          className={`w-4 h-4 shrink-0 transition-colors ${
                            isActive ? 'text-[#FF6A00]' : 'text-[#6F665F] group-hover:text-[#FF8A24]'
                          }`}
                        />
                        <span className="truncate">{item.label}</span>
                        {isActive && (
                          <span className="ml-auto w-1.5 h-1.5 rounded-full bg-[#FF6A00] shadow-[0_0_6px_#FF6A00]" />
                        )}
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Mobile Footer Org */}
        <div className="p-3 border-t border-[#FF6A00]/14">
          <div
            onClick={() => handleNavClick('/settings/organization')}
            className="p-2.5 rounded-xl bg-[#120C08] border border-[#FF6A00]/15 flex items-center gap-3 cursor-pointer hover:border-[#FF6A00]/40 transition-colors"
          >
            <div className="w-8 h-8 rounded-lg bg-[#FF6A00]/20 border border-[#FF6A00]/30 flex items-center justify-center text-[#FF8A24] font-mono font-bold text-xs shrink-0">
              PL
            </div>
            <div className="flex flex-col min-w-0">
              <span className="text-xs font-semibold text-[#F5F0EA] truncate">PrimeLogix</span>
              <span className="text-[10px] font-mono text-[#A89D92]">Enterprise Tier • Active</span>
            </div>
          </div>
        </div>
      </div>

      {/* ============================================================== */}
      {/* 2. DESKTOP RESPONSIVE SIDEBAR (>= lg screens)                  */}
      {/* ============================================================== */}
      <aside
        className={`hidden lg:flex h-screen sticky top-0 bg-[#0A0705] border-r border-[#FF6A00]/14 flex-col justify-between select-none z-30 transition-all duration-300 ease-in-out ${
          collapsed ? 'w-18' : 'w-64'
        } ${className}`}
      >
        {/* Brand Header with Collapse / Expand Toggle */}
        <div>
          <div className="h-16 px-4 border-b border-[#FF6A00]/14 flex items-center justify-between">
            <div
              onClick={() => onNavigate('/')}
              className="flex items-center gap-2.5 cursor-pointer group min-w-0"
              title="AEGIS Decision Intelligence"
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#FF6A00] to-[#FF8A24] p-1.5 flex items-center justify-center shadow-[0_0_15px_rgba(255,106,0,0.4)] group-hover:shadow-[0_0_20px_rgba(255,106,0,0.6)] transition-all shrink-0">
                <svg viewBox="0 0 100 100" className="w-full h-full fill-white">
                  <polygon points="50,10 90,85 10,85" />
                </svg>
              </div>
              {!collapsed && (
                <div className="flex flex-col truncate">
                  <span className="font-extrabold tracking-widest text-[#F5F0EA] text-base leading-none">
                    AEGIS
                  </span>
                  <span className="text-[9px] font-mono tracking-wider text-[#FF8A24] mt-0.5">
                    DECISION INTEL
                  </span>
                </div>
              )}
            </div>

            {/* Quick Toggle Button on Sidebar Header */}
            {onToggleCollapse && (
              <button
                onClick={onToggleCollapse}
                className="p-1.5 rounded-lg text-[#6F665F] hover:text-[#FF8A24] hover:bg-[#FF6A00]/10 transition-colors"
                title={collapsed ? 'Expand sidebar' : 'Shrink sidebar (wider analytics)'}
                aria-label="Toggle sidebar width"
              >
                {collapsed ? (
                  <ChevronRight className="w-4 h-4 text-[#FF8A24]" />
                ) : (
                  <PanelLeftClose className="w-4 h-4 text-[#A89D92]" />
                )}
              </button>
            )}
          </div>

          {/* Navigation list */}
          <div className="py-4 px-2 space-y-6 overflow-y-auto max-h-[calc(100vh-140px)] scrollbar-none">
            {navSections.map((sec) => (
              <div key={sec.title}>
                {!collapsed ? (
                  <p className="px-3 text-[10px] font-mono uppercase tracking-widest text-[#6F665F] font-semibold mb-2">
                    {sec.title}
                  </p>
                ) : (
                  <div className="w-full h-px bg-[#FF6A00]/10 my-2" />
                )}
                <div className="space-y-1">
                  {sec.items.map((item) => {
                    const Icon = item.icon;
                    const isActive = currentPath.startsWith(item.path);
                    return (
                      <button
                        key={item.path}
                        onClick={() => onNavigate(item.path)}
                        className={`w-full flex items-center rounded-xl text-xs font-medium transition-all duration-200 group relative ${
                          collapsed ? 'justify-center p-2.5' : 'gap-3 px-3 py-2'
                        } ${
                          isActive
                            ? 'bg-[#FF6A00]/15 text-[#FFB15A] border border-[#FF6A00]/30 shadow-[0_0_12px_rgba(255,106,0,0.15)] font-semibold'
                            : 'text-[#A89D92] hover:text-[#F5F0EA] hover:bg-[#FF6A00]/06'
                        }`}
                        title={collapsed ? item.label : undefined}
                      >
                        <Icon
                          className={`w-4 h-4 shrink-0 transition-colors ${
                            isActive ? 'text-[#FF6A00]' : 'text-[#6F665F] group-hover:text-[#FF8A24]'
                          }`}
                        />
                        {!collapsed && <span className="truncate">{item.label}</span>}
                        {isActive && !collapsed && (
                          <span className="ml-auto w-1.5 h-1.5 rounded-full bg-[#FF6A00] shadow-[0_0_6px_#FF6A00]" />
                        )}
                        {isActive && collapsed && (
                          <span className="absolute right-1 top-1 w-1.5 h-1.5 rounded-full bg-[#FF6A00] shadow-[0_0_6px_#FF6A00]" />
                        )}
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer Org info */}
        <div className="p-2.5 border-t border-[#FF6A00]/14">
          <div
            onClick={() => onNavigate('/settings/organization')}
            className={`rounded-xl bg-[#120C08] border border-[#FF6A00]/15 flex items-center cursor-pointer hover:border-[#FF6A00]/40 transition-colors ${
              collapsed ? 'justify-center p-2' : 'gap-3 p-2.5'
            }`}
            title="PrimeLogix Enterprise"
          >
            <div className="w-8 h-8 rounded-lg bg-[#FF6A00]/20 border border-[#FF6A00]/30 flex items-center justify-center text-[#FF8A24] font-mono font-bold text-xs shrink-0">
              PL
            </div>
            {!collapsed && (
              <div className="flex flex-col min-w-0">
                <span className="text-xs font-semibold text-[#F5F0EA] truncate">PrimeLogix</span>
                <span className="text-[10px] font-mono text-[#A89D92]">Enterprise Tier</span>
              </div>
            )}
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
