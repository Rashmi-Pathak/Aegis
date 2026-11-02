import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const data = [
  { month: 'Sep', utilization: 88, deadstock: 4.2 },
  { month: 'Oct', utilization: 86, deadstock: 4.8 },
  { month: 'Nov', utilization: 85, deadstock: 5.4 },
  { month: 'Dec', utilization: 92, deadstock: 3.9 },
  { month: 'Jan', utilization: 84, deadstock: 6.8 },
  { month: 'Feb', utilization: 82, deadstock: 7.4 },
  { month: 'Mar', utilization: 84, deadstock: 6.9 },
];

export const InventoryTrendChart: React.FC<{ height?: number }> = ({ height = 260 }) => {
  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid stroke="rgba(255, 106, 0, 0.08)" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="month" stroke="#6F665F" fontSize={11} tickLine={false} />
          <YAxis stroke="#6F665F" fontSize={11} tickLine={false} tickFormatter={(v) => `${v}%`} />
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
          <Area type="monotone" dataKey="utilization" stroke="#FF6A00" strokeWidth={2} fill="rgba(255,106,0,0.2)" name="Fleet Asset Utilization %" />
          <Area type="monotone" dataKey="deadstock" stroke="#FF4500" strokeWidth={1.5} fill="rgba(255,69,0,0.15)" name="Idle / Dwell Rate %" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default InventoryTrendChart;
