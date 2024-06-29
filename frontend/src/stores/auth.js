import { writable } from 'svelte/store';

export const isAuthenticated = writable(false);

if (typeof window !== 'undefined' && localStorage.getItem('authToken')) {
  isAuthenticated.set(true);
}