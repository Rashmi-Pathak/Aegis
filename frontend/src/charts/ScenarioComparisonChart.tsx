import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';

interface ScenarioComparisonChartProps {
  baselineRevenue?: number;
  simulatedRevenue?: number;
  baselineProfit?: number;
  simulatedProfit?: number;
  baselineCash?: number;
  simulatedCash?: number;
  height?: number;
}

export const ScenarioComparisonChart: React.FC<ScenarioComparisonChartProps> = ({
  baselineRevenue = 148.2,
  simulatedRevenue = 154.5,
  baselineProfit = 21.0,
  simulatedProfit = 24.8,
  baselineCash = 18.6,
  simulatedCash = 21.2,
  height = 280,
}) => {
  const data = [
    { metric: 'Revenue ($M)', Baseline: baselineRevenue, Scenario: simulatedRevenue },
    { metric: 'Operating Profit ($M)', Baseline: baselineProfit, Scenario: simulatedProfit },
    { metric: 'Free Cash Flow ($M)', Baseline: baselineCash, Scenario: simulatedCash },
  ];

  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 15, right: 15, left: -10, bottom: 0 }}>
          <CartesianGrid stroke="rgba(255, 106, 0, 0.08)" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="metric" stroke="#6F665F" fontSize={11} tickLine={false} />
          <YAxis stroke="#6F665F" fontSize={11} tickLine={false} tickFormatter={(v) => `$${v}M`} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#120C08',
              borderColor: 'rgba(255,106,0,0.3)',
              borderRadius: '12px',
              color: '#F5F0EA',
              fontFamily: 'monospace',
              fontSize: '12px',
            }}
          />
          <Legend
            verticalAlign="top"
            height={36}
            formatter={(value) => <span className="text-xs text-[#A89D92] font-mono">{value}</span>}
          />
          <Bar dataKey="Baseline" fill="#6F665F" radius={[4, 4, 0, 0]} />
          <Bar dataKey="Scenario" fill="#FF6A00" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ScenarioComparisonChart;
