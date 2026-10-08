import { useEffect, useRef, useState } from 'react'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { highlights, profile, services } from '../config/content'

export default function Highlights() {
  const track = useRef<HTMLDivElement>(null)
  const [idx, setIdx] = useState(0)

  useEffect(() => {
    const t = track.current
    if (!t) return
    const onScroll = () => {
      const card = t.querySelector<HTMLElement>('.hl')
      if (!card) return
      const step = card.offsetWidth + 20
      setIdx(Math.min(highlights.length - 1, Math.round(t.scrollLeft / step)))
    }
    t.addEventListener('scroll', onScroll, { passive: true })
    return () => t.removeEventListener('scroll', onScroll)
  }, [])

  const go = (i: number) => {
    const t = track.current
    const card = t?.querySelectorAll<HTMLElement>('.hl')[i]
    if (!t || !card) return
    t.scrollTo({ left: card.offsetLeft - t.querySelector<HTMLElement>('.hl')!.offsetLeft, behavior: 'smooth' })
  }

  return (
    <section className="highlights" id="services">
      <div className="wrap sec-top" data-reveal>
        <h2 className="h-l">{profile.highlights.title}</h2>
        <a className="link" href="#price">{profile.price.title.replace(/\.$/, '')} <ChevronRight /></a>
      </div>

      <div className="hl-track" ref={track} data-reveal>
        {highlights.map((h) => (
          <article className="hl" key={h.title}>
            <img src={h.img} alt={h.kicker} loading="lazy" />
            <div className="hl-cap">
              <small>{h.kicker}</small>
              <b>{h.title}</b>
              <span>{h.text}</span>
            </div>
          </article>
        ))}
      </div>

      <div className="hl-ctrl">
        <button className="round" onClick={() => go(idx - 1)} disabled={idx === 0} aria-label="Предыдущая"><ChevronLeft /></button>
        <div className="dots">
          {highlights.map((h, i) => (
            <button key={h.title} className={i === idx ? 'on' : ''} onClick={() => go(i)} aria-label={'Слайд ' + (i + 1)} />
          ))}
        </div>
        <button className="round" onClick={() => go(idx + 1)} disabled={idx === highlights.length - 1} aria-label="Следующая"><ChevronRight /></button>
      </div>

      <div className="wrap price" id="price">
        <div data-reveal>
          <h3 className="h-m">{profile.price.title}</h3>
          <p className="mute" style={{ marginTop: 14, maxWidth: '32ch' }}>{profile.price.note}</p>
        </div>
        <ul data-reveal>
          {services.map((s) => (
            <li key={s.title}>{s.title}{s.price && <span>{s.price}</span>}</li>
          ))}
        </ul>
      </div>
    </section>
  )
}
