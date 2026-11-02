import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, ReferenceLine } from 'recharts';

const cashData = [
  { month: 'Oct', operating: 6.8, investing: -2.1, financing: -1.4, net: 3.3 },
  { month: 'Nov', operating: 7.2, investing: -1.8, financing: -1.2, net: 4.2 },
  { month: 'Dec', operating: 8.5, investing: -3.2, financing: -1.5, net: 3.8 },
  { month: 'Jan', operating: 5.4, investing: -2.0, financing: -1.1, net: 2.3 },
  { month: 'Feb', operating: 5.9, investing: -1.5, financing: -1.0, net: 3.4 },
  { month: 'Mar', operating: 6.2, investing: -2.4, financing: -1.2, net: 2.6 },
];

export const CashFlowChart: React.FC<{ height?: number }> = ({ height = 260 }) => {
  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={cashData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid stroke="rgba(255, 106, 0, 0.08)" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="month" stroke="#6F665F" fontSize={11} tickLine={false} />
          <YAxis stroke="#6F665F" fontSize={11} tickLine={false} tickFormatter={(v) => `$${v}M`} />
          <ReferenceLine y={0} stroke="#FF6A00" strokeWidth={1} />
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
          <Bar dataKey="operating" fill="#FF6A00" radius={[4, 4, 0, 0]} name="Operating Inflow" />
          <Bar dataKey="investing" fill="#6F665F" radius={[0, 0, 4, 4]} name="CapEx / Investment" />
          <Bar dataKey="net" fill="#FFB15A" radius={[4, 4, 0, 0]} name="Net Free Cash Flow" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CashFlowChart;
