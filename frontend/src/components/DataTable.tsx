import React from 'react';

export interface Column<T> {
  key: string;
  header: string;
  render?: (item: T) => React.ReactNode;
  align?: 'left' | 'center' | 'right';
  className?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyExtractor: (item: T) => string;
  onRowClick?: (item: T) => void;
  emptyMessage?: string;
  className?: string;
}

export function DataTable<T>({
  columns,
  data,
  keyExtractor,
  onRowClick,
  emptyMessage = 'No records found',
  className = '',
}: DataTableProps<T>) {
  return (
    <div className={`overflow-x-auto rounded-xl border border-[#FF6A00]/16 bg-[#120C08]/75 backdrop-blur-md ${className}`}>
      <table className="w-full text-left text-sm">
        <thead className="border-b border-[#FF6A00]/16 bg-[#17100B]/80 text-xs uppercase tracking-wider text-[#A89D92] font-mono">
          <tr>
            {columns.map((col) => (
              <th
                key={col.key}
                className={`px-5 py-3.5 font-medium ${
                  col.align === 'right' ? 'text-right' : col.align === 'center' ? 'text-center' : 'text-left'
                } ${col.className || ''}`}
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-[#FF6A00]/10 text-xs">
          {data.length === 0 ? (
            <tr>
              <td colSpan={columns.length} className="px-5 py-8 text-center text-[#6F665F] font-mono">
                {emptyMessage}
              </td>
            </tr>
          ) : (
            data.map((item) => (
              <tr
                key={keyExtractor(item)}
                onClick={() => onRowClick?.(item)}
                className={`transition-colors duration-150 hover:bg-[#FF6A00]/06 ${
                  onRowClick ? 'cursor-pointer' : ''
                }`}
              >
                {columns.map((col) => (
                  <td
                    key={col.key}
                    className={`px-5 py-3 text-[#F5F0EA] ${
                      col.align === 'right' ? 'text-right' : col.align === 'center' ? 'text-center' : 'text-left'
                    } ${col.className || ''}`}
                  >
                    {col.render ? col.render(item) : (item as any)[col.key]}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default DataTable;
