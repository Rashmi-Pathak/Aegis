import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts';

interface RevenueChartProps {
  data?: { date: string; actual: number; target: number }[];
  height?: number;
}

const defaultData = [
  { date: 'Oct 25', actual: 36.4, target: 35.0 },
  { date: 'Nov 25', actual: 39.8, target: 38.5 },
  { date: 'Dec 25', actual: 48.2, target: 45.0 },
  { date: 'Jan 26', actual: 41.5, target: 42.0 },
  { date: 'Feb 26', actual: 44.1, target: 44.5 },
  { date: 'Mar 26', actual: 48.2, target: 46.8 },
];

export const RevenueChart: React.FC<RevenueChartProps> = ({
  data = defaultData,
  height = 280,
}) => {
  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
          <defs>
            <linearGradient id="revActualGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#FF6A00" stopOpacity={0.45} />
              <stop offset="95%" stopColor="#FF6A00" stopOpacity={0.0} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke="rgba(255, 106, 0, 0.08)" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="date" stroke="#6F665F" fontSize={11} tickLine={false} />
          <YAxis
            stroke="#6F665F"
            fontSize={11}
            tickLine={false}
            tickFormatter={(v) => `$${v}M`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#120C08',
              borderColor: 'rgba(255,106,0,0.3)',
              borderRadius: '12px',
              color: '#F5F0EA',
              fontFamily: 'monospace',
              fontSize: '12px',
            }}
            formatter={(value: any) => [`$${value}M`, '']}
          />
          <Area
            type="monotone"
            dataKey="target"
            stroke="#6F665F"
            strokeWidth={1.5}
            strokeDasharray="4 4"
            fill="none"
            name="Plan Benchmark"
          />
          <Area
            type="monotone"
            dataKey="actual"
            stroke="#FF6A00"
            strokeWidth={2.5}
            fill="url(#revActualGrad)"
            name="Actual Revenue"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RevenueChart;
