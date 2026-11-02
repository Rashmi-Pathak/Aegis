import React from 'react';
import AppShell from '@/components/AppShell';
import { AlertItem } from '@/types';

interface AppLayoutProps {
  children: React.ReactNode;
  currentPath: string;
  onNavigate: (path: string) => void;
  activeBusinessId?: string;
  onSelectBusiness?: (id: string) => void;
  alerts?: AlertItem[];
}

export const AppLayout: React.FC<AppLayoutProps> = ({
  children,
  currentPath,
  onNavigate,
  activeBusinessId,
  onSelectBusiness,
  alerts,
}) => {
  return (
    <AppShell
      currentPath={currentPath}
      onNavigate={onNavigate}
      activeBusinessId={activeBusinessId}
      onSelectBusiness={onSelectBusiness}
      alerts={alerts}
    >
      {children}
    </AppShell>
  );
};

export const AdminLayout = AppLayout;
export default AppLayout;
