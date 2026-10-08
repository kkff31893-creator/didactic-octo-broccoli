// Данные клиента берутся из выбранного профиля (src/config/profiles.ts).
import { profile } from './profiles'

export const site = profile.site
export type Site = typeof site
