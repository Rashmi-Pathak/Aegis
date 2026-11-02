import apiClient from './client';
import { RiskItem, AnomalyItem } from '@/types';

export const riskApi = {
  async getRisks(): Promise<RiskItem[]> {
    try {
      return await apiClient<RiskItem[]>('/risks');
    } catch {
      return [
        {
          id: 'rsk_fuel_surge',
          title: 'Diesel Benchmark Spike & Spot Rate Squeeze',
          category: 'financial',
          severity: 'critical',
          score: 88,
          probability: 0.86,
          impact: 92,
          exposureAmount: '$2.85M',
          detectedAt: '2026-03-02 09:14 UTC',
          status: 'active',
          primaryDrivers: ['Global Crude Benchmark +18%', 'Carrier Spot Surcharges', 'Fixed Long-Term Shipper Contracts'],
          secondaryDrivers: ['Refinery Maintenance Closures', 'Port Terminal Truck Idling'],
          affectedAreas: ['Gross Margin', 'Short-Term Working Capital', 'OTIF Compliance'],
          recommendedActions: [
            'Trigger Dynamic Fuel Surcharge Clause B-14',
            'Reroute 24% of mid-haul corridors to intermodal rail',
            'Lock 60-day heating oil hedging contracts for 350k gallons',
          ],
        },
        {
          id: 'rsk_port_dwell',
          title: 'Rotterdam & Long Beach Port Dwell Congestion',
          category: 'operational',
          severity: 'high',
          score: 74,
          probability: 0.72,
          impact: 78,
          exposureAmount: '$1.42M',
          detectedAt: '2026-03-01 16:30 UTC',
          status: 'investigating',
          primaryDrivers: ['Customs Clearance Labor Shortage', 'Chassis Availability Deficit'],
          secondaryDrivers: ['Rail Hub Storage Saturation'],
          affectedAreas: ['Container Demurrage Fees', 'Turnaround Time', 'Chassis Rental Fees'],
          recommendedActions: [
            'Divert 18 inbound vessels to secondary terminals in Oakland & Antwerp',
            'Pre-clear customs documentation via digital EDI automated gate check',
          ],
        },
        {
          id: 'rsk_driver_attrition',
          title: 'Class-A Commercial Driver Turnaround Anomaly',
          category: 'operational',
          severity: 'medium',
          score: 58,
          probability: 0.61,
          impact: 64,
          exposureAmount: '$780K',
          detectedAt: '2026-02-28 11:20 UTC',
          status: 'active',
          primaryDrivers: ['Competitive Sign-on Bonuses from Regional Couriers', 'Night-Shift Route Fatigue'],
          secondaryDrivers: ['Vehicle Telemetry Ergonomics Feedback'],
          affectedAreas: ['Fleet Active Utilization', 'Recruiting & Onboarding Cost'],
          recommendedActions: [
            'Adjust milestone incentive pay by 4.2% on long-haul routes',
            'Introduce hybrid 4-day rotating dispatch schedule',
          ],
        },
        {
          id: 'rsk_cold_spoilage',
          title: 'Cold-Chain Pharma Sensor Telemetry Drift',
          category: 'supply_chain',
          severity: 'low',
          score: 34,
          probability: 0.28,
          impact: 85,
          exposureAmount: '$340K',
          detectedAt: '2026-02-26 14:05 UTC',
          status: 'mitigated',
          primaryDrivers: ['Trailer Unit #418 Sensor Calibration Lag'],
          secondaryDrivers: ['Ambient Summer Transit Window'],
          affectedAreas: ['Pharma Batch Compliance', 'Insurance Claims'],
          recommendedActions: [
            'Re-calibrate sensor firmware over-the-air and dispatch depot inspection',
          ],
        },
      ];
    }
  },

  async getRiskDetail(id: string): Promise<RiskItem> {
    const risks = await this.getRisks();
    const match = risks.find((r) => r.id === id);
    return match || risks[0];
  },
};

export const anomalyApi = {
  async getAnomalies(): Promise<AnomalyItem[]> {
    try {
      return await apiClient<AnomalyItem[]>('/anomalies');
    } catch {
      return [
        {
          id: 'anom_01',
          metric: 'Fuel Expense per Mile (Diesel TL)',
          detectedAt: '24m ago',
          severity: 'critical',
          deviationScore: 3.84, // Sigma
          expectedValue: '$0.58 / mi',
          actualValue: '$0.84 / mi',
          explanation: 'Station pump rate spike detected across Gulf Coast corridor combined with extended idling in Houston depot.',
          rootCauseCandidate: 'Terminal Congestion + Uncontracted Fuel Stops',
        },
        {
          id: 'anom_02',
          metric: 'Port Container Demurrage Accumulation',
          detectedAt: '2h ago',
          severity: 'high',
          deviationScore: 2.95,
          expectedValue: '$4,200 / day',
          actualValue: '$18,600 / day',
          explanation: 'Long Beach Terminal 4 chassis shortage causing container release holds exceeding 72h contract limit.',
          rootCauseCandidate: 'Intermodal Chassis Scarcity',
        },
        {
          id: 'anom_03',
          metric: 'Tier-1 Customer Order Cancellation Rate',
          detectedAt: '5h ago',
          severity: 'medium',
          deviationScore: 2.15,
          expectedValue: '1.2%',
          actualValue: '3.7%',
          explanation: 'Customer #4018 cancelled 14 consolidated loads following reported border crossing inspection delays.',
          rootCauseCandidate: 'Customs Transit Delay Cascade',
        },
      ];
    }
  },
};

export default riskApi;
