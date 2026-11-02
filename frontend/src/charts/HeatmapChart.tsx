import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, ZAxis, Tooltip, ResponsiveContainer, Cell, CartesianGrid } from 'recharts';
import { RiskItem } from '@/types';

interface HeatmapChartProps {
  risks?: RiskItem[];
  onSelectRisk?: (risk: RiskItem) => void;
  height?: number;
}

const defaultRisks: RiskItem[] = [
  { id: '1', title: 'Diesel Benchmark Surge', category: 'financial', severity: 'critical', score: 88, probability: 0.86, impact: 92, exposureAmount: '$2.85M', detectedAt: 'Today', status: 'active', primaryDrivers: [], secondaryDrivers: [], affectedAreas: [], recommendedActions: [] },
  { id: '2', title: 'Port Congestion Dwell', category: 'operational', severity: 'high', score: 74, probability: 0.72, impact: 78, exposureAmount: '$1.42M', detectedAt: 'Yesterday', status: 'active', primaryDrivers: [], secondaryDrivers: [], affectedAreas: [], recommendedActions: [] },
  { id: '3', title: 'Driver Turnover Anomaly', category: 'operational', severity: 'medium', score: 58, probability: 0.61, impact: 64, exposureAmount: '$780K', detectedAt: '3d ago', status: 'active', primaryDrivers: [], secondaryDrivers: [], affectedAreas: [], recommendedActions: [] },
  { id: '4', title: 'Cold-Chain Sensor Drift', category: 'supply_chain', severity: 'low', score: 34, probability: 0.28, impact: 85, exposureAmount: '$340K', detectedAt: '5d ago', status: 'mitigated', primaryDrivers: [], secondaryDrivers: [], affectedAreas: [], recommendedActions: [] },
];

export const HeatmapChart: React.FC<HeatmapChartProps> = ({
  risks = defaultRisks,
  onSelectRisk,
  height = 320,
}) => {
  const chartData = risks.map((r) => ({
    name: r.title,
    x: Math.round(r.probability * 100),
    y: r.impact,
    z: r.score,
    severity: r.severity,
    exposure: r.exposureAmount,
    riskObj: r,
  }));

  const getColor = (sev: string) => {
    switch (sev) {
      case 'critical':
        return '#FF4500';
      case 'high':
        return '#FF6A00';
      case 'medium':
        return '#FFB15A';
      default:
        return '#A89D92';
    }
  };

  return (
    <div style={{ height }} className="w-full relative">
      <ResponsiveContainer width="100%" height="100%">
        <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 0 }}>
          <CartesianGrid stroke="rgba(255, 106, 0, 0.08)" strokeDasharray="3 3" />
          <XAxis
            type="number"
            dataKey="x"
            name="Probability"
            unit="%"
            domain={[0, 100]}
            stroke="#6F665F"
            fontSize={11}
            tickLine={false}
          />
          <YAxis
            type="number"
            dataKey="y"
            name="Impact Severity"
            domain={[0, 100]}
            stroke="#6F665F"
            fontSize={11}
            tickLine={false}
          />
          <ZAxis type="number" dataKey="z" range={[80, 400]} />
          <Tooltip
            cursor={{ strokeDasharray: '3 3' }}
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const data = payload[0].payload;
                return (
                  <div className="p-3 bg-[#120C08] border border-[#FF6A00]/40 rounded-xl shadow-lg text-xs font-mono space-y-1">
                    <p className="font-bold text-[#F5F0EA]">{data.name}</p>
                    <p className="text-[#FF8A24]">Exposure: {data.exposure}</p>
                    <p className="text-[#A89D92]">Probability: {data.x}% • Impact: {data.y}</p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Scatter
            name="Risks"
            data={chartData}
            onClick={(e) => onSelectRisk?.(e.riskObj)}
            cursor="pointer"
          >
            {chartData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={getColor(entry.severity)}
                stroke="#FFB15A"
                strokeWidth={1}
                className="hover:opacity-80 transition-opacity"
              />
            ))}
          </Scatter>
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
};

export default HeatmapChart;
