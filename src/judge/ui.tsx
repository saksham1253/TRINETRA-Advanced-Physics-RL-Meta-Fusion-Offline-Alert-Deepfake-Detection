import type { ReactNode } from 'react'
import { cx } from '../console/ui/primitives'

// Small typographic extensions of the console design system (trn tokens) for the long-form judge page.
export function Heading({ level = 2, children, className }: { level?: 1 | 2 | 3; children: ReactNode; className?: string }) {
  if (level === 1) return <h1 className={cx('font-trn-display text-4xl font-semibold leading-tight tracking-tight text-trn-text md:text-6xl', className)}>{children}</h1>
  if (level === 3) return <h3 className={cx('font-trn-display text-lg font-semibold text-trn-text', className)}>{children}</h3>
  return <h2 className={cx('font-trn-display text-2xl font-semibold tracking-tight text-trn-text md:text-3xl', className)}>{children}</h2>
}

export function Eyebrow({ children, className }: { children: ReactNode; className?: string }) {
  return <p className={cx('font-trn-mono text-xs uppercase tracking-widest text-trn-brand', className)}>{children}</p>
}

export function Rule({ className }: { className?: string }) {
  return <hr className={cx('border-0 border-t border-trn-line', className)} />
}
