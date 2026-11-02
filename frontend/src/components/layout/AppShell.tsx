import React, { useState, useEffect } from 'react';
import Sidebar from '../navigation/Sidebar';
import TopBar from '../navigation/TopBar';
import CommandPalette from '../navigation/CommandPalette';
import NotificationCenter from '../notifications/NotificationCenter';
import CommandCenterBackground from '@/backgrounds/CommandCenterBackground';
import { AlertItem } from '@/types';

interface AppShellProps {
  children: React.ReactNode;
  currentPath: string;
  onNavigate: (path: string) => void;
  activeBusinessId?: string;
  onSelectBusiness?: (id: string) => void;
  alerts?: AlertItem[];
}

export const AppShell: React.FC<AppShellProps> = ({
  children,
  currentPath,
  onNavigate,
  activeBusinessId = 'primelogix',
  onSelectBusiness,
  alerts = [],
}) => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState<boolean>(() => {
    try {
      return localStorage.getItem('aegis_sidebar_collapsed') === 'true';
    } catch {
      return false;
    }
  });
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);

  // Global keyboard shortcut Ctrl+B or Cmd+B to toggle sidebar collapse
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'b') {
        e.preventDefault();
        setSidebarCollapsed((prev) => {
          const next = !prev;
          try {
            localStorage.setItem('aegis_sidebar_collapsed', String(next));
          } catch {}
          return next;
        });
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleToggleCollapse = () => {
    setSidebarCollapsed((prev) => {
      const next = !prev;
      try {
        localStorage.setItem('aegis_sidebar_collapsed', String(next));
      } catch {}
      return next;
    });
  };

  return (
    <div className="relative min-h-screen bg-[#080604] text-[#F5F0EA] flex overflow-x-hidden selection:bg-[#FF6A00]/25 selection:text-[#FFB15A]">
      {/* Dynamic Telemetry & Background Grid */}
      <CommandCenterBackground />

      {/* Responsive Navigation Sidebar (Desktop + Mobile Drawer) */}
      <Sidebar
        currentPath={currentPath}
        onNavigate={(path) => {
          onNavigate(path);
          setMobileMenuOpen(false);
        }}
        collapsed={sidebarCollapsed}
        onToggleCollapse={handleToggleCollapse}
        isMobileOpen={mobileMenuOpen}
        onCloseMobile={() => setMobileMenuOpen(false)}
      />

      {/* Main Fluid Layout Workspace */}
      <div className="flex-1 flex flex-col min-w-0 z-10 transition-all duration-300 ease-in-out">
        <TopBar
          activeBusinessId={activeBusinessId}
          onSelectBusiness={onSelectBusiness}
          onToggleSidebar={() => setMobileMenuOpen(true)}
          onToggleCollapse={handleToggleCollapse}
          isSidebarCollapsed={sidebarCollapsed}
          onOpenCommandPalette={() => setCommandPaletteOpen(true)}
          onOpenNotifications={() => setNotificationsOpen(true)}
        />

        <main className="flex-1 p-3.5 sm:p-6 lg:p-8 w-full max-w-full mx-auto transition-all duration-300">
          {children}
        </main>
      </div>

      {/* Global Interactive Overlays */}
      <CommandPalette
        isOpen={commandPaletteOpen}
        onClose={() => setCommandPaletteOpen(false)}
        onNavigate={onNavigate}
      />

      <NotificationCenter
        isOpen={notificationsOpen}
        onClose={() => setNotificationsOpen(false)}
        alerts={alerts}
      />
    </div>
  );
};

export default AppShell;
