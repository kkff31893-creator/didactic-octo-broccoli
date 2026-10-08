// Профили клиентов. Профиль выбирается параметром ?c=<ключ> в адресе, по умолчанию — demo.
// Чтобы сделать персональное демо: скопируйте профиль, замените данные, добавьте его в объект profiles внизу файла.
import heroDemo from '../assets/img/hero.webp'
import engine from '../assets/img/engine.webp'
import engine3 from '../assets/img/engine3.webp'
import brake from '../assets/img/brake.webp'
import lift from '../assets/img/lift.webp'
import disc from '../assets/img/disc.webp'
import wheel from '../assets/img/wheel.webp'

const U = (id: string, w = 1600, h?: number) =>
  'https://images.unsplash.com/photo-' + id + '?w=' + w + (h ? '&h=' + h + '&fit=crop&crop=center' : '') + '&q=80&auto=format'

export type Profile = {
  site: {
    name: string
    tagline: string
    city: string
    phone: string
    phoneHref: string
    address: string
    hours: string
    map: { lat: number; lng: number; delta: number }
    formEndpoint: string
  }
  title: string
  hero: { img: string; alt: string; kicker: string; title: string[]; sub: string; cta: string; facts: [string, string][] }
  statement: string
  highlights: { title: string; items: { img: string; kicker: string; title: string; text: string }[] }
  price: { title: string; note: string; items: { title: string; price: string }[] }
  scan: { img: string; alt: string; kicker: string; title: string[]; idle: string; steps: { x: number; y: number; title: string; text: string }[] }
  stats: null | { kicker: string; title: string[]; items: { value: number; decimals?: number; suffix: string; label: string }[]; link?: { href: string; text: string } }
  works: null | { img: string; tag: string; title: string; text: string }[]
  reviews: null | { name: string; car: string; rating: number; date: string; text: string }[]
  booking: { title: string; sub: string; services: string[] }
  footerNote: string
}

const demo: Profile = {
  site: {
    name: 'AutoPro',
    tagline: 'Автосервис Тюмень',
    city: 'Тюмень',
    phone: '+7 (3452) 12-34-56',
    phoneHref: '+73452123456',
    address: 'г. Тюмень, ул. Примерная, 12',
    hours: 'Пн–Сб: 09:00–20:00',
    map: { lat: 57.1522, lng: 65.5272, delta: 0.045 },
    formEndpoint: '',
  },
  title: 'AutoPro — автосервис в Тюмени: диагностика, ремонт, ТО',
  hero: {
    img: heroDemo,
    alt: 'Автомобиль в тёмном сервисном боксе',
    kicker: 'AutoPro · Тюмень',
    title: ['Автосервис', 'в Тюмени.'],
    sub: 'Профессиональное обслуживание вашего автомобиля. Диагностика, ремонт и ТО с гарантией на выполненные работы.',
    cta: 'Записаться на сервис',
    facts: [['Тюмень', 'ул. Примерная, 12'], ['Профессиональный сервис', 'с 2014 года'], ['Гарантия 12 мес.', 'на все работы']],
  },
  statement: 'Мы чиним машины так, как чинили бы свою. Показываем каждую деталь, согласуем цену до начала работ и даём гарантию на год.',
  highlights: {
    title: 'Услуги. Всё в одном боксе.',
    items: [
      { img: engine3, kicker: 'Двигатель', title: 'Ремонт без догадок.', text: 'Находим причину, а не меняем всё подряд.' },
      { img: lift, kicker: 'ТО', title: 'Обслуживание за один визит.', text: 'Масло, фильтры, осмотр ходовой. По регламенту.' },
      { img: brake, kicker: 'Тормоза', title: 'Останавливается уверенно.', text: 'Колодки, диски, суппорта. Проверка на стенде.' },
      { img: wheel, kicker: 'Шиномонтаж', title: 'Сезон без очередей.', text: 'Замена, балансировка, хранение. По записи.' },
      { img: disc, kicker: 'Диски', title: 'Точно в допуске.', text: 'Контроль биения после каждой замены.' },
    ],
  },
  price: {
    title: 'Цены без сюрпризов.',
    note: 'Стоимость работ без запчастей. Точную сумму называем после осмотра и до начала ремонта.',
    items: [
      { title: 'Компьютерная диагностика', price: 'от 800 ₽' },
      { title: 'ТО автомобиля', price: 'от 1 500 ₽' },
      { title: 'Замена масла', price: 'от 600 ₽' },
      { title: 'Ремонт двигателя', price: 'от 3 500 ₽' },
      { title: 'Ремонт ходовой', price: 'от 1 200 ₽' },
      { title: 'Ремонт тормозной системы', price: 'от 1 200 ₽' },
      { title: 'Электрика', price: 'от 1 000 ₽' },
      { title: 'Кондиционер', price: 'от 1 800 ₽' },
      { title: 'Шиномонтаж', price: 'от 1 600 ₽' },
    ],
  },
  scan: {
    img: engine,
    alt: 'Моторный отсек на диагностике',
    kicker: 'Диагностика',
    title: ['Видим то, что', 'не видно глазу.'],
    idle: 'Технологии, которые работают на ваш автомобиль.',
    steps: [
      { x: 50, y: 14, title: 'Впуск', text: 'Герметичность впуска и состояние фильтра.' },
      { x: 49, y: 48, title: 'Топливная система', text: 'Подача и смесеобразование: ровная работа и расход.' },
      { x: 74, y: 73, title: 'Зажигание', text: 'Катушки, провода, свечи. Без пропусков и потери тяги.' },
      { x: 27, y: 53, title: 'Магистрали', text: 'Давление, утечки и износ патрубков.' },
    ],
  },
  stats: {
    kicker: 'Почему выбирают нас',
    title: ['Надёжность,', 'проверенная временем.'],
    items: [
      { value: 10, suffix: '+', label: 'лет опыта' },
      { value: 5000, suffix: '+', label: 'обслуженных автомобилей' },
      { value: 98, suffix: '%', label: 'довольных клиентов' },
      { value: 12, suffix: ' мес.', label: 'гарантии на работы' },
    ],
  },
  works: [
    { img: engine3, tag: 'Двигатель', title: 'Диагностика и настройка мотора', text: 'Плавающие обороты: нашли подсос воздуха за час, устранили в тот же день.' },
    { img: brake, tag: 'Тормоза', title: 'Тормозная система под ключ', text: 'Диски, колодки, прокачка. Проверили на стенде перед выдачей.' },
    { img: lift, tag: 'ТО', title: 'Комплексное обслуживание', text: 'Осмотр на подъёмнике, масло и фильтры, отчёт с фото.' },
    { img: disc, tag: 'Тормоза', title: 'Замена тормозных дисков', text: 'Подобрали диски под стиль езды, проверили биение.' },
  ],
  reviews: [
    { name: 'Алексей К.', car: 'Toyota Camry', rating: 5, date: '12.09.2026', text: 'Сделали полное ТО быстро и аккуратно. Мастер всё показал, цена совпала со сметой.' },
    { name: 'Мария С.', car: 'Kia Sportage', rating: 5, date: '03.09.2026', text: 'В другом месте насчитали на 40 тысяч. Здесь показали на подъёмнике, что менять нужно только две стойки.' },
    { name: 'Дмитрий П.', car: 'Skoda Octavia', rating: 5, date: '28.08.2026', text: 'Причину плавающих оборотов нашли за час. Устранили в тот же день и дали гарантию.' },
    { name: 'Игорь В.', car: 'Hyundai Solaris', rating: 5, date: '17.08.2026', text: 'Приехал к назначенному времени, ждать не пришлось. Тормоза как новые.' },
    { name: 'Елена Т.', car: 'Volkswagen Tiguan', rating: 5, date: '05.08.2026', text: 'Горел Check Engine. Диагностика, ремонт и отчёт в мессенджер. Без навязанных услуг.' },
    { name: 'Сергей Н.', car: 'Lada Vesta', rating: 5, date: '22.07.2026', text: 'Езжу сюда третий год. Чисто, аккуратно, всегда отдают старые детали.' },
  ],
  booking: {
    title: 'Запишитесь на обслуживание.',
    sub: 'Остальное мы возьмём на себя.',
    services: ['Диагностика', 'ТО автомобиля', 'Замена масла', 'Ремонт двигателя', 'Ремонт ходовой', 'Тормозная система', 'Электрика', 'Кондиционер', 'Шиномонтаж', 'Другое'],
  },
  footerNote: 'Демо-сайт: данные условные, фото Unsplash.',
}

// Персональное демо для «Урбанвил» (шинный обменный пункт). Данные — из открытой карточки 2ГИС.
const urbanvil: Profile = {
  site: {
    name: 'Урбанвил',
    tagline: 'Шины и диски · Тюмень',
    city: 'Тюмень',
    phone: '+7 (985) 655-33-32',
    phoneHref: '+79856553332',
    address: 'г. Тюмень, Старый Тобольский тракт 5 км, 3 ст4',
    hours: 'Ежедневно: 09:00–19:00',
    map: { lat: 57.110422, lng: 65.753041, delta: 0.018 },
    formEndpoint: '',
  },
  title: 'Урбанвил — шины и диски в Тюмени: выкуп, обмен, шиномонтаж',
  hero: {
    img: U('1578844251758-2f71da64c96f', 2200),
    alt: 'Стопки зимних шин',
    kicker: 'Урбанвил · Тюмень',
    title: ['Шины и диски', 'без переплаты.'],
    sub: 'Выкуп и обмен б/у шин, продажа, шиномонтаж, ремонт дисков и хранение. Ежедневно с 9 до 19.',
    cta: 'Записаться на шиномонтаж',
    facts: [['Тюмень', 'Старый Тобольский тракт, 5 км'], ['Рейтинг 4,8', '613 оценок в 2ГИС'], ['Ежедневно', 'с 09:00 до 19:00']],
  },
  statement: 'Привозите старые шины. Оценим износ при вас, выкупим или зачтём в обмен, подберём комплект из наличия и сразу поставим.',
  highlights: {
    title: 'Всё для колёс. В одном месте.',
    items: [
      { img: U('1527266258038-6ae3e089a609', 1400), kicker: 'Выкуп и обмен', title: 'Старые шины в зачёт.', text: 'Оценим износ при вас и выкупим или зачтём в обмен.' },
      { img: U('1599082267768-4815b2ea6bd2', 1400), kicker: 'Шиномонтаж', title: 'Переобуем за полчаса.', text: 'Снятие, монтаж, балансировка. По записи без очереди.' },
      { img: U('1593699199342-59b40e08f0ac', 1400), kicker: 'Диски', title: 'Ровные, как с завода.', text: 'Правка, прокатка и сварка дисков.' },
      { img: U('1760836395760-9831facb4754', 1400), kicker: 'Хранение и аренда', title: 'Комплект подождёт у нас.', text: 'Сезонное хранение и аренда колёс.' },
      { img: U('1571335746824-742511d49bce', 1400), kicker: 'Ошиповка и ремонт', title: 'Зима без сюрпризов.', text: 'Ошиповка, ремонт порезов и проколов.' },
    ],
  },
  price: {
    title: 'Что мы делаем.',
    note: 'Стоимость зависит от радиуса и состояния. Точную цену назовём по телефону или на месте.',
    items: [
      { title: 'Выкуп б/у шин', price: 'оценка при вас' },
      { title: 'Продажа б/у шин и дисков', price: 'из наличия' },
      { title: 'Обмен шин с доплатой', price: 'по оценке' },
      { title: 'Шиномонтаж и балансировка', price: 'по записи' },
      { title: 'Ремонт порезов и проколов', price: '' },
      { title: 'Правка, прокатка и сварка дисков', price: '' },
      { title: 'Ошиповка', price: '' },
      { title: 'Сезонное хранение и аренда колёс', price: '' },
      { title: 'Доставка', price: 'по городу' },
    ],
  },
  scan: {
    img: U('1601411101851-ea0e07766235', 1600, 667),
    alt: 'Колесо крупным планом: протектор, боковина и диск',
    kicker: 'Честная оценка',
    title: ['Проверяем шину', 'при вас.'],
    idle: 'Прежде чем купить или выкупить, смотрим четыре вещи.',
    steps: [
      { x: 26, y: 45, title: 'Протектор', text: 'Глубина и равномерность износа по всей ширине.' },
      { x: 42, y: 22, title: 'Плечевая зона', text: 'Неравномерный износ подскажет, что не так с развалом.' },
      { x: 50, y: 67, title: 'Боковина', text: 'Порезы, грыжи и трещины, с которыми ездить нельзя.' },
      { x: 58, y: 51, title: 'Диск', text: 'Биение, вмятины и коррозия посадочных полок.' },
    ],
  },
  stats: {
    kicker: 'Нам доверяют',
    title: ['Оценки клиентов,', 'а не слова.'],
    items: [
      { value: 4.8, decimals: 1, suffix: '★', label: 'средняя оценка в 2ГИС' },
      { value: 613, suffix: '', label: 'оценок от клиентов' },
      { value: 7, suffix: ' дней', label: 'в неделю, с 9 до 19' },
    ],
    link: { href: 'https://2gis.ru/tyumen/firm/70000001062432933/tab/reviews', text: 'Читать отзывы в 2ГИС' },
  },
  works: null,
  reviews: null,
  booking: {
    title: 'Запишитесь на шиномонтаж.',
    sub: 'Или привезите шины на оценку.',
    services: ['Шиномонтаж', 'Выкуп шин', 'Обмен шин', 'Покупка шин или дисков', 'Ремонт диска', 'Ошиповка', 'Хранение', 'Другое'],
  },
  footerNote: 'Демо-версия сайта для «Урбанвил». Данные из открытой карточки 2ГИС, фото Unsplash.',
}

export const profiles: Record<string, Profile> = { demo, urbanvil }

const key = typeof location !== 'undefined' ? new URLSearchParams(location.search).get('c') ?? 'demo' : 'demo'
export const profile: Profile = profiles[key] ?? demo
