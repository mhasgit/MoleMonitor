import { createContext, useContext } from 'react'

export type BackendStatusContextType = {
  backendError: boolean
  setBackendError: (v: boolean) => void
  retry: () => Promise<void>
}

export const BackendStatusContext = createContext<BackendStatusContextType | null>(null)

export function useBackendStatus() {
  const ctx = useContext(BackendStatusContext)
  return ctx
}
