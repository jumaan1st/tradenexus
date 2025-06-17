'use client';

import { createContext, useContext, useState } from 'react';

const GlobalContext = createContext();

export const GlobalProvider = ({ children }) => {
  const [currentPageTitle, setCurrentPageTitle] = useState('Dashboard');

  return (
    <GlobalContext.Provider value={{ currentPageTitle, setCurrentPageTitle }}>
      {children}
    </GlobalContext.Provider>
  );
};

export const useGlobalContext = () => useContext(GlobalContext);
