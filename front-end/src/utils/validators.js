import { onlyDigits } from './masks'

export function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(value || ''))
}

export function isValidCpfCnpj(value) {
  const len = onlyDigits(value).length
  return len === 11 || len === 14
}

export function isValidPhone(value) {
  const len = onlyDigits(value).length
  return len === 0 || len === 10 || len === 11
}

export function isValidCep(value) {
  return onlyDigits(value).length === 8
}

export const passwordRules = [
  { key: 'length', label: '8–20 caracteres', test: (v) => v.length >= 8 && v.length <= 20 },
  { key: 'upper', label: '1 maiúscula', test: (v) => /[A-Z]/.test(v) },
  { key: 'number', label: '1 número', test: (v) => /\d/.test(v) },
  {
    key: 'special',
    label: '1 caractere especial',
    test: (v) => /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(v),
  },
]

export function isValidPassword(value) {
  return passwordRules.every((rule) => rule.test(String(value || '')))
}
