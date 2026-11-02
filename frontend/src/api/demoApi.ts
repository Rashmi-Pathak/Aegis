import apiClient from './client';
import { DemoBusiness } from '@/types';

export const DEMO_BUSINESSES: DemoBusiness[] = [
  {
    id: 'primelogix',
    name: 'PrimeLogix',
    industry: 'Freight & Global Logistics',
    tagline: 'Cross-border transport, fleet management & cold logistics',
    description: 'Autonomous freight fleet operating 1,200 heavy transport vehicles across North American and European corridors.',
    zipFileName: 'PrimeLogix_Aegis_Demo.zip',
    datasetCount: 8,
    recordCount: 428000,
    healthScore: 68,
    riskCount: 4,
    primaryRiskStory: {
      trigger: 'Surging diesel benchmarks (+28%) compounded by port customs dwell time',
      causalChain: ['Fuel Price Surge', 'Route Inefficiencies', 'Port Dwell Congestion', 'Contract SLA Penalties', 'Working Capital Compression'],
      affectedMetrics: ['Gross Operating Margin', 'On-Time In-Full Delivery (OTIF)', 'Fleet Fuel Burn Index', 'Fleet Utilization Rate'],
      potentialImpact: '$2.85M annualized margin erosion across Q3/Q4',
    },
    metrics: { revenue: '$148.2M', growth: '+8.4%', margin: '14.2%', runway: '18 mo' },
  },
  {
    id: 'novamart',
    name: 'NovaMart',
    industry: 'Omnichannel Superstores & Retail',
    tagline: '142 regional hypermarkets & e-commerce delivery',
    description: 'Retail powerhouse balancing perishable grocery lines, consumer electronics, and private label fast-moving goods.',
    zipFileName: 'NovaMart_Aegis_Demo.zip',
    datasetCount: 12,
    recordCount: 890000,
    healthScore: 74,
    riskCount: 3,
    primaryRiskStory: {
      trigger: 'Container import tariff revisions and central distribution center labor shortages',
      causalChain: ['Import Tariff Shock', 'Distribution Center Bottleneck', 'Stockouts in Tier-1 SKUs', 'Customer Defection to Competitors'],
      affectedMetrics: ['E-Commerce Same-Day Fill Rate', 'Gross Margin Return on Inventory', 'Customer Footfall'],
      potentialImpact: '$4.12M potential stockout revenue loss during promotional season',
    },
    metrics: { revenue: '$320.5M', growth: '+4.1%', margin: '22.8%', runway: '24 mo' },
  },
  {
    id: 'cloudnest',
    name: 'CloudNest',
    industry: 'B2B Enterprise SaaS & Cloud Infra',
    tagline: 'Developer platform & multi-cloud database orchestration',
    description: 'High-growth infrastructure provider serving 4,500 enterprise engineering teams globally.',
    zipFileName: 'CloudNest_Aegis_Demo.zip',
    datasetCount: 7,
    recordCount: 310000,
    healthScore: 82,
    riskCount: 2,
    primaryRiskStory: {
      trigger: 'Unoptimized GPU cluster inference cost inflation and contract renewals churn risk in Mid-Market',
      causalChain: ['Compute Infrastructure Cost Overruns', 'Mid-Market Renewal Friction', 'CAC Expansion', 'Net Revenue Retention Dip'],
      affectedMetrics: ['Net Revenue Retention (NRR)', 'Gross Margin per Core Hour', 'Customer Churn Probability'],
      potentialImpact: '$1.45M ARR exposure across expiring 2-year subscriptions',
    },
    metrics: { revenue: '$72.8M', growth: '+34.2%', margin: '71.5%', runway: '36 mo' },
  },
  {
    id: 'autocore',
    name: 'AutoCore',
    industry: 'Automotive OEM & EV Components',
    tagline: 'Powertrain assembly & battery pack tier-1 manufacturing',
    description: 'Precision manufacturing company supplying sub-assemblies and telemetry modules to EV automakers.',
    zipFileName: 'AutoCore_Aegis_Demo.zip',
    datasetCount: 9,
    recordCount: 540000,
    healthScore: 71,
    riskCount: 3,
    primaryRiskStory: {
      trigger: 'Critical lithium-cell supplier insolvency rumors and semiconductor batch defects',
      causalChain: ['Tier-2 Component Shortage', 'Assembly Line Idle Rate', 'OEM Late Penalty Trigger', 'Warranties & Rework Cost'],
      affectedMetrics: ['Overall Equipment Effectiveness (OEE)', 'Scrap Rate', 'Finished Goods Inventory'],
      potentialImpact: '$6.2M batch rework and OEM penalty liabilities',
    },
    metrics: { revenue: '$210.4M', growth: '+12.6%', margin: '16.4%', runway: '22 mo' },
  },
  {
    id: 'mediplus',
    name: 'MediPlus',
    industry: 'Healthcare Clinics & Diagnostic Centers',
    tagline: 'Integrated outpatient clinics and pathology laboratory network',
    description: 'Network of 86 ambulatory care centers providing radiology, general practice, and specialized oncology diagnosis.',
    zipFileName: 'MediPlus_Aegis_Demo.zip',
    datasetCount: 11,
    recordCount: 680000,
    healthScore: 79,
    riskCount: 2,
    primaryRiskStory: {
      trigger: 'Specialist clinical nurse turnover accelerating overtime compensation',
      causalChain: ['Staffing Shortage', 'Overtime Expenditure Spike', 'Patient Wait-Time Inflation', 'Patient Retention Decline'],
      affectedMetrics: ['Clinic Utilization', 'Staff Overtime Ratio', 'Patient Net Promoter Score'],
      potentialImpact: '$2.1M wage escalation and diagnostic imaging under-utilization',
    },
    metrics: { revenue: '$185.0M', growth: '+6.8%', margin: '19.2%', runway: '30 mo' },
  },
  {
    id: 'urbaneats',
    name: 'UrbanEats',
    industry: 'Food Delivery & Cloud Kitchens',
    tagline: 'Last-mile meal delivery and private brand ghost kitchens',
    description: 'Hyperlocal logistics and food preparation network serving 28 metropolitan areas with 15,000 active couriers.',
    zipFileName: 'UrbanEats_Aegis_Demo.zip',
    datasetCount: 8,
    recordCount: 920000,
    healthScore: 65,
    riskCount: 4,
    primaryRiskStory: {
      trigger: 'Courier incentives war and raw ingredient food cost volatility in dark kitchens',
      causalChain: ['Rider Acquisition Subsidy Spike', 'Ingredient Price Inflation', 'Order Cancellation Spikes', 'Contribution Margin Deficit'],
      affectedMetrics: ['Order Contribution Margin', 'Average Delivery Minutes', 'Courier Churn Rate'],
      potentialImpact: '$3.7M quarterly burn rate acceleration',
    },
    metrics: { revenue: '$94.6M', growth: '+21.5%', margin: '8.1%', runway: '14 mo' },
  },
  {
    id: 'buildright',
    name: 'BuildRight',
    industry: 'Commercial Construction & EPC',
    tagline: 'Infrastructure engineering, high-rise and industrial contracting',
    description: 'General engineering contractor managing 34 active projects across civil infrastructure and commercial hubs.',
    zipFileName: 'BuildRight_Aegis_Demo.zip',
    datasetCount: 6,
    recordCount: 290000,
    healthScore: 69,
    riskCount: 3,
    primaryRiskStory: {
      trigger: 'Structural steel delivery delays pushing milestone billings into subsequent fiscal year',
      causalChain: ['Subcontractor Delay', 'Equipment Demurrage Fees', 'Retainage Withholding', 'Cash Flow Deficit'],
      affectedMetrics: ['Project Completion Variance', 'Days Sales Outstanding (DSO)', 'Work-in-Progress (WIP) Cash'],
      potentialImpact: '$5.4M delayed milestone payments and contractual liquidated damages',
    },
    metrics: { revenue: '$280.0M', growth: '+5.3%', margin: '11.8%', runway: '16 mo' },
  },
  {
    id: 'stylesphere',
    name: 'StyleSphere',
    industry: 'Direct-to-Consumer Fashion & Apparel',
    tagline: 'Global fast-fashion e-commerce brand with automated fulfillment',
    description: 'Omnichannel fashion brand processing 45,000 orders weekly with automated European warehousing.',
    zipFileName: 'StyleSphere_Aegis_Demo.zip',
    datasetCount: 10,
    recordCount: 760000,
    healthScore: 73,
    riskCount: 3,
    primaryRiskStory: {
      trigger: 'High return rates (34%) on seasonal autumn apparel combined with deadstock buildup',
      causalChain: ['Fit Sizing Discrepancies', 'Surge in Reverse Logistics Costs', 'Warehouse Space Congestion', 'Aggressive Discounting Need'],
      affectedMetrics: ['Return Rate (%)', 'Reverse Logistics Cost per Unit', 'Inventory Holding Costs'],
      potentialImpact: '$3.2M margin erosion from salvage discounting',
    },
    metrics: { revenue: '$112.4M', growth: '+18.9%', margin: '28.4%', runway: '20 mo' },
  },
  {
    id: 'edutech_labs',
    name: 'EduTech Labs',
    industry: 'EdTech & Professional Certification LMS',
    tagline: 'Enterprise reskilling platform and technical micro-degrees',
    description: 'Online learning technology platform with 1.2M registered students and 350 university/corporate partnerships.',
    zipFileName: 'EduTech_Labs_Aegis_Demo.zip',
    datasetCount: 7,
    recordCount: 380000,
    healthScore: 84,
    riskCount: 1,
    primaryRiskStory: {
      trigger: 'B2B enterprise corporate budget freezes delaying seat renewals',
      causalChain: ['Corporate Training Budget Reductions', 'Delayed Multi-Year Renewals', 'Decreased Course Completion Velocity'],
      affectedMetrics: ['Net Revenue Retention', 'Enterprise Contract Value', 'Course Completion Ratio'],
      potentialImpact: '$1.1M in deferred recurring enterprise subscription revenue',
    },
    metrics: { revenue: '$48.5M', growth: '+26.0%', margin: '62.0%', runway: '40 mo' },
  },
  {
    id: 'greengrid',
    name: 'GreenGrid',
    industry: 'Renewable Power & Clean Grid Utilities',
    tagline: 'Solar/Wind distributed generation & battery energy storage system',
    description: 'Grid-scale clean power operator with 2.8 Gigawatt generation capacity and battery arbitrage systems.',
    zipFileName: 'GreenGrid_Aegis_Demo.zip',
    datasetCount: 9,
    recordCount: 810000,
    healthScore: 88,
    riskCount: 2,
    primaryRiskStory: {
      trigger: 'Inverter hardware degradation and grid curtailment during peak midday solar generation',
      causalChain: ['Inverter Temperature Spikes', 'Component Thermal Derating', 'Negative Spot Pricing Curtailment', 'Storage Cycling Fatigue'],
      affectedMetrics: ['Levelized Cost of Energy (LCOE)', 'Generation Availability Factor', 'Storage Round-Trip Efficiency'],
      potentialImpact: '$2.3M uncaptured power during merchant peak windows',
    },
    metrics: { revenue: '$164.0M', growth: '+15.2%', margin: '38.5%', runway: '32 mo' },
  },
  {
    id: 'finedge',
    name: 'FinEdge',
    industry: 'FinTech, Payments & SME Credit',
    tagline: 'Cross-border merchant acquiring and working capital credit facilities',
    description: 'Financial technology infrastructure processing $12B in annualized transactional volume with underwriting engines.',
    zipFileName: 'FinEdge_Aegis_Demo.zip',
    datasetCount: 12,
    recordCount: 1250000,
    healthScore: 76,
    riskCount: 3,
    primaryRiskStory: {
      trigger: 'Micro-merchant non-performing loan delinquency rate increase in retail sector',
      causalChain: ['Macro Consumer Discretionary Softening', 'Merchant Default Rate Rise', 'Provision for Credit Losses Expansion', 'Liquidity Facility Drawdown'],
      affectedMetrics: ['Non-Performing Loan (NPL) Ratio', 'Cost of Risk (bps)', 'Net Interest Margin (NIM)'],
      potentialImpact: '$4.8M provision requirement adjustment',
    },
    metrics: { revenue: '$135.8M', growth: '+29.4%', margin: '41.2%', runway: '28 mo' },
  },
  {
    id: 'freshkart',
    name: 'FreshKart',
    industry: 'Quick Commerce & Farm-to-Fork Grocery',
    tagline: '15-minute grocery dark stores and farm direct procurement',
    description: 'Rapid grocery network managing 180 micro-fulfillment centers with live cold-chain IoT tracking.',
    zipFileName: 'FreshKart_Aegis_Demo.zip',
    datasetCount: 10,
    recordCount: 980000,
    healthScore: 66,
    riskCount: 4,
    primaryRiskStory: {
      trigger: 'Refrigeration unit anomalies causing perishable dairy & produce shrinkage',
      causalChain: ['Cold Chain Sensor Telemetry Failures', 'Micro-fulfillment Spoilage Waste', 'Re-order Stockout Cascades', 'Local Customer Dissatisfaction'],
      affectedMetrics: ['Inventory Shrinkage Rate', 'Fresh Goods Spoilage Loss', 'Order Net Margin'],
      potentialImpact: '$1.9M product wastage and replenishment expedite fees',
    },
    metrics: { revenue: '$82.4M', growth: '+44.0%', margin: '9.4%', runway: '12 mo' },
  },
  {
    id: 'staysphere',
    name: 'StaySphere',
    industry: 'Hospitality, Boutique Hotels & Rentals',
    tagline: 'Tech-enabled boutique accommodations and extended stay residences',
    description: 'Hospitality brand managing 115 boutique residential properties and luxury urban apart-hotels.',
    zipFileName: 'StaySphere_Aegis_Demo.zip',
    datasetCount: 8,
    recordCount: 410000,
    healthScore: 80,
    riskCount: 2,
    primaryRiskStory: {
      trigger: 'Off-peak weekday occupancy drop offset by OTA aggregator commission fee hikes',
      causalChain: ['Corporate Travel Policy Restrictions', 'OTA Channel Dominance', 'Commission Margin Bleed', 'Fixed Lease Overhead Burden'],
      affectedMetrics: ['RevPAR (Revenue per Available Room)', 'Direct Booking Share', 'Operating Profit Margin'],
      potentialImpact: '$2.05M margin compression from OTA distribution fees',
    },
    metrics: { revenue: '$78.2M', growth: '+14.1%', margin: '24.0%', runway: '26 mo' },
  },
  {
    id: 'agronova',
    name: 'AgroNova',
    industry: 'AgriTech & Specialty Crop Logistics',
    tagline: 'Precision crop analytics, seed distribution and farm logistics',
    description: 'Agricultural inputs and yield optimization platform serving 8,000 commercial farms and grain elevators.',
    zipFileName: 'AgroNova_Aegis_Demo.zip',
    datasetCount: 9,
    recordCount: 520000,
    healthScore: 78,
    riskCount: 2,
    primaryRiskStory: {
      trigger: 'Prolonged regional drought conditions curtailing fertilizer and seed purchase timing',
      causalChain: ['Precipitation Deficit Anomaly', 'Farmer Credit Repayment Hesitancy', 'Deferred Chemical Pre-orders', 'Bulk Storage Carrying Costs'],
      affectedMetrics: ['Seasonal Pre-order Volume', 'Receivables Aging > 90 Days', 'Inventory Turnover Ratio'],
      potentialImpact: '$3.9M in deferred seasonal receivables and inventory storage costs',
    },
    metrics: { revenue: '$156.0M', growth: '+7.2%', margin: '21.5%', runway: '34 mo' },
  },
  {
    id: 'medsupplyx',
    name: 'MedSupplyX',
    industry: 'Medical Device & Surgical Distribution',
    tagline: 'Critical surgical instruments, sterile consumables & implant logistics',
    description: 'Specialized healthcare distributor delivering sterile surgical hardware to 420 hospital systems.',
    zipFileName: 'MedSupplyX_Aegis_Demo.zip',
    datasetCount: 9,
    recordCount: 470000,
    healthScore: 86,
    riskCount: 1,
    primaryRiskStory: {
      trigger: 'Regulatory lot traceability audit requirement demanding lot-level recalls validation',
      causalChain: ['Sterilization Documentation Discrepancy', 'Temporary Lot Quarantining', 'Consignment Hospital Restocking Delay'],
      affectedMetrics: ['Consignment Fill Rate', 'Lot Quarantine Holding Days', 'Compliance Safety Index'],
      potentialImpact: '$1.6M quarantined product inventory and compliance auditing expense',
    },
    metrics: { revenue: '$198.5M', growth: '+11.8%', margin: '31.2%', runway: '38 mo' },
  },
];

export const demoApi = {
  async getDemoBusinesses(): Promise<DemoBusiness[]> {
    try {
      return await apiClient<DemoBusiness[]>('/demo/businesses');
    } catch {
      // Clean fallback from seeded demo catalogue
      return DEMO_BUSINESSES;
    }
  },

  async getDemoBusiness(id: string): Promise<DemoBusiness> {
    try {
      return await apiClient<DemoBusiness>(`/demo/businesses/${id}`);
    } catch {
      const match = DEMO_BUSINESSES.find((b) => b.id.toLowerCase() === id.toLowerCase());
      if (match) return match;
      return DEMO_BUSINESSES[0];
    }
  },

  async getDemoOverview(id: string) {
    try {
      return await apiClient(`/demo/businesses/${id}/overview`);
    } catch {
      const b = await demoApi.getDemoBusiness(id);
      return {
        business: b,
        healthScore: b.healthScore,
        activeRisks: b.riskCount,
        forecastConfidence: 0.94,
        recentAnomalies: 3,
        systemStatus: 'OPERATIONAL',
      };
    }
  },
};

export default demoApi;
