import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';

const AuthContext = createContext(null);

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}

/**
 * DEMO-ONLY — plaintext credentials for local development / prototype review.
 * MUST be replaced with a backend authentication API (hashed passwords, JWT/session)
 * before any production or staging deployment.
 */
const CREDENTIALS = {
  admin: { password: 'admin123', role: 'admin', name: 'Admin' },
  investigator: { password: 'investor123', role: 'investigator', name: 'Investigator' },
};

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      const stored = localStorage.getItem('aduanflow_user');
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  });

  const login = useCallback((username, password) => {
    const cred = CREDENTIALS[username];
    if (!cred || cred.password !== password) return false;
    const userData = { username, role: cred.role, name: cred.name };
    setUser(userData);
    localStorage.setItem('aduanflow_user', JSON.stringify(userData));
    return true;
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    localStorage.removeItem('aduanflow_user');
  }, []);

  const isLoggedIn = !!user;

  return (
    <AuthContext.Provider value={{ user, login, logout, isLoggedIn }}>
      {children}
    </AuthContext.Provider>
  );
}
