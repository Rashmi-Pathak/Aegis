import React from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';

interface ContributionItem {
  name: string;
  value: number;
}

const defaultData: ContributionItem[] = [
  { name: 'Freight Haulage', value: 48 },
  { name: 'Warehousing & 3PL', value: 24 },
  { name: 'Cold-Chain Logistics', value: 18 },
  { name: 'Customs Brokerage', value: 10 },
];

const COLORS = ['#FF6A00', '#FF8A24', '#FFB15A', '#A89D92'];

export const ContributionChart: React.FC<{ data?: ContributionItem[]; height?: number }> = ({
  data = defaultData,
  height = 240,
}) => {
  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={55}
            outerRadius={80}
            paddingAngle={4}
            dataKey="value"
          >
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: '#120C08',
              borderColor: 'rgba(255,106,0,0.3)',
              borderRadius: '8px',
              color: '#F5F0EA',
              fontFamily: 'monospace',
              fontSize: '12px',
            }}
            formatter={(value: any) => [`${value}%`, 'Contribution']}
          />
          <Legend
            verticalAlign="bottom"
            height={36}
            formatter={(value) => <span className="text-xs text-[#A89D92] font-mono">{value}</span>}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ContributionChart;
