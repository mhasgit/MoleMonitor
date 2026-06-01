/** Mirrors api/auth_validation.py */

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const SPECIAL_CHAR_PATTERN = /[!@#$%^&*(),.?":{}|<>\[\]\\/_\-+=]/

export function normalizePhone(phone: string): string {
  // Strip non-digits for consistent phone storage and comparisons.
  return (phone || '').replace(/\D/g, '')
}

export function isValidEmail(email: string): boolean {
  // Validate email with the same regex rules used by backend auth checks.
  return Boolean(email && EMAIL_PATTERN.test(email.trim()))
}

export function isValidPassword(password: string): boolean {
  // Enforce minimum length and special character requirement for passwords.
  if (!password || password.length <= 6) return false
  return SPECIAL_CHAR_PATTERN.test(password)
}
