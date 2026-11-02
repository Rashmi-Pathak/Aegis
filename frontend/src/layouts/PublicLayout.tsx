import React from 'react';
import GlobalNeonBackground from '@/backgrounds/GlobalNeonBackground';

interface PublicLayoutProps {
  children: React.ReactNode;
}

export const PublicLayout: React.FC<PublicLayoutProps> = ({ children }) => {
  return (
    <GlobalNeonBackground>
      {children}
    </GlobalNeonBackground>
  );
};

export default PublicLayout;
