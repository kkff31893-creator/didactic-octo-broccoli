import { site } from '../config/site'

export function LogoMark() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M2 21 10.4 3h3.2L22 21h-4.3l-1.8-4H8.1l-1.8 4zm7.6-7.4h4.8L12 8.2z" fill="currentColor" />
    </svg>
  )
}

export default function Logo() {
  return (
    <a className="logo" href="#top" aria-label={site.name}>
      <LogoMark />
      {site.name}
    </a>
  )
}
