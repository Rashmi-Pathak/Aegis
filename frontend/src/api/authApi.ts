import apiClient from './client';
import { User, Organization } from '@/types';

export interface LoginCredentials {
  email: string;
  password?: string;
}

export interface AuthResponse {
  token: string;
  user: User;
  organization: Organization;
}

export const authApi = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      return await apiClient<AuthResponse>('/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      });
    } catch {
      // Fallback seeded demo user response
      const demoUser: User = {
        id: 'usr_demo_01',
        name: 'Chief Risk & Operating Officer',
        email: credentials.email || 'executive@aegis.ai',
        role: 'executive',
        organizationId: 'org_primelogix',
        createdAt: new Date().toISOString(),
      };
      const demoOrg: Organization = {
        id: 'org_primelogix',
        name: 'PrimeLogix Global',
        slug: 'primelogix',
        industry: 'Freight & Global Logistics',
        tier: 'enterprise',
        healthScore: 78,
        dataQualityScore: 96,
        activeRisksCount: 4,
        createdAt: new Date().toISOString(),
      };
      return {
        token: 'aegis_jwt_demo_token',
        user: demoUser,
        organization: demoOrg,
      };
    }
  },

  async signup(data: any): Promise<AuthResponse> {
    try {
      return await apiClient<AuthResponse>('/auth/signup', {
        method: 'POST',
        body: JSON.stringify(data),
      });
    } catch {
      return this.login({ email: data.email });
    }
  },

  async requestDemoAccess(): Promise<AuthResponse> {
    // Authenticate into seeded demo mode
    return this.login({ email: 'demo@aegis.ai' });
  },

  logout() {
    localStorage.removeItem('aegis_auth_token');
    localStorage.removeItem('aegis_active_org_id');
  },
};

export default authApi;
