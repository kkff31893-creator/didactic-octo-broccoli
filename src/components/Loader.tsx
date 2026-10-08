import { useEffect, useRef, useState } from 'react'
import heroImg from '../assets/img/hero.webp'

// Реальный прогресс: шрифт и главное фото. Без искусственных задержек дольше 0,9 с.
export default function Loader({ onDone }: { onDone: () => void }) {
  const pctEl = useRef<HTMLSpanElement>(null)
  const barEl = useRef<HTMLElement>(null)
  const [done, setDone] = useState(false)

  useEffect(() => {
    document.body.classList.add('locked')
    const total = 2
    let real = 0
    const bump = () => { real += 1 }
    const i = new Image()
    i.onload = bump
    i.onerror = bump
    i.src = heroImg
    document.fonts.load('600 40px "Inter Tight Variable"').then(bump, bump)

    const t0 = performance.now()
    let shown = 0
    let raf = 0
    const loop = () => {
      const target = Math.min((real / total) * 100, ((performance.now() - t0) / 900) * 100)
      shown += Math.max(0.6, (target - shown) * 0.12)
      if (shown > target) shown = target
      if (pctEl.current) pctEl.current.textContent = String(Math.round(shown))
      if (barEl.current) barEl.current.style.width = shown + '%'
      if (shown >= 99.9 && real >= total) {
        setTimeout(() => {
          setDone(true)
          document.body.classList.remove('locked')
          onDone()
        }, 200)
        return
      }
      raf = requestAnimationFrame(loop)
    }
    raf = requestAnimationFrame(loop)
    return () => cancelAnimationFrame(raf)
  }, [onDone])

  return (
    <div className={'loader' + (done ? ' done' : '')} role="status" aria-live="polite">
      <div className="loader-in">
        <div className="loader-row">
          <span>LOADING GARAGE...</span>
          <span><span ref={pctEl}>0</span>%</span>
        </div>
        <div className="loader-bar"><i ref={barEl} /></div>
      </div>
    </div>
  )
}
