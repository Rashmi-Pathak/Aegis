import React, { useState } from 'react';
import {
  Search,
  Bell,
  ChevronDown,
  Building2,
  Command,
  Shield,
  Menu,
  PanelLeftClose,
  PanelLeftOpen,
} from 'lucide-react';
import StatusIndicator from '@/components/status/StatusIndicator';
import { DEMO_BUSINESSES } from '@/api/demoApi';

interface TopBarProps {
  onToggleSidebar?: () => void;
  onToggleCollapse?: () => void;
  isSidebarCollapsed?: boolean;
  onOpenCommandPalette?: () => void;
  onOpenNotifications?: () => void;
  onSelectBusiness?: (id: string) => void;
  activeBusinessId?: string;
  className?: string;
}

export const TopBar: React.FC<TopBarProps> = ({
  onToggleSidebar,
  onToggleCollapse,
  isSidebarCollapsed = false,
  onOpenCommandPalette,
  onOpenNotifications,
  onSelectBusiness,
  activeBusinessId = 'primelogix',
  className = '',
}) => {
  const [isOrgDropdownOpen, setIsOrgDropdownOpen] = useState(false);
  const activeBusiness =
    DEMO_BUSINESSES.find((b) => b.id.toLowerCase() === activeBusinessId.toLowerCase()) ||
    DEMO_BUSINESSES[0];

  return (
    <header
      className={`h-16 sticky top-0 bg-[#080604]/90 backdrop-blur-md border-b border-[#FF6A00]/14 px-3.5 sm:px-6 flex items-center justify-between z-20 transition-all ${className}`}
    >
      {/* Left: Mobile hamburger / Desktop sidebar toggle & Organization Selector */}
      <div className="flex items-center gap-2 sm:gap-3.5 min-w-0">
        {/* Mobile Hamburger Drawer Trigger (< lg) */}
        {onToggleSidebar && (
          <button
            onClick={onToggleSidebar}
            className="p-2 rounded-xl text-[#A89D92] hover:text-[#FFB15A] hover:bg-[#FF6A00]/10 border border-transparent hover:border-[#FF6A00]/20 transition-colors lg:hidden shrink-0"
            aria-label="Open mobile navigation"
            title="Open navigation"
          >
            <Menu className="w-5 h-5 text-[#FF8A24]" />
          </button>
        )}

        {/* Desktop Sidebar Width Toggle Button (>= lg) */}
        {onToggleCollapse && (
          <button
            onClick={onToggleCollapse}
            className="hidden lg:flex items-center gap-1.5 p-2 rounded-xl text-[#A89D92] hover:text-[#FFB15A] hover:bg-[#FF6A00]/10 border border-transparent hover:border-[#FF6A00]/20 transition-all shrink-0"
            title={isSidebarCollapsed ? 'Expand sidebar' : 'Shrink sidebar (wider analytics view)'}
            aria-label="Toggle sidebar collapse"
          >
            {isSidebarCollapsed ? (
              <PanelLeftOpen className="w-4 h-4 text-[#FF8A24]" />
            ) : (
              <PanelLeftClose className="w-4 h-4 text-[#A89D92]" />
            )}
            <span className="hidden xl:inline text-[11px] font-mono text-[#A89D92]">
              {isSidebarCollapsed ? 'Expand' : 'Shrink'}
            </span>
          </button>
        )}

        {/* Organization Switcher Dropdown */}
        <div className="relative">
          <button
            onClick={() => setIsOrgDropdownOpen(!isOrgDropdownOpen)}
            className="flex items-center gap-2 sm:gap-2.5 px-2.5 sm:px-3 py-1.5 rounded-xl bg-[#120C08] border border-[#FF6A00]/20 hover:border-[#FF6A00]/40 transition-colors text-xs font-mono max-w-[200px] sm:max-w-xs"
          >
            <Building2 className="w-3.5 h-3.5 text-[#FF6A00] shrink-0" />
            <span className="font-semibold text-[#F5F0EA] truncate">{activeBusiness.name}</span>
            <span className="text-[#6F665F] hidden sm:inline truncate">
              ({activeBusiness.industry.split(' ')[0]})
            </span>
            <ChevronDown className="w-3.5 h-3.5 text-[#A89D92] shrink-0" />
          </button>

          {isOrgDropdownOpen && (
            <>
              <div
                className="fixed inset-0 z-40"
                onClick={() => setIsOrgDropdownOpen(false)}
              />
              <div className="absolute left-0 mt-2 w-72 max-w-[calc(100vw-2rem)] rounded-2xl bg-[#120C08] border border-[#FF6A00]/30 shadow-[0_10px_35px_rgba(0,0,0,0.8)] p-2 z-50 max-h-96 overflow-y-auto">
                <div className="px-3 py-2 text-[10px] font-mono uppercase text-[#6F665F] font-semibold border-b border-[#FF6A00]/10 flex items-center justify-between">
                  <span>14 DEMO BUSINESSES</span>
                  <span className="text-[#FF8A24]">ACTIVE DB</span>
                </div>
                <div className="py-1 space-y-1">
                  {DEMO_BUSINESSES.map((b) => (
                    <button
                      key={b.id}
                      onClick={() => {
                        onSelectBusiness?.(b.id);
                        setIsOrgDropdownOpen(false);
                      }}
                      className={`w-full text-left px-3 py-2 rounded-xl text-xs flex items-center justify-between transition-colors ${
                        b.id === activeBusinessId
                          ? 'bg-[#FF6A00]/15 text-[#FFB15A] font-semibold'
                          : 'text-[#A89D92] hover:text-[#F5F0EA] hover:bg-[#FF6A00]/06'
                      }`}
                    >
                      <div className="min-w-0 pr-2">
                        <span className="block font-medium truncate">{b.name}</span>
                        <span className="text-[10px] text-[#6F665F] font-mono truncate block">
                          {b.industry}
                        </span>
                      </div>
                      <span className="text-[11px] font-mono text-[#FF8A24] shrink-0">
                        {b.healthScore} <span className="text-[9px] text-[#6F665F]">HLTH</span>
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-2 sm:gap-3.5">
        {/* Mobile Quick Search Button */}
        <button
          onClick={onOpenCommandPalette}
          className="md:hidden p-2 rounded-xl bg-[#0D0906] border border-[#FF6A00]/18 text-[#A89D92] hover:text-[#FF8A24] hover:border-[#FF6A00]/40 transition-colors"
          aria-label="Open search command palette"
        >
          <Search className="w-4 h-4 text-[#FF6A00]" />
        </button>

        {/* Desktop Command Search Trigger */}
        <button
          onClick={onOpenCommandPalette}
          className="hidden md:flex items-center gap-3 px-3 py-1.5 rounded-xl bg-[#0D0906] border border-[#FF6A00]/16 hover:border-[#FF6A00]/35 transition-colors text-xs text-[#A89D92] font-mono"
        >
          <Search className="w-3.5 h-3.5 text-[#FF6A00]" />
          <span className="hidden lg:inline">Quick search or command...</span>
          <span className="lg:hidden">Search...</span>
          <kbd className="px-1.5 py-0.5 rounded bg-[#17100B] text-[10px] text-[#FFB15A] border border-[#FF6A00]/20 flex items-center gap-0.5">
            <Command className="w-2.5 h-2.5" /> K
          </kbd>
        </button>

        {/* Telemetry Status Indicator */}
        <div className="hidden sm:block">
          <StatusIndicator status="operational" />
        </div>

        {/* Notifications Trigger */}
        <button
          onClick={onOpenNotifications}
          className="relative p-2 rounded-xl bg-[#120C08] border border-[#FF6A00]/18 text-[#A89D92] hover:text-[#F5F0EA] hover:border-[#FF6A00]/40 transition-colors"
          aria-label="Open notifications"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-[#FF6A00] shadow-[0_0_6px_#FF6A00]" />
        </button>

        {/* User Avatar */}
        <div className="flex items-center gap-2.5 pl-1.5 sm:pl-2 border-l border-[#FF6A00]/14">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-[#FF6A00] to-[#FFB15A] p-0.5 shadow-[0_0_10px_rgba(255,106,0,0.3)] shrink-0">
            <div className="w-full h-full rounded-[10px] bg-[#080604] flex items-center justify-center text-xs font-mono font-bold text-[#FFB15A]">
              CR
            </div>
          </div>
          <div className="hidden xl:flex flex-col text-left">
            <span className="text-xs font-semibold text-[#F5F0EA] leading-none">CRO / Operations</span>
            <span className="text-[10px] font-mono text-[#6F665F] mt-1">Autonomous Access</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default TopBar;
