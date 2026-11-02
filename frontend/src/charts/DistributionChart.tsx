import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const distData = [
  { bin: '$0 - 50K', frequency: 45 },
  { bin: '$50K - 100K', frequency: 78 },
  { bin: '$100K - 250K', frequency: 120 },
  { bin: '$250K - 500K', frequency: 65 },
  { bin: '$500K - 1M', frequency: 32 },
  { bin: '$1M+', frequency: 14 },
];

export const DistributionChart: React.FC<{ height?: number }> = ({ height = 240 }) => {
  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={distData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid stroke="rgba(255, 106, 0, 0.08)" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="bin" stroke="#6F665F" fontSize={11} tickLine={false} />
          <YAxis stroke="#6F665F" fontSize={11} tickLine={false} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#120C08',
              borderColor: 'rgba(255,106,0,0.3)',
              borderRadius: '8px',
              color: '#F5F0EA',
              fontFamily: 'monospace',
              fontSize: '12px',
            }}
          />
          <Bar dataKey="frequency" fill="#FF8A24" radius={[4, 4, 0, 0]} name="Account Exposure Count" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default DistributionChart;
