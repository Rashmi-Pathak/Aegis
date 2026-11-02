import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts';

const riskTrendData = [
  { day: 'Day 1', financial: 42, operational: 55, supplyChain: 62 },
  { day: 'Day 5', financial: 48, operational: 58, supplyChain: 68 },
  { day: 'Day 10', financial: 65, operational: 62, supplyChain: 74 },
  { day: 'Day 15', financial: 82, operational: 70, supplyChain: 79 },
  { day: 'Day 20', financial: 88, operational: 74, supplyChain: 84 },
  { day: 'Day 25', financial: 85, operational: 72, supplyChain: 80 },
  { day: 'Day 30', financial: 78, operational: 68, supplyChain: 75 },
];

export const RiskTrendChart: React.FC<{ height?: number }> = ({ height = 280 }) => {
  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={riskTrendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid stroke="rgba(255, 106, 0, 0.08)" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="day" stroke="#6F665F" fontSize={11} tickLine={false} />
          <YAxis stroke="#6F665F" fontSize={11} tickLine={false} domain={[0, 100]} />
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
          <Line
            type="monotone"
            dataKey="financial"
            stroke="#FF6A00"
            strokeWidth={2.5}
            dot={{ fill: '#FF6A00', r: 3 }}
            name="Energy / Financial Exposure"
          />
          <Line
            type="monotone"
            dataKey="supplyChain"
            stroke="#FF8A24"
            strokeWidth={2}
            strokeDasharray="4 4"
            dot={{ fill: '#FF8A24', r: 3 }}
            name="Supply Chain Congestion"
          />
          <Line
            type="monotone"
            dataKey="operational"
            stroke="#A89D92"
            strokeWidth={1.5}
            dot={{ fill: '#A89D92', r: 2 }}
            name="Driver / Labor Variance"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RiskTrendChart;
