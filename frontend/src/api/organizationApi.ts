import apiClient from './client';
import { Organization } from '@/types';

export const organizationApi = {
  async getCurrentOrganization(): Promise<Organization> {
    try {
      return await apiClient<Organization>('/organizations/current');
    } catch {
      return {
        id: 'org_primelogix',
        name: 'PrimeLogix Global',
        slug: 'primelogix',
        industry: 'Freight & Global Logistics',
        tier: 'enterprise',
        healthScore: 78,
        dataQualityScore: 96,
        activeRisksCount: 4,
        createdAt: '2026-01-15T08:00:00Z',
      };
    }
  },

  async listOrganizations(): Promise<Organization[]> {
    try {
      return await apiClient<Organization[]>('/organizations');
    } catch {
      return [
        {
          id: 'org_primelogix',
          name: 'PrimeLogix Global',
          slug: 'primelogix',
          industry: 'Freight & Logistics',
          tier: 'enterprise',
          healthScore: 78,
          dataQualityScore: 96,
          activeRisksCount: 4,
          createdAt: '2026-01-15T08:00:00Z',
        },
        {
          id: 'org_novamart',
          name: 'NovaMart Superstores',
          slug: 'novamart',
          industry: 'Omnichannel Retail',
          tier: 'enterprise',
          healthScore: 74,
          dataQualityScore: 92,
          activeRisksCount: 3,
          createdAt: '2026-02-01T10:00:00Z',
        },
        {
          id: 'org_cloudnest',
          name: 'CloudNest Systems',
          slug: 'cloudnest',
          industry: 'Enterprise SaaS',
          tier: 'growth',
          healthScore: 82,
          dataQualityScore: 98,
          activeRisksCount: 2,
          createdAt: '2026-02-10T12:00:00Z',
        },
      ];
    }
  },
};

export default organizationApi;
