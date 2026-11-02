import React from 'react';

interface SectionHeaderProps {
  badge?: string;
  title: string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
}

export const SectionHeader: React.FC<SectionHeaderProps> = ({
  badge,
  title,
  description,
  action,
  className = '',
}) => {
  return (
    <div className={`flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-6 ${className}`}>
      <div>
        {badge && (
          <span className="inline-block text-[10px] font-mono uppercase tracking-widest text-[#FF8A24] font-semibold mb-1">
            {badge}
          </span>
        )}
        <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-[#F5F0EA]">{title}</h2>
        {description && <p className="text-xs sm:text-sm text-[#A89D92] mt-1 max-w-2xl">{description}</p>}
      </div>
      {action && <div className="shrink-0">{action}</div>}
    </div>
  );
};

export default SectionHeader;
