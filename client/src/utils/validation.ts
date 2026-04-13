/** Mirrors api/auth_validation.py */

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const SPECIAL_CHAR_PATTERN = /[!@#$%^&*(),.?":{}|<>\[\]\\/_\-+=]/

export function normalizePhone(phone: string): string {
  return (phone || '').replace(/\D/g, '')
}

export function isValidEmail(email: string): boolean {
  return Boolean(email && EMAIL_PATTERN.test(email.trim()))
}

export function isValidPassword(password: string): boolean {
  if (!password || password.length <= 6) return false
  return SPECIAL_CHAR_PATTERN.test(password)
}
