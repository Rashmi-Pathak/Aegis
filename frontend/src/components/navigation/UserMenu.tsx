import React, { useState } from 'react';
import { User, Settings, LogOut, Shield, ExternalLink } from 'lucide-react';

interface UserMenuProps {
  onNavigate?: (path: string) => void;
  onLogout?: () => void;
  className?: string;
}

export const UserMenu: React.FC<UserMenuProps> = ({
  onNavigate,
  onLogout,
  className = '',
}) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className={`relative ${className}`}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 p-1.5 rounded-xl hover:bg-[#FF6A00]/10 transition-colors"
      >
        <div className="w-8 h-8 rounded-lg bg-[#FF6A00]/20 border border-[#FF6A00]/40 flex items-center justify-center text-xs font-mono font-bold text-[#FFB15A]">
          EX
        </div>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 rounded-2xl bg-[#120C08] border border-[#FF6A00]/30 shadow-[0_15px_40px_rgba(0,0,0,0.8)] p-2 z-50 text-xs">
          <div className="px-3 py-2 border-b border-[#FF6A00]/12">
            <p className="font-semibold text-[#F5F0EA]">Chief Risk Officer</p>
            <p className="text-[10px] font-mono text-[#6F665F]">executive@aegis.ai</p>
          </div>
          <div className="py-1 space-y-0.5">
            <button
              onClick={() => {
                onNavigate?.('/settings');
                setIsOpen(false);
              }}
              className="w-full px-3 py-2 rounded-lg flex items-center gap-2.5 text-[#A89D92] hover:text-[#F5F0EA] hover:bg-[#FF6A00]/10"
            >
              <Settings className="w-3.5 h-3.5 text-[#FF6A00]" />
              <span>Platform Settings</span>
            </button>
            <button
              onClick={() => {
                onNavigate?.('/admin');
                setIsOpen(false);
              }}
              className="w-full px-3 py-2 rounded-lg flex items-center gap-2.5 text-[#A89D92] hover:text-[#F5F0EA] hover:bg-[#FF6A00]/10"
            >
              <Shield className="w-3.5 h-3.5 text-[#FF8A24]" />
              <span>Super Admin Console</span>
            </button>
          </div>
          <div className="pt-1 border-t border-[#FF6A00]/12">
            <button
              onClick={() => {
                onLogout?.();
                setIsOpen(false);
              }}
              className="w-full px-3 py-2 rounded-lg flex items-center gap-2.5 text-[#FF4500] hover:bg-[#FF4500]/10"
            >
              <LogOut className="w-3.5 h-3.5" />
              <span>Sign Out</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserMenu;
