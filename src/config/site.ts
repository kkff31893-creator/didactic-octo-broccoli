// Всё, что нужно заменить для реального клиента, лежит здесь и в content.ts.
export const site = {
  name: 'AutoPro',
  tagline: 'Автосервис Тюмень',
  city: 'Тюмень',
  cityIn: 'Тюмени', // «в Тюмени»
  phone: '+7 (3452) 12-34-56',
  phoneHref: '+73452123456',
  address: 'г. Тюмень, ул. Примерная, 12',
  hours: 'Пн–Сб: 09:00–20:00',
  since: 2014,
  warrantyMonths: 12,
  // Координаты центра карты (OpenStreetMap)
  map: { lat: 57.1522, lng: 65.5272, delta: 0.045 },
  // Адрес, куда отправлять заявки. Пока пусто — форма только подтверждает на странице.
  formEndpoint: '' as string,
}
export type Site = typeof site
