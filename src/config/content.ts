// Контент выбранного профиля (src/config/profiles.ts). Компоненты читают его отсюда.
import { profile } from './profiles'

export { profile }

export const nav = [
  { id: 'services', label: 'Услуги' },
  { id: 'about', label: profile.works ? 'О сервисе' : 'О нас' },
  ...(profile.works ? [{ id: 'works', label: 'Наши работы' }] : []),
  ...(profile.reviews ? [{ id: 'reviews', label: 'Отзывы' }] : []),
  { id: 'contact', label: 'Контакты' },
]

export const statement = profile.statement
export const highlights = profile.highlights.items
export const services = profile.price.items
export const scanImage = profile.scan.img
export const scanSteps = profile.scan.steps
export const works = profile.works ?? []
export const reviews = profile.reviews ?? []
export const contactServices = profile.booking.services
