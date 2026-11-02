import React from 'react';
import { ChevronRight, Home } from 'lucide-react';

interface BreadcrumbItem {
  label: string;
  path?: string;
}

interface BreadcrumbsProps {
  items: BreadcrumbItem[];
  onNavigate?: (path: string) => void;
  className?: string;
}

export const Breadcrumbs: React.FC<BreadcrumbsProps> = ({
  items,
  onNavigate,
  className = '',
}) => {
  return (
    <nav className={`flex items-center gap-1.5 text-xs font-mono text-[#A89D92] ${className}`}>
      <button
        onClick={() => onNavigate?.('/command-center')}
        className="hover:text-[#FFB15A] transition-colors p-1"
      >
        <Home className="w-3.5 h-3.5" />
      </button>
      {items.map((item, idx) => (
        <React.Fragment key={idx}>
          <ChevronRight className="w-3.5 h-3.5 text-[#6F665F]" />
          {item.path ? (
            <button
              onClick={() => onNavigate?.(item.path!)}
              className="hover:text-[#FFB15A] transition-colors font-medium"
            >
              {item.label}
            </button>
          ) : (
            <span className="text-[#F5F0EA] font-semibold">{item.label}</span>
          )}
        </React.Fragment>
      ))}
    </nav>
  );
};

export default Breadcrumbs;
