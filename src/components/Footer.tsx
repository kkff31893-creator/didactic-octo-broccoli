import { nav } from '../config/content'
import { site } from '../config/site'

export default function Footer() {
  return (
    <footer className="foot">
      <div className="wrap foot-in">
        <span>© {new Date().getFullYear()} {site.name}, {site.city}. Демо-сайт: данные условные, фото Unsplash.</span>
        <nav aria-label="Разделы">
          {nav.map((n) => <a key={n.id} href={'#' + n.id}>{n.label}</a>)}
        </nav>
      </div>
    </footer>
  )
}
