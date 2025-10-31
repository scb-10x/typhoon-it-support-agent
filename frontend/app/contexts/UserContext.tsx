"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";

interface UserInfo {
  employee_id: string;
  email: string;
  full_name_th: string;
  full_name_en: string;
  nickname: string;
  department: string;
  position: string;
  phone: string;
  office_location: string;
  manager: string;
  joined_date: string;
}

interface CompanyInfo {
  name_th: string;
  name_en: string;
  address_th: string;
  address_en: string;
  phone: string;
  website: string;
  industry: string;
  size: string;
}

interface UserSession {
  user: UserInfo | null;
  company: CompanyInfo | null;
  isLoading: boolean;
}

const UserContext = createContext<UserSession>({
  user: null,
  company: null,
  isLoading: true,
});

export const useUser = () => useContext(UserContext);

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function UserProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserInfo | null>(null);
  const [company, setCompany] = useState<CompanyInfo | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchUserSession = async () => {
      const response = await fetch(`${API_URL}/user/session`);
      if (response.ok) {
        const data = await response.json();
        setUser(data.user);
        setCompany(data.company);
      }
      setIsLoading(false);
    };

    fetchUserSession();
  }, []);

  return (
    <UserContext.Provider value={{ user, company, isLoading }}>
      {children}
    </UserContext.Provider>
  );
}


