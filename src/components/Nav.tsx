import { useEffect, useState } from 'react'
import { Menu, X } from 'lucide-react'
import Logo from './Logo'
import { nav } from '../config/content'

// Полноширинная панель над первым экраном, плавающая «пилюля» после него
export default function Nav() {
  const [pill, setPill] = useState(false)
  const [open, setOpen] = useState(false)
  const [active, setActive] = useState('')

  useEffect(() => {
    const onScroll = () => setPill(window.scrollY > window.innerHeight * 0.6)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => {
    const els = nav.map((n) => document.getElementById(n.id)).filter(Boolean) as HTMLElement[]
    const io = new IntersectionObserver(
      (entries) => entries.forEach((e) => e.isIntersecting && setActive(e.target.id)),
      { rootMargin: '-45% 0px -50% 0px' },
    )
    els.forEach((el) => io.observe(el))
    return () => io.disconnect()
  }, [])

  useEffect(() => {
    document.body.classList.toggle('locked', open)
  }, [open])

  return (
    <>
      <header className={'nav' + (pill ? ' pill' : '')}>
        <div className="nav-in">
          <Logo />
          <nav className="menu" aria-label="Разделы">
            {nav.map((n) => (
              <a key={n.id} href={'#' + n.id} className={active === n.id ? 'active' : ''}>{n.label}</a>
            ))}
          </nav>
          <a className="btn btn-blue btn-sm" href="#contact">Записаться</a>
          <button className="burger" aria-label={open ? 'Закрыть меню' : 'Открыть меню'} onClick={() => setOpen((v) => !v)}>
            {open ? <X /> : <Menu />}
          </button>
        </div>
      </header>
      <div className={'mobile-menu' + (open ? ' open' : '')}>
        {nav.map((n) => (
          <a key={n.id} href={'#' + n.id} onClick={() => setOpen(false)}>{n.label}</a>
        ))}
        <a className="btn btn-blue" href="#contact" onClick={() => setOpen(false)}>Записаться на сервис</a>
      </div>
    </>
  )
}
