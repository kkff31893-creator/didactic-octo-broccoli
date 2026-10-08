import { useRef } from 'react'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { reviews } from '../config/content'

export default function Reviews() {
  const track = useRef<HTMLDivElement>(null)

  const go = (dir: number) => {
    const t = track.current
    const card = t?.querySelector<HTMLElement>('.rv')
    if (!t || !card) return
    t.scrollBy({ left: dir * (card.offsetWidth + 20), behavior: 'smooth' })
  }

  return (
    <section className="reviews" id="reviews">
      <div className="wrap sec-top" data-reveal>
        <div>
          <p className="kicker">Отзывы</p>
          <h2 className="h-l">Что говорят клиенты.</h2>
        </div>
        <div style={{ display: 'flex', gap: 12 }}>
          <button className="round" onClick={() => go(-1)} aria-label="Назад"><ChevronLeft /></button>
          <button className="round" onClick={() => go(1)} aria-label="Вперёд"><ChevronRight /></button>
        </div>
      </div>
      <div className="rv-track" ref={track} data-reveal>
        {reviews.map((r) => (
          <article className="rv" key={r.name}>
            <div className="rv-stars" aria-label={`Оценка ${r.rating} из 5`}>{'★'.repeat(r.rating)}</div>
            <p>«{r.text}»</p>
            <div className="rv-who">
              <div>
                <b>{r.name}</b>
                {r.car}
              </div>
              <time>{r.date}</time>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}
