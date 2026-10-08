import { useState } from 'react'
import { site } from '../config/site'
import { contactServices } from '../config/content'

function maskPhone(v: string) {
  let d = v.replace(/\D/g, '')
  if (d.startsWith('8')) d = '7' + d.slice(1)
  if (d && !d.startsWith('7')) d = '7' + d
  d = d.slice(0, 11)
  let o = d ? '+7' : ''
  if (d.length > 1) o += ' (' + d.slice(1, 4)
  if (d.length > 4) o += ') ' + d.slice(4, 7)
  if (d.length > 7) o += '-' + d.slice(7, 9)
  if (d.length > 9) o += '-' + d.slice(9, 11)
  return o
}

export default function Booking() {
  const [phone, setPhone] = useState('')
  const [bad, setBad] = useState(false)
  const [sent, setSent] = useState(false)
  const [busy, setBusy] = useState(false)

  const { lat, lng, delta } = site.map
  const bbox = [lng - delta * 1.6, lat - delta, lng + delta * 1.6, lat + delta].join('%2C')
  const mapSrc = `https://www.openstreetmap.org/export/embed.html?bbox=${bbox}&layer=mapnik&marker=${lat}%2C${lng}`

  const submit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (phone.replace(/\D/g, '').length < 11) {
      setBad(true)
      return
    }
    setBusy(true)
    const data = Object.fromEntries(new FormData(e.currentTarget).entries())
    try {
      if (site.formEndpoint) {
        await fetch(site.formEndpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      } else {
        await new Promise((r) => setTimeout(r, 500))
      }
      setSent(true)
    } catch {
      setBusy(false)
      alert('Не удалось отправить заявку. Позвоните нам: ' + site.phone)
    }
  }

  return (
    <section className="booking" id="contact">
      <div className="wrap">
        <div data-reveal>
          <p className="kicker">Запись</p>
          <h2 className="h-l">Запишитесь на обслуживание.<br /><span className="mute">Остальное мы возьмём на себя.</span></h2>
        </div>
        <div className="book-grid">
          <div data-reveal>
            {sent ? (
              <div className="sent" role="status">
                <h3 className="h-m">Заявка принята.</h3>
                <p className="mute">Перезвоним в течение 10 минут в рабочее время.</p>
              </div>
            ) : (
              <form className="form" onSubmit={submit} noValidate>
                <div className="field">
                  <label htmlFor="f-name">Имя</label>
                  <input id="f-name" name="name" autoComplete="name" />
                </div>
                <div className={'field' + (bad ? ' bad' : '')}>
                  <label htmlFor="f-phone">Телефон{bad ? ': введите полностью' : ''}</label>
                  <input id="f-phone" name="phone" type="tel" inputMode="tel" autoComplete="tel" placeholder="+7 (___) ___-__-__" value={phone}
                    onChange={(e) => { setPhone(maskPhone(e.target.value)); setBad(false) }} />
                </div>
                <div className="field">
                  <label htmlFor="f-car">Марка автомобиля</label>
                  <input id="f-car" name="car" />
                </div>
                <div className="field">
                  <label htmlFor="f-service">Какая услуга нужна</label>
                  <select id="f-service" name="service" defaultValue={contactServices[0]}>
                    {contactServices.map((s) => <option key={s}>{s}</option>)}
                  </select>
                </div>
                <button className="btn btn-blue" type="submit" disabled={busy}>{busy ? 'Отправляем…' : 'Отправить заявку'}</button>
                <p className="agree">Нажимая кнопку, вы соглашаетесь на обработку персональных данных.</p>
              </form>
            )}
          </div>
          <div data-reveal data-delay={0.1}>
            <div className="info-row"><small>Адрес</small><b>{site.address}</b></div>
            <a className="info-row" href={'tel:' + site.phoneHref}><small>Телефон</small><b>{site.phone}</b></a>
            <div className="info-row"><small>Режим работы</small><b>{site.hours}</b></div>
            <div className="map">
              <iframe title="Карта: как нас найти" src={mapSrc} loading="lazy" referrerPolicy="no-referrer" />
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
