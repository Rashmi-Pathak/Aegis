import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const custData = [
  { month: 'Q1 25', retention: 96.2, nrr: 118 },
  { month: 'Q2 25', retention: 95.8, nrr: 116 },
  { month: 'Q3 25', retention: 95.4, nrr: 114 },
  { month: 'Q4 25', retention: 96.0, nrr: 115 },
  { month: 'Q1 26', retention: 94.8, nrr: 112 },
];

export const CustomerTrendChart: React.FC<{ height?: number }> = ({ height = 260 }) => {
  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={custData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid stroke="rgba(255, 106, 0, 0.08)" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="month" stroke="#6F665F" fontSize={11} tickLine={false} />
          <YAxis stroke="#6F665F" fontSize={11} tickLine={false} domain={[90, 120]} />
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
          <Line type="monotone" dataKey="nrr" stroke="#FF8A24" strokeWidth={2.5} name="Net Revenue Retention (NRR %)" />
          <Line type="monotone" dataKey="retention" stroke="#FFB15A" strokeWidth={2} name="Logo Retention Rate %" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CustomerTrendChart;
