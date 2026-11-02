import React from 'react';
import { LineChart, Line, ResponsiveContainer } from 'recharts';

interface KPITrendChartProps {
  data?: number[];
  color?: string;
  height?: number;
}

export const KPITrendChart: React.FC<KPITrendChartProps> = ({
  data = [12, 14, 13, 16, 18, 17, 21, 24],
  color = '#FF6A00',
  height = 36,
}) => {
  const chartData = data.map((val, idx) => ({ idx, val }));

  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData} margin={{ top: 2, right: 2, left: 2, bottom: 2 }}>
          <Line
            type="monotone"
            dataKey="val"
            stroke={color}
            strokeWidth={1.8}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default KPITrendChart;
