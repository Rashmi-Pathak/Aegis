import React, { useState, useEffect } from 'react';
import LandingPage from '@/pages/landing/LandingPage';
import HowAegisWorksPage from '@/pages/landing/HowAegisWorksPage';
import DocumentationPage from '@/pages/landing/DocumentationPage';
import RequestDemoPage from '@/pages/landing/RequestDemoPage';
import LoginPage from '@/pages/auth/LoginPage';
import SignupPage from '@/pages/auth/SignupPage';
import ForgotPasswordPage from '@/pages/auth/ForgotPasswordPage';
import OrganizationSetupPage from '@/pages/onboarding/OrganizationSetupPage';
import DataUploadPage from '@/pages/onboarding/DataUploadPage';
import DataProcessingPage from '@/pages/onboarding/DataProcessingPage';
import DemoSelectorPage from '@/pages/demo/DemoSelectorPage';
import ExecutiveCommandCenterPage from '@/pages/command-center/ExecutiveCommandCenterPage';
import AnalyticsPage from '@/pages/analytics/AnalyticsPage';
import RevenuePage from '@/pages/analytics/RevenuePage';
import CustomersPage from '@/pages/analytics/CustomersPage';
import InventoryPage from '@/pages/analytics/InventoryPage';
import FinancePage from '@/pages/analytics/FinancePage';
import MarketingPage from '@/pages/analytics/MarketingPage';
import ForecastCenterPage from '@/pages/forecast-center/ForecastCenterPage';
import RiskCenterPage from '@/pages/risk-center/RiskCenterPage';
import RiskDetailPage from '@/pages/risk-center/RiskDetailPage';
import InvestigationWorkspacePage from '@/pages/investigation/InvestigationWorkspacePage';
import DecisionCenterPage from '@/pages/decision-center/DecisionCenterPage';
import WhatIfSimulationPage from '@/pages/simulation/WhatIfSimulationPage';
import BusinessGraphPage from '@/pages/business-graph/BusinessGraphPage';
import DataCenterPage from '@/pages/data-center/DataCenterPage';
import ModelIntelligencePage from '@/pages/models/ModelIntelligencePage';
import ReportCenterPage from '@/pages/reports/ReportCenterPage';
import AlertCenterPage from '@/pages/alerts/AlertCenterPage';
import SettingsPage from '@/pages/settings/SettingsPage';
import AdminSystemHealthPage from '@/pages/admin/AdminSystemHealthPage';

import PublicLayout from '@/layouts/PublicLayout';
import AuthLayout from '@/layouts/AuthLayout';
import AppLayout from '@/layouts/AppLayout';
import { alertApi } from '@/api/alertApi';
import { AlertItem } from '@/types';

export const Router: React.FC = () => {
  // Hash-based / Path-based SPA routing
  const [currentPath, setCurrentPath] = useState<string>(
    window.location.pathname === '/' && window.location.hash
      ? window.location.hash.replace('#', '')
      : window.location.pathname || '/'
  );

  const [activeBusinessId, setActiveBusinessId] = useState<string>('primelogix');
  const [alerts, setAlerts] = useState<AlertItem[]>([]);

  useEffect(() => {
    alertApi.getAlerts().then(setAlerts);

    const handleLocationChange = () => {
      const path =
        window.location.pathname === '/' && window.location.hash
          ? window.location.hash.replace('#', '')
          : window.location.pathname;
      setCurrentPath(path || '/');
      window.scrollTo(0, 0);
    };

    window.addEventListener('popstate', handleLocationChange);
    window.addEventListener('hashchange', handleLocationChange);
    return () => {
      window.removeEventListener('popstate', handleLocationChange);
      window.removeEventListener('hashchange', handleLocationChange);
    };
  }, []);

  const navigate = (path: string) => {
    window.history.pushState({}, '', path);
    setCurrentPath(path);
    window.scrollTo(0, 0);
  };

  const selectBusiness = (id: string) => {
    setActiveBusinessId(id);
    localStorage.setItem('aegis_active_business_id', id);
  };

  // 1. Public Landing Pages
  if (currentPath === '/') {
    return (
      <PublicLayout>
        <LandingPage onNavigate={navigate} />
      </PublicLayout>
    );
  }

  if (currentPath === '/how-it-works') {
    return (
      <PublicLayout>
        <HowAegisWorksPage onNavigate={navigate} />
      </PublicLayout>
    );
  }

  if (currentPath === '/docs') {
    return (
      <PublicLayout>
        <DocumentationPage onNavigate={navigate} />
      </PublicLayout>
    );
  }

  if (currentPath === '/request-demo') {
    return (
      <PublicLayout>
        <RequestDemoPage onNavigate={navigate} />
      </PublicLayout>
    );
  }

  // 2. Auth Pages
  if (currentPath === '/login') {
    return (
      <AuthLayout>
        <LoginPage onNavigate={navigate} />
      </AuthLayout>
    );
  }

  if (currentPath === '/signup') {
    return (
      <AuthLayout>
        <SignupPage onNavigate={navigate} />
      </AuthLayout>
    );
  }

  if (currentPath === '/forgot-password') {
    return (
      <AuthLayout>
        <ForgotPasswordPage onNavigate={navigate} />
      </AuthLayout>
    );
  }

  // 3. Onboarding Flow
  if (currentPath === '/onboarding/organization') {
    return <OrganizationSetupPage onNavigate={navigate} />;
  }

  if (currentPath === '/onboarding/upload') {
    return <DataUploadPage onNavigate={navigate} />;
  }

  if (currentPath === '/onboarding/processing') {
    return <DataProcessingPage onNavigate={navigate} />;
  }

  // 4. Demo Business Selector
  if (currentPath === '/demo') {
    return (
      <PublicLayout>
        <DemoSelectorPage onNavigate={navigate} onSelectBusiness={selectBusiness} />
      </PublicLayout>
    );
  }

  // 5. Authenticated App Pages (Wrapped in AppLayout & AppShell)
  const renderAppContent = () => {
    switch (currentPath) {
      case '/command-center':
      case '/dashboard':
        return (
          <ExecutiveCommandCenterPage
            onNavigate={navigate}
            activeBusinessId={activeBusinessId}
          />
        );

      case '/analytics':
        return <AnalyticsPage onNavigate={navigate} />;
      case '/analytics/revenue':
        return <RevenuePage onNavigate={navigate} />;
      case '/analytics/customers':
        return <CustomersPage onNavigate={navigate} />;
      case '/analytics/inventory':
        return <InventoryPage onNavigate={navigate} />;
      case '/analytics/finance':
        return <FinancePage onNavigate={navigate} />;
      case '/analytics/marketing':
        return <MarketingPage onNavigate={navigate} />;

      case '/forecast-center':
        return <ForecastCenterPage onNavigate={navigate} />;

      case '/risk-center':
        return <RiskCenterPage onNavigate={navigate} />;
      case '/risk-center/detail':
        return <RiskDetailPage onNavigate={navigate} />;

      case '/investigation':
        return <InvestigationWorkspacePage onNavigate={navigate} />;

      case '/decision-center':
        return <DecisionCenterPage onNavigate={navigate} />;

      case '/simulation':
        return <WhatIfSimulationPage onNavigate={navigate} />;

      case '/business-graph':
        return <BusinessGraphPage onNavigate={navigate} />;

      case '/data-center':
        return <DataCenterPage onNavigate={navigate} />;

      case '/models':
        return <ModelIntelligencePage onNavigate={navigate} />;

      case '/reports':
        return <ReportCenterPage onNavigate={navigate} />;

      case '/alerts':
      case '/anomalies':
        return <AlertCenterPage onNavigate={navigate} />;

      case '/settings':
      case '/settings/organization':
        return <SettingsPage onNavigate={navigate} />;

      case '/admin':
        return <AdminSystemHealthPage onNavigate={navigate} />;

      default:
        return (
          <ExecutiveCommandCenterPage
            onNavigate={navigate}
            activeBusinessId={activeBusinessId}
          />
        );
    }
  };

  return (
    <AppLayout
      currentPath={currentPath}
      onNavigate={navigate}
      activeBusinessId={activeBusinessId}
      onSelectBusiness={selectBusiness}
      alerts={alerts}
    >
      {renderAppContent()}
    </AppLayout>
  );
};

export default Router;
