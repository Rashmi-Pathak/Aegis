import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts';

const waterfallData = [
  { name: 'Baseline Topline', delta: 148.2, fill: '#FF6A00' },
  { name: 'Carrier Rates', delta: 8.4, fill: '#FF8A24' },
  { name: 'Fuel Cost Surge', delta: -14.2, fill: '#FF4500' },
  { name: 'Port Demurrage', delta: -4.8, fill: '#FF4500' },
  { name: 'Volume Expansion', delta: 10.6, fill: '#FFB15A' },
  { name: 'Closing Revenue', delta: 148.2, fill: '#FF8A24' },
];

export const WaterfallChart: React.FC<{ height?: number }> = ({ height = 260 }) => {
  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={waterfallData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
          <CartesianGrid stroke="rgba(255, 106, 0, 0.08)" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="name" stroke="#6F665F" fontSize={10} tickLine={false} />
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
          <Bar dataKey="delta" radius={[4, 4, 0, 0]}>
            {waterfallData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.delta < 0 ? '#FF4500' : '#FF6A00'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default WaterfallChart;
